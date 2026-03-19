import argparse
from rich.console import Console

from chatbot.chat import chat_loop
from config.loader import load_personas
from chatbot.compare import compare_loop
from constants import PERSONA_NAME

console = Console()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--persona", default="tech_support")
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--model", default="ollama")

    args = parser.parse_args()
    personas = load_personas()

    console.print("Available Personas:", style="blue")
    for p in personas:
        console.print("-", p)
    print('\n')

    if args.compare:
        compare_loop(
            persona=personas[args.persona],
            persona_name=PERSONA_NAME[args.persona].value,
            model=args.model
        )
    else:
        chat_loop(
            persona=personas[args.persona],
            persona_name=PERSONA_NAME[args.persona].value,
            compare=args.compare,
            benchmark=args.benchmark,
            model=args.model
        )

if __name__ == "__main__":
    main()
