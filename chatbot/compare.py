from rich.console import Console
from rich.table import Table

from chatbot.llm import generate_response
from constants import PROMPT_STRATEGIES, MODEL_VERSION

console = Console()

STRATEGY_LABELS = {
    "zero_shot": "Zero Shot",
    "few_shot": "Few Shot",
    "cot": "Chain of Thought",
}

def get_loader_msg(strategy):
    return f"[bold cyan]Generating [yellow]{STRATEGY_LABELS[strategy]}[/yellow] response...[/bold cyan]"

def compare_loop(persona, persona_name, model):
    console.print("Chatbot ready. Type '/exit' to quit.")

    while True:
        user = input("You > ")

        if user.startswith("/"):
            if user == "/exit":
                break
        
        console.print(f"[bold cyan]Generating response... Persona: [yellow]{persona_name}[/yellow] Model: [yellow]{MODEL_VERSION[model].value}[/yellow]...[/bold cyan]")
        responses = {}
        for strategy in PROMPT_STRATEGIES:
            loader_msg = get_loader_msg(strategy)
            with console.status(loader_msg, spinner="dots"):
                responses[strategy] = generate_response(
                    user=user,
                    persona=persona,
                    model=model,
                    strategy=strategy,
                    silent=True
                )

        table = Table(title="Prompt Strategy Comparison", header_style="bold magenta", show_lines=True, expand=True)

        for strategy in PROMPT_STRATEGIES:
            table.add_column(STRATEGY_LABELS[strategy], justify="left", ratio=1)

        response_row = []
        stats_row = []
        for strategy in PROMPT_STRATEGIES:
            r = responses[strategy]
            text = r["text"]
            # truncated = text[:300] + "..." if len(text) > 300 else text
            truncated = text
            response_row.append(truncated)
            stats_row.append(f"Input: {r['input_tokens']}\nOutput: {r['output_tokens']}\nLatency:{round(r['latency'], 2)}s")

        table.add_row(*response_row)
        table.add_row(*stats_row)

        console.print(table)
