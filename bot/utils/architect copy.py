import os
import anthropic
import json
from dotenv import load_dotenv
from aux_functions import load_json, save_json
from build.build_cylinder import build_cylinder
from build.build_rectangle import build_rectangle
from build.prompts.prompts import BUILD_PROMPT
from build.tools import TOOLS

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

    for part_id, parts_list in session_parts.items():
        for part in parts_list:
            if part.get("Status") != "PENDING":
                continue

            print(f"🏗️ Architecting Part {part_id}: {part['Name']}...")

            context = json.dumps(table[session_id], indent=2)

            player_ctx = ""
            if not has_completed and player_coordinates:
                player_ctx = f"PLAYER_COORDS (origin for the first part): {json.dumps(player_coordinates)}\n\n"

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
                    else:
                        print(f"  ⚠️ Unknown tool: {content.name}")

            if not tool_was_called:
                print(f"  ❌ No tool called for part {part_id}. LLM said:")
                for block in response.content:
                    if block.type == "text":
                        print(f"     {block.text[:400]}")

    save_json(table, table_path)
    return {"status": "success", "session_id": session_id}