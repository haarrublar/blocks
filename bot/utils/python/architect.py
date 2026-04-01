import os
import anthropic
import json
from dotenv import load_dotenv
from aux_functions import load_json, save_json
from build.build_cylinder import build_cylinder
from build.build_rectangle import build_rectangle
from build.prompts.prompts import BUILD_PROMPT
from build.tools import TOOLS
import re


load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def claude_architect(session_id: str, table_path: str, player_coordinates: dict = None):
    table = load_json(table_path)
    if session_id not in table:
        return {"error": "Session not found in table"}

    BUILDERS = {
        "build_rectangle": build_rectangle,
        "build_cylinder": build_cylinder,
    }

    session_parts = table[session_id]

    has_completed = any(
        part.get("Status") == "COMPLETED"
        for parts_list in session_parts.values()
        for part in parts_list
    )

    valid_keys = [k for k in session_parts.keys() if str(k).isdigit()]
    for part_id in sorted(valid_keys, key=int):
        parts_list = session_parts[part_id] 

        for part in parts_list:
            if part.get("Status") != "PENDING":
                continue

            print(f"🏗️ Architecting Part {part_id}: {part['Name']}...")

            context = json.dumps(session_parts, indent=2)

            if not has_completed:
                player_ctx = f"PLAYER_COORDS (Origin for ID 1): {json.dumps(player_coordinates)}\n"
            else:
                player_ctx = "CONTEXT: Align this part using the 'boundaries' of the ID specified in the Logic field.\n"

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=BUILD_PROMPT["architect_prompt"],
                tools=TOOLS,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"{player_ctx}"
                            f"Context Table:\n{context}\n\n"
                            f"Task: Calculate coordinates for part ID {part_id} "
                            f"and call the appropriate build tool."
                        ),
                    }
                ],
            )

            tool_was_called = False
            for content in response.content:
                if content.type == "tool_use":
                    args = content.input
                    print(f"  🔧 Tool: {content.name} | Args: {args}")

                    if content.name in BUILDERS:
                        result = BUILDERS[content.name](**args)

                        part["Status"] = "COMPLETED"
                        part["boundaries"] = result.get("bounds")
                        part["Commands"] = result.get("commands", [])

                        has_completed = True
                        tool_was_called = True
                        print(f"  ✅ COMPLETED. top={part['boundaries'].get('top')}")
                        
                        save_json(table, table_path)
                    else:
                        print(f"  ⚠️ Unknown tool: {content.name}")

            if not tool_was_called:
                print(f"  ❌ No tool called for part {part_id}. LLM said:")
                for block in response.content:
                    if block.type == "text":
                        print(f"     {block.text[:400]}")

    return {"status": "success", "session_id": session_id}