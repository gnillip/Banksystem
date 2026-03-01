import json

print("Initializing...")
PORT = input("PORT: ")

DATA = {
    "PORT": PORT
}

with open("env.json", "w") as f:
    json.dump(DATA, f, indent=4)