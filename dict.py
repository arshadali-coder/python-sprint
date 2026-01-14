dict ={
    "Arshad Ali": {
        "password": "1",
        "wins": 0,
        "losses": 1,
        "draws": 0
    },
    "karthik": {
        "password": "17yrs",
        "wins": 0,
        "losses": 2,
        "draws": 1
    }
}

for name in dict:
    print(f"Username: {name}, Password: {dict[name]['password']}")
    print(f"Wins: {dict[name]['wins']}, Losses: {dict[name]['losses']}, Draws: {dict[name]['draws']}")