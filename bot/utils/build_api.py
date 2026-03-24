import anthropic
import os
import json
from dotenv import load_dotenv
from .build.tools import TOOLS
from .build.build_rectangle import build_rectangle
from .build.build_triangle import build_triangle
from .build.build_cylinder import build_cylinder
import json
import os

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

def ask_claude_build(
        player_coord: dict, 
        task_description: str, 
        session_id: str, 
        all_sessions: dict
    ):
    
    session_data = all_sessions.get(session_id)
    history = session_data.get("history",[])
    
    task_description = (task_description or "").strip().lower()

    if task_description == "reset":
        return {
            "llm_reasoning": "Session reset. Starting new architectural log",
            "action_payload": "" # Always return an empty string for the payload too
        }
    
    history.append({"role": "user", "content": task_description})

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=TOOLS,
        system="You are a Minecraft Architect. Coordinates are pre-loaded. Remember previous dimensions and parameters from the history.",
        messages=history
    )

    reasoning = ""
    all_commands = []
    assistant_content = []

    BUILDERS = {
        "build_rectangle": build_rectangle,
        "build_triangle": build_triangle,
        "build_cylinder": build_cylinder,
    }

    for content in response.content:
        if content.type == "text":
            reasoning += content.text
            assistant_content.append({"type": "text", "text": content.text})

        elif content.type == "tool_use":
            args = {**content.input, **player_coord}
            commands = BUILDERS[content.name](**args)
            all_commands.extend(commands)

            assistant_content.append({
                "type": "tool_use",
                "id": content.id,
                "name": content.name,
                "input": content.input
            })

            # Flush assistant message before tool_result
            history.append({"role": "assistant", "content": assistant_content})
            history.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": content.id,
                    "content": f"Success. {len(commands)} commands generated."
                }]
            })
            assistant_content = []

    if assistant_content:
        history.append({"role": "assistant", "content": assistant_content})

    all_sessions[session_id]["history"] = history
    save_all_sessions(all_sessions)

    return {"llm_reasoning": reasoning, "action_payload": "\n".join(all_commands)}


# if __name__ == "__main__":
#     print("=== Minecraft Architect (Persistent Sessions) ===")

#     all_sessions = load_all_sessions()

#     if all_sessions:
#         current_session_id = list(all_sessions.keys())[-1]
#         print(f"Resuming session: {current_session_id}")
#     else:
#         current_session_id = str(uuid.uuid4())[:8]
#         print(f"New session: {current_session_id}")

#     try:
#         while True:
#             msg = input(f"\n[{current_session_id}] You: ").strip()
#             if not msg:
#                 continue

#             if msg.lower() == "reset":
#                 current_session_id = str(uuid.uuid4())[:8]
#                 print(f"New session: {current_session_id}")
#                 continue

#             result = ask_claude_build(msg, current_session_id, all_sessions)

#             if result["llm_reasoning"]:
#                 print(f"\nArchitect: {result['llm_reasoning']}")
#             if result["action_payload"]:
#                 print(f"\n--- COMMANDS ---\n{result['action_payload']}")

#     except KeyboardInterrupt:
#         print("\nSession saved. Goodbye!")