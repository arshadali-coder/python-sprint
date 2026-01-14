import json
import random
import os

class Storage:
    FILE = "users.json"
    
    @staticmethod
    def load_users():
        if not os.path.exists(Storage.FILE):
            return {}
        with open(Storage.FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_users(users):
        with open(Storage.FILE, "w") as f:
            json.dump(users, f, indent=4)


class User:
    def __init__(self, username, password, wins=0, losses=0, draws=0):
        self.username = username
        self.password = password
        self.wins = wins
        self.losses = losses
        self.draws = draws

    @staticmethod
    def register():
        users = Storage.load_users()
        username = input("Choose username: ")

        if username in users:
            print("❌ Username already exists.")
            return None

        password = input("Choose password: ")
        users[username] = {
            "password": password,
            "wins": 0,
            "losses": 0,
            "draws": 0
        }
        Storage.save_users(users)
        print("✅ Registration successful.")
        return User(username, password)

    @staticmethod
    def login():
        users = Storage.load_users()
        username = input("Username: ")
        password = input("Password: ")

        if username not in users or users[username]["password"] != password:
            print("❌ Invalid credentials.")
            return None

        data = users[username]
        print(f"✅ Welcome back, {username}")
        return User(username, password,
                    data["wins"], data["losses"], data["draws"])

    def save(self):
        users = Storage.load_users()
        users[self.username] = {
            "password": self.password,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws
        }
        Storage.save_users(users)

    def update_stats(self, result):
        if result == "win":
            self.wins += 1
        elif result == "loss":
            self.losses += 1
        else:
            self.draws += 1
        self.save()

class RPSEngine:
    MOVES = ["rock", "paper", "scissors"]

    @staticmethod
    def get_computer_move():
        return random.choice(RPSEngine.MOVES)

    @staticmethod
    def decide(player, computer):
        if player == computer:
            return "draw"
        if (
            (player == "rock" and computer == "scissors") or
            (player == "paper" and computer == "rock") or
            (player == "scissors" and computer == "paper")
        ):
            return "win"
        return "loss"


class GameSession:
    def __init__(self, user):
        self.user = user
        self.engine = RPSEngine()

    def play(self):
        rounds = int(input("Enter number of rounds: "))
        score = {"win": 0, "loss": 0, "draw": 0}

        for r in range(1, rounds + 1):
            print(f"\nRound {r}")
            player_move = input("Choose rock/paper/scissors: ").lower()

            if player_move not in RPSEngine.MOVES:
                print("❌ Invalid move.")
                continue

            computer_move = self.engine.get_computer_move()
            result = self.engine.decide(player_move, computer_move)

            print(f"🧠 Computer chose: {computer_move}")
            print(f"🎯 Result: {result.upper()}")

            score[result] += 1

        print("\n🏁 Match Result")
        print(score)

        if score["win"] > score["loss"]:
            self.user.update_stats("win")
            print("🏆 You WON the match!")
        elif score["loss"] > score["win"]:
            self.user.update_stats("loss")
            print("💀 You LOST the match!")
        else:
            self.user.update_stats("draw")
            print("🤝 Match DRAW!")


def main():
    print("🎮 Rock Paper Scissors CLI")

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Select option: ")

        if choice == "1":
            user = User.register()
        elif choice == "2":
            user = User.login()
        elif choice == "3":
            print("👋 Bye!")
            break
        else:
            print("❌ Invalid choice.")
            continue

        if user:
            session = GameSession(user)
            session.play()


if __name__ == "__main__":
    main()