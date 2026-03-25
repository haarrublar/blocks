import json
import anthropic
import os
import json
from dotenv import load_dotenv
from .build.tools import TOOLS
from .build.build_rectangle import build_rectangle
from .build.build_triangle import build_triangle
from .build.build_cylinder import build_cylinder
from .build.prompts.building_prompt import planner_w_coordinates, execution_w_coordinates


HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'build_history.json')
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def load_all_sessions():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_all_sessions(all_sessions):
    with open(HISTORY_FILE, "w") as f:
        json.dump(all_sessions, f, indent=4)


def get_bounds(commands):
    """Extract real min/max coordinates from executed fill commands."""
    if not commands:
        return {}
        
    xs, ys, zs = [], [], []
    for cmd in commands:
        parts = cmd.lstrip('/').split()
        
        if parts[0].lower() == "fill":
            parts = parts[1:]
            
        if len(parts) >= 6:
            try:
                x1, y1, z1 = int(parts[0]), int(parts[1]), int(parts[2])
                x2, y2, z2 = int(parts[3]), int(parts[4]), int(parts[5])
                xs += [x1, x2]
                ys += [y1, y2]
                zs += [z1, z2]
            except ValueError:
                continue 
                
    if not xs: 
        return {}

    return {
        "x_min": min(xs), "x_max": max(xs),
        "y_min": min(ys), "y_max": max(ys),
        "z_min": min(zs), "z_max": max(zs),
        "top": max(ys) + 1,
        "center_x": (min(xs) + max(xs)) // 2,
        "center_z": (min(zs) + max(zs)) // 2,
    }
    
    

