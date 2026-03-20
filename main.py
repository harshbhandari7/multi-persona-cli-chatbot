import argparse
from rich.console import Console

from chatbot.chat import chat_loop
from config.loader import load_personas
from chatbot.compare import compare_loop
from constants import PERSONA_NAME
from chatbot.benchmark import benchmark_loop

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

    valid_personas = list(personas.keys())
    if args.persona not in personas or args.persona not in PERSONA_NAME.__members__:
        console.print(
            f"[bold red]Error:[/bold red] Unknown persona '[yellow]{args.persona}[/yellow]'. "
            f"Valid options: {', '.join(valid_personas)}",
            style="red"
        )
        return

    if args.compare:
        compare_loop(
            persona=personas[args.persona],
            persona_name=PERSONA_NAME[args.persona].value,
            model=args.model
        )
    elif args.benchmark:
        benchmark_loop(
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
