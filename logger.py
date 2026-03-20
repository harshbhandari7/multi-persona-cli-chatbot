import json
import time

def log_event(data, path="logs/conversations.jsonl"):
    data["timestamp"] = time.time()

    with open(path, "a") as f:
        f.write(json.dumps(data) + "\n")
