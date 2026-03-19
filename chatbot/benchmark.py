from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table

from chatbot.llm import generate_response
from constants import MODEL_VERSION, TOKEN_PRICING

console = Console()


# removing deepseek and openai temporarily
# ALL_MODELS = [m.name for m in MODEL_VERSION]
ALL_MODELS = [m.name for m in MODEL_VERSION if m.name != "deepseek" and m.name != "openai"]

def calculate_cost(model, input_tokens, output_tokens):
    input_price, output_price = TOKEN_PRICING.get(model, (0.0, 0.0))
    return (input_tokens * input_price + output_tokens * output_price) / 1_000_000

def benchmark_loop(persona, persona_name, model):
    console.print("Benchmark mode. Type '/exit' to quit.")

    while True:
        user = input("You > ")

        if user.startswith("/"):
            if user == "/exit":
                break

        console.print(
            f"[bold cyan]Benchmarking across all models — Persona: [yellow]{persona_name}[/yellow]...[/bold cyan]"
        )

        results = {}
        with console.status("[bold cyan]Running all models concurrently...[/bold cyan]", spinner="dots"):
            with ThreadPoolExecutor(max_workers=len(ALL_MODELS)) as executor:
                futures = {
                    executor.submit(
                        generate_response,
                        user=user,
                        persona=persona,
                        model=m,
                        silent=True
                    ): m
                    for m in ALL_MODELS
                }
                for future in as_completed(futures):
                    m = futures[future]
                    results[m] = future.result()

        table = Table(
            title=f"Model Benchmark - {persona_name}",
            header_style="bold magenta",
            show_lines=True,
            expand=True
        )

        for m in ALL_MODELS:
            table.add_column(MODEL_VERSION[m].value, justify="left", ratio=1)

        response_row = []
        stats_row = []
        for m in ALL_MODELS:
            r = results[m]
            text = r["text"]
            # truncated = text[:300] + "..." if len(text) > 300 else text
            response_row.append(text)

            cost = calculate_cost(m, r["input_tokens"], r["output_tokens"])
            cost_str = f"~${cost:.5f}"
            stats_row.append(
                f"in: {r['input_tokens']}\nout: {r['output_tokens']}\n"
                f"{round(r['latency'], 2)}s\n{cost_str}"
            )

        table.add_row(*response_row)
        table.add_row(*stats_row)

        console.print(table)
