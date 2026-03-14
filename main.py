import argparse
from chatbot.chat import chat_loop
from config.loader import load_personas
from rich.console import Console

console = Console()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--persona", default="tech_support")
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--benchmark", action="store_true")

    args = parser.parse_args()
    personas = load_personas()

    console.print("Available Personas:", style="blue")
    for p in personas:
        console.print("-", p)
    print('\n')
    chat_loop(
        persona=personas[args.persona],
        compare=args.compare,
        benchmark=args.benchmark
    )

if __name__ == "__main__":
    main()
