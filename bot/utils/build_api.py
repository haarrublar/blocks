import anthropic
import os
import json
import uuid
from dotenv import load_dotenv
from build.prompts.prompts import BUILD_PROMPT
from build.tools import TOOLS
from build.build_rectangle import build_rectangle
from build.build_cylinder import build_cylinder


load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PLAYER_COORDS = {"x": -493, "y": 65, "z": 91}
HISTORY_FILE = "./build/session/session.json"

def load_all_sessions():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_all_sessions(all_sessions):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(all_sessions, f, indent=4)

def ask_claude_build(description: str, session_id: str = None, all_sessions: dict = None):
    if all_sessions is None:
        all_sessions = load_all_sessions()
    
    if not session_id:
        session_id = list(all_sessions.keys())[-1] if all_sessions else str(uuid.uuid4())

    log_entries = all_sessions.get(session_id, [])

    if not log_entries:
        context_summary = f"Project Start. Initial Player Location: {PLAYER_COORDS}\n"
    else:
        context_summary = "Project Status: Continuing build. Use the Building Log bounds for alignment.\n"
        for entry in log_entries:
            context_summary += f"- Task: {entry['request']}\n  Bounds: {entry['bounds']}\n"

    full_prompt = f"{context_summary}\nNew Request: {description}"
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        tools=TOOLS,
        system=BUILD_PROMPT["system_prompt"],
        messages=[{"role": "user", "content": full_prompt}]
    )

    reasoning = ""
    all_commands = []
    final_bounds = {}
    BUILDERS = {"build_rectangle": build_rectangle, "build_cylinder": build_cylinder}

    for content in response.content:
        if content.type == "text":
            reasoning += content.text
        elif content.type == "tool_use":
            args = content.input 
            
            result = BUILDERS[content.name](**args)
            all_commands.extend(result["commands"])
            final_bounds = result["bounds"]

    new_entry = {
        "request": description,
        "reasoning": reasoning.strip(),
        "bounds": final_bounds,
        "commands": all_commands
    }
    
    if session_id not in all_sessions:
        all_sessions[session_id] = []
    all_sessions[session_id].append(new_entry)
    save_all_sessions(all_sessions)

    return {
        "llm_reasoning": reasoning, 
        "action_payload": "\n".join(all_commands), 
        "session_id": session_id
    }

if __name__ == "__main__":
    # 1. LOAD existing sessions from the JSON file first
    all_sessions = load_all_sessions()
    
    # 2. DECIDE: Do you want to continue the last session or start new?
    # Logic: If sessions exist, use the most recent key. Otherwise, new ID.
    if all_sessions:
        active_id = list(all_sessions.keys())[-1]
        print(f"🔄 Continuing existing session: {active_id}")
    else:
        active_id = str(uuid.uuid4())
        print(f"🆕 Starting brand new session: {active_id}")
    
    test_request = "from the blue cube you build now build a red cylinder on top of it. make it hollow false and the radius 2, it can be 4 blockk height"
    
    print(f"--- 🏗️ Starting Architect Test ---")
    print(f"Player Position: {PLAYER_COORDS}")
    print(f"Request: {test_request}\n")

    try:
        # 3. PASS the existing dictionary and the active ID
        # This ensures 'history = all_sessions.get(session_id, [])' finds the old messages
        result = ask_claude_build(test_request, active_id, all_sessions)
        
        print(f"🤔 Reasoning: {result['llm_reasoning']}")
        print(f"📜 Commands: {result['action_payload']}")
    except Exception as e:
        print(f"💥 Test Failed: {e}")