import anthropic
import traceback
import os, sys
import json
import uuid
from dotenv import load_dotenv

from deconstruction import claude_decompose
from architect import claude_architect
from aux_functions import load_json, save_json
from build.prompts.prompts import BUILD_PROMPT
from build.tools import TOOLS
from build.build_rectangle import build_rectangle
from build.build_cylinder import build_cylinder




load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PLAYER_COORDS = {"x": -20, "y": -61, "z": -195}
HISTORY_FILE = "./build/session/session.json"
TABLE_FILE = "./build/session/components_table.json"



def build_claude(description: str, player_coordinates: dict, session_id: str = None, all_sessions: dict = None):
    
    all_history = load_json(HISTORY_FILE)
    components_table = load_json(TABLE_FILE)     
    
    if "reset" in description:
        # 1. Force a brand new ID
        session_id = str(uuid.uuid4())
        # 2. CLEAR the history for this specific call so the LLM starts fresh
        current_context_history = {} 
        print(f"🧹 Reset detected. Starting fresh session: {session_id}")
    else:
        # Use existing logic
        if not session_id:
            session_id = list(all_sessions.keys())[-1] if all_sessions else str(uuid.uuid4())
        current_context_history = all_history
    
    
    claude_decompose(
        description= description, 
        components_table= components_table, 
        all_history= all_history, 
        history_path= HISTORY_FILE, 
        table_path= TABLE_FILE, 
        player_coordinates= PLAYER_COORDS, 
        session_id= session_id
    )
    
    claude_architect(
        session_id=session_id, 
        table_path=TABLE_FILE,
        player_coordinates=PLAYER_COORDS
    )

    
    

    
    
    
    
    

    # reasoning = ""
    # all_commands = []
    # final_bounds = {}
    # BUILDERS = {"build_rectangle": build_rectangle, "build_cylinder": build_cylinder}

    # for content in response.content:
    #     if content.type == "text":
    #         reasoning += content.text
    #     elif content.type == "tool_use":
    #         args = content.input 
            
    #         result = BUILDERS[content.name](**args)
    #         all_commands.extend(result["commands"])
    #         final_bounds = result["bounds"]

    # new_entry = {
    #     "building_id": description.split('.')[0][:20], 
    #     "request": description,
    #     "reasoning": reasoning.strip(),
    #     "bounds": final_bounds,
    #     "commands": all_commands
    # }
    
    # if session_id not in all_sessions:
    #     all_sessions[session_id] = []
    # all_sessions[session_id].append(new_entry)
    
    
    # save_all_sessions(all_sessions)
    # export_blueprint_to_md(session_id, all_sessions)

    # return {
    #     "llm_reasoning": reasoning, 
    #     "action_payload": "\n".join(all_commands), 
    #     "session_id": session_id
    # }

if __name__ == "__main__":
    all_sessions = load_json(HISTORY_FILE)
    
    if all_sessions:
        active_id = list(all_sessions.keys())[-1]
        print(f"🔄 Continuing existing session: {active_id}")
    else:
        active_id = str(uuid.uuid4())
        print(f"🆕 Starting brand new session: {active_id}")
    
    test_request = """ reset.
Build an L-shape building of heigth 8 blocks. Make it hollow and without ceiling. Additionally to not make any shared walls. The longer side make it three times longer than the shorter. The shorter make it 10 blocks width. Make it yellow and the inner width make it 8 blocks.
    """
    
    print(f"--- 🏗️ Starting Architect Test ---")
    print(f"Player Position: {PLAYER_COORDS}")
    print(f"Request: {test_request}\n")

    try:

        result = build_claude(description=test_request, player_coordinates=PLAYER_COORDS, session_id=active_id, all_sessions=all_sessions)
        print(f"🤔 Reasoning: {result['llm_reasoning']}")
        print(f"📜 Commands: {result['action_payload']}")
        traceback.print_exc(file=sys.stdout)
    except Exception as e:
        print(f"💥 Test Failed: {e}")
        traceback.print_exc(file=sys.stdout)