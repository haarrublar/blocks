import os
import anthropic
import json
import uuid
from dotenv import load_dotenv
from aux_functions import save_json, clean_and_load_json
from build.prompts.prompts import BUILD_PROMPT
from build.tools import TOOLS

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def claude_decompose(
    description: str,
    components_table: object,
    all_history: object,
    history_path: str,
    table_path: str,
    player_coordinates: dict,
    session_id: str = None,
):
    context_summary = "### GLOBAL COMPONENTS TABLE (SPATIAL TRUTH):\n"
    context_summary += json.dumps(components_table, indent=2)

    context_summary += "\n\n### SESSION HISTORY (NARRATIVE CONTEXT):\n"
    session_history = all_history.get(session_id, [])
    context_summary += json.dumps(session_history, indent=2)

    context_summary += f"\n\nCURRENT_SESSION: {session_id}"
    context_summary += f"\nPLAYER_COORDS: {player_coordinates}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=BUILD_PROMPT["planner_prompt"],
        messages=[
            {
                "role": "user",
                "content": f"{context_summary}\n\nRequest: {description}",
            }
        ],
    )
    
    try:
        new_parts = clean_and_load_json(response.content[0].text)

        if session_id not in all_history:
            all_history[session_id] = []
        if session_id not in components_table:
            components_table[session_id] = {}

        for part in new_parts:
            part_id = part.get("ID")
            components_table[session_id].setdefault(part_id, [])

            table_entry = {
                "ID": part.get("ID"),
                "Name": part.get("Name"),
                "Shape": part.get("Shape"),
                "Dimensions": part.get("Dimensions"),
                "Material": part.get("Material"),
                "Logic": part.get("Logic"),
                "Status": "PENDING",
                "boundaries": None,
                "Commands": [],
            }
            components_table[session_id][part_id].append(table_entry)

            history_entry = {
                "request": description,
                "part_name": part.get("Name"),
                "timestamp": str(uuid.uuid4()),
            }
            all_history[session_id].append(history_entry)

        save_json(all_history, history_path)
        save_json(components_table, table_path)

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing Planner response: {e}")
        return {"error": "Invalid output format"}

    return {"session_id": session_id, "planned_parts": len(new_parts)}