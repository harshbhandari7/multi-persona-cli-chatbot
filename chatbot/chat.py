from rich.console import Console
from chatbot.llm import generate_response
from logger import log_event


console = Console()

def chat_loop(persona, compare, benchmark):
    console.print("Chatbot ready. Type '/exit' to quit.")

    history = []
    
    while True:
        user = input("You > ")
        
        if user.startswith("/"):
            if user == "/clear":
                history = []
                console.print("History cleared", style="yellow bold")
                continue
            if user == "/exit":
                break
        

        history.append({"role": "user", "content": user})
         
        response = generate_response(user=user, history=history, persona=persona)

        history.append({"role": "assistant", "content": response["text"]})

        print("\n------------------------------\n")
        console.print("Bot >", style="bold green", end=" ")
        console.print(response['text'])

        console.print(
            f"[dim]tokens: {response["input_tokens"]} -> { response['output_tokens']} \
            | latency: {response['latency']:.2f}s [/dim]",
            style="bold red"
        )

        log_event({
            "persona": persona,
            "prompt": user,
            "response": response
        })





