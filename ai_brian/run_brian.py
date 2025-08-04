#SoulTrak/ai_brain/run_brian

from .csvpln import generate_output
from .prompt_templates import PROMPT_OPTIONS

def run_planner(prompt_key="Daily Feedback"):
    if prompt_key not in PROMPT_OPTIONS:
        raise ValueError("Invalid prompt key.")
    selected_prompt = PROMPT_OPTIONS[prompt_key]
    return generate_output(selected_prompt)

def main():
    print("\n🤖 Welcome to SoulTrak AI Planner")
    print("Choose a prompt to run:")
    for i, key in enumerate(PROMPT_OPTIONS.keys(), 1):
        print(f"{i}. {key}")

    choice = input("Enter 1–5: ")
    keys = list(PROMPT_OPTIONS.keys())

    if choice not in map(str, range(1, len(keys)+1)):
        print("❌ Invalid choice.")
        return

    selected_key = keys[int(choice) - 1]
    print(f"\n💬 Generating feedback using prompt: {selected_key}...\n")
    response = run_planner(prompt_key=selected_key)
    print(response)

if __name__ == "__main__":
    main()
