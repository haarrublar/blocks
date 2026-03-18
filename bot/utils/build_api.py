import anthropic
import os
from prompts_second import BUILD_PROMPT
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_claude_build(description: str, offset_x: int = 3, offset_z: int = 4):
    # === 1. PLANNING STEP (rethink + logical layout) ===
    plan_prompt = BUILD_PROMPT["plan_prompt"].format(description=description)
    
    plan_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        temperature=0.2,
        system="You are a realistic Minecraft base designer.",
        messages=[{"role": "user", "content": plan_prompt}]
    )
    
    plan = plan_response.content[0].text.strip()
    print("\n=== INTERNAL PLAN (what the AI is thinking) ===")
    print(plan)
    print("=" * 50)

    # === 2. BUILD COMMANDS using the plan ===
    build_user = f"Plan:\n{plan}\n\nStart house around ~{offset_x} ~0 ~{offset_z}"

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        temperature=0.1,
        system=BUILD_PROMPT["main_prompt"].format(plan=plan),
        messages=[{"role": "user", "content": build_user}]
    )

    raw = response.content[0].text.strip()
    commands = [line.strip() for line in raw.splitlines() if line.strip().startswith("/")]
    return commands


# TEST MODE
if __name__ == "__main__":
    print("=== Minecraft Build Tester (Planner + Builder) ===")
    print("Now with logical layouts!\n")
    
    try:
        while True:
            description = input("> ").strip()
            if not description:
                continue

            print("\nPlanning + building...\n")
            commands = ask_claude_build(description)

            print("--- FINAL COMMANDS (copy-paste ready) ---")
            for cmd in commands:
                print(cmd)
            print("-" * 60)

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")