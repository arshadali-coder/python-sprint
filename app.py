import json

with open("data.json", "r") as f:
    data = json.load(f)

print(data["users"]["arshad"]["wins"])