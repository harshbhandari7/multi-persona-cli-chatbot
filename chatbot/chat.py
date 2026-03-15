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
         
        console.print("Bot >", style="bold green", end=" ")
        response = generate_response(
            user=user, 
            history=history, 
            persona=persona,
            model="ollama"
        )

        history.append({"role": "assistant", "content": response["text"]})

        # console.print(response['text'])
        console.print()
        console.print(
            f"Input tokens: {response["input_tokens"]} | Thought tokens: {response["thought_tokens"]} | Output tokens: { response['output_tokens']} | latency: {response['latency']:.2f}s",
            style="bold red"
        )
        print("\n\n ------------------------------------------------------------------------------------ \n\n")
        
        log_event({
            "persona": persona,
            "prompt": user,
            "response": response
        })