def ask_claude_build(
        player_coord: dict,
        task_description: str,
        session_id: str,
        all_sessions: dict
    ):

    session_data = all_sessions.setdefault(session_id, {"history": []})
    history = session_data["history"]

    if task_description.lower().strip() == "reset":
        history.clear()
        all_sessions[session_id]["history"] = history
        save_all_sessions(all_sessions)
        return {"llm_reasoning": "Session reset.", "action_payload": ""}

    def sanitize_history(history):
        """Remove any tool_use/tool_result pairs that are not properly matched."""
        cleaned = []
        i = 0
        while i < len(history):
            msg = history[i]

            if (msg["role"] == "user" and
                isinstance(msg.get("content"), list) and
                msg["content"] and
                msg["content"][0].get("type") == "tool_result"):
                # Check previous message has matching tool_use
                prev = cleaned[-1] if cleaned else None
                if not (prev and
                        prev["role"] == "assistant" and
                        isinstance(prev.get("content"), list) and
                        any(b.get("type") == "tool_use" and
                            b.get("id") == msg["content"][0].get("tool_use_id")
                            for b in prev["content"])):
                    i += 1
                    continue

            if (msg["role"] == "assistant" and
                isinstance(msg.get("content"), list) and
                any(b.get("type") == "tool_use" for b in msg["content"])):
                next_msg = history[i + 1] if i + 1 < len(history) else None
                is_followed = (
                    next_msg and
                    next_msg["role"] == "user" and
                    isinstance(next_msg.get("content"), list) and
                    any(b.get("type") == "tool_result" for b in next_msg["content"])
                )
                if not is_followed:
                    i += 1
                    continue

            cleaned.append(msg)
            i += 1
        return cleaned

    history[:] = sanitize_history(history)

    if not history:
        history.append({
            "role": "user",
            "content": f"Task: {task_description}\nPlayer at x={player_coord['x']}, y={player_coord['y']}, z={player_coord['z']}"
        })

    BUILDERS = {
        "build_rectangle": build_rectangle,
        "build_triangle": build_triangle,
        "build_cylinder": build_cylinder,
    }


    reasoning = f"Task: {task_description}\nPlayer: {player_coord}\n"

    plan_system = planner_w_coordinates(player_coord)

    if len(history) == 1:
        history.append({"role": "user", "content": (
            f"Deconstruct this request into a precise Lego-style plan:\n\n"
            f"Request: {task_description}\n"
            f"Player position: x={player_coord['x']}, y={player_coord['y']}, z={player_coord['z']}\n\n"
            f"Follow the layer model and deconstruction examples exactly."
        )})

        plan_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=TOOLS,
            tool_choice={"type": "none"},
            system=plan_system,
            messages=history
        )

        plan_text = plan_response.content[0].text.strip()
        reasoning += f"=== FULL PLAN ===\n{plan_text}\n\n"
        print("=== PLAN ===\n", plan_text)
        history.append({"role": "assistant", "content": plan_text})

    else:
        plan_text = next(
            (msg["content"] for msg in history
             if msg["role"] == "assistant" and isinstance(msg["content"], str)),
            None
        )
        if not plan_text:
            return {
                "llm_reasoning": "Could not recover plan. Please reset and try again.",
                "action_payload": ""
            }
        reasoning += f"=== RECOVERED PLAN ===\n{plan_text}\n\n"


    all_commands = []
    previous_bounds = None
    step = 0

    execution_system = execution_w_coordinates(player_coord)

    plan_message = {"role": "user", "content": f"The full plan:\n{plan_text}"}

    while True:
        step += 1

        prompt = f"Execute step {step} of the plan."

        if previous_bounds:
            prompt += (
                f"\n\nPrevious structure real bounds:\n{json.dumps(previous_bounds, indent=2)}"
                f"\n→ Stack ON TOP: y={previous_bounds['top']}"
                f"\n→ Place BESIDE at ground: y={player_coord['y']}"
                f"\n→ Previous center: x={previous_bounds['center_x']}, z={previous_bounds['center_z']}"
                f"\n→ Previous footprint: x[{previous_bounds['x_min']} to {previous_bounds['x_max']}],"
                f" z[{previous_bounds['z_min']} to {previous_bounds['z_max']}]"
            )
        else:
            prompt += f"\n\nThis is step 1. Player is at x={player_coord['x']}, y={player_coord['y']}, z={player_coord['z']}."

        reasoning += f"\n--- STEP {step} ---\n{prompt}\n"
        history.append({"role": "user", "content": prompt})

        execution_history = [m for m in history if m.get("content") != plan_text][-8:]

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=TOOLS,
            system=execution_system,
            messages=[plan_message] + execution_history,
        )

        tool_called = False

        for block in response.content:
            if block.type == "text":
                reasoning += f"Claude: {block.text}\n"
                if "BUILD COMPLETE" in block.text.upper():
                    history.append({"role": "assistant", "content": block.text})
                    all_sessions[session_id]["history"] = history
                    save_all_sessions(all_sessions)
                    return {
                        "llm_reasoning": reasoning.strip(),
                        "action_payload": "\n".join(all_commands)
                    }

            elif block.type == "tool_use":
                tool_called = True
                tool_name = block.name
                tool_input = {**player_coord, **block.input.copy()}

                if step > 1 and previous_bounds:
                    same_center = (
                        abs(tool_input.get("x", 0) - previous_bounds.get("center_x", 0)) < 5 and
                        abs(tool_input.get("z", 0) - previous_bounds.get("center_z", 0)) < 5
                    )
                    too_low = tool_input.get("y", 0) < previous_bounds.get("top", 0) - 5
                    if same_center and too_low:
                        reasoning += f"WARNING: forced y to previous top\n"
                        tool_input["y"] = previous_bounds["top"]

                commands = BUILDERS[tool_name](**tool_input)
                all_commands.extend(commands)

                if commands:
                    previous_bounds = get_bounds(commands)
                    reasoning += f"Step {step}: {tool_name} → top={previous_bounds['top']}\n"
                    print(f"Step {step} | {tool_name} → top={previous_bounds['top']}")

                history.append({
                    "role": "assistant",
                    "content": [{"type": "tool_use", "id": block.id,
                                 "name": tool_name, "input": tool_input}]
                })
                history.append({
                    "role": "user",
                    "content": [{"type": "tool_result", "tool_use_id": block.id,
                                 "content": (
                                     f"Step {step} done.\nReal bounds: {json.dumps(previous_bounds)}\n"
                                     f"Top for next stacked piece: y={previous_bounds['top']}\n"
                                     f"Center: x={previous_bounds['center_x']}, z={previous_bounds['center_z']}"
                                 )}]
                })

        if not tool_called:
            history.append({"role": "assistant",
                            "content": response.content[0].text if response.content else ""})
            break

    all_sessions[session_id]["history"] = history
    save_all_sessions(all_sessions)
    return {
        "llm_reasoning": reasoning.strip(),
        "action_payload": "\n".join(all_commands)
    }

