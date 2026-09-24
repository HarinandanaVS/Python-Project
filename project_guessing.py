import random
import time
import os

class Player:
    def __init__(self, name, score=0, games_played=0):
        self.name = name
        self.score = int(score)
        self.games_played = int(games_played)

class Championship:
    def __init__(self):
        self.leaderboard = {}
        self.load_leaderboard()

    def load_leaderboard(self):
        if os.path.exists("leaderboard.txt"):
            with open("leaderboard.txt", "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 3:
                        self.leaderboard[data[0]] = Player(data[0], data[1], data[2])

    def save_leaderboard(self):
        with open("leaderboard.txt", "w") as file:
            for p in self.leaderboard.values():
                file.write(f"{p.name},{p.score},{p.games_played}\n")

    def display_rules(self):
        print("\n--- Game Rules ---")
        print("1. Guess the secret number within your attempt limit.")
        print("2. 10 points are deducted for every incorrect attempt.")
        print("3. A bonus 50 points are awarded if you guess correctly in under 15 seconds.")
        print("4. Zero points are awarded if you run out of attempts.")
        
    def show_leaderboard(self):
        print("\n--- Leaderboard ---")
        if not self.leaderboard:
            print("No scores recorded yet.")
        else:
            sorted_players = sorted(self.leaderboard.values(), key=lambda x: x.score, reverse=True)
            for idx, p in enumerate(sorted_players):
                print(f"{idx+1}. {p.name} | Total Score: {p.score} | Games Played: {p.games_played}")

    def search_player(self, name):
        if name in self.leaderboard:
            p = self.leaderboard[name]
            print(f"\nPlayer: {p.name} | Total Score: {p.score} | Games Played: {p.games_played}")
        else:
            print("\nPlayer not found.")

    def start_game(self):
        while True:
            num_players = input("\nEnter number of players (2-5): ")
            if num_players.isdigit() and 2 <= int(num_players) <= 5:
                num_players = int(num_players)
                break
            print("Invalid input. Please enter a number between 2 and 5.")

        current_players = []
        for i in range(num_players):
            while True:
                name = input(f"Enter name for Player {i+1}: ")
                if name not in current_players:
                    current_players.append(name)
                    if name not in self.leaderboard:
                        self.leaderboard[name] = Player(name)
                    break
                print("Name already taken in this session. Choose another.")

        print("\nDifficulty Levels: Easy (1-50), Medium (1-100), Hard (1-500)")
        while True:
            diff = input("Choose difficulty (Easy/Medium/Hard): ").capitalize()
            if diff in ["Easy", "Medium", "Hard"]:
                break
            print("Invalid difficulty.")

        if diff == "Easy":
            max_num = 50
            max_attempts = 5
        elif diff == "Medium":
            max_num = 100
            max_attempts = 7
        else:
            max_num = 500
            max_attempts = 10

        secret_number = random.randint(1, max_num)
        random.shuffle(current_players)
        
        print(f"\nGame starting! The secret number is between 1 and {max_num}.")
        print(f"Turn order: {', '.join(current_players)}")

        game_active = True
        attempts_tracker = {name: 0 for name in current_players}
        start_time = time.time()

        while game_active:
            for name in current_players:
                if attempts_tracker[name] >= max_attempts:
                    continue

                print(f"\n{name}'s turn (Attempt {attempts_tracker[name]+1}/{max_attempts}):")
                
                while True:
                    guess = input("Enter your guess: ")
                    if guess.isdigit():
                        guess = int(guess)
                        break
                    print("Invalid input. Please enter a number.")

                attempts_tracker[name] += 1
                time_taken = time.time() - start_time

                if guess == secret_number:
                    print(f"\nCorrect, {name}! You found the number.")
                    game_active = False
                    
                    points = 100 - (attempts_tracker[name] * 10)
                    if time_taken < 15:
                        print("Speed Bonus! +50 points.")
                        points += 50
                    
                    self.leaderboard[name].score += points
                    break
                else:
                    diff_val = abs(secret_number - guess)
                    if diff_val <= 5:
                        print("Very Close!")
                    elif guess < secret_number:
                        print("Too Low!")
                    else:
                        print("Too High!")

            if all(attempts_tracker[n] >= max_attempts for n in current_players) and game_active:
                print(f"\nOut of attempts! The secret number was {secret_number}.")
                game_active = False

        for name in current_players:
            self.leaderboard[name].games_played += 1

        self.save_leaderboard()

if __name__ == "__main__":
    game = Championship()
    while True:
        print("\n" + "="*40)
        print("🏆 NUMBER GUESSING CHAMPIONSHIP 🏆")
        print("="*40)
        print("1. Start New Game")
        print("2. Display Rules")
        print("3. Show Leaderboard")
        print("4. Search Player Statistics")
        print("5. Exit")
        print("="*40)
        choice = input("Enter your choice: ")
        if choice == '1':
            game.start_game()
        elif choice == '2':
            game.display_rules()
        elif choice == '3':
            game.show_leaderboard()
        elif choice == '4':
            name = input("Enter player name to search: ")
            game.search_player(name)
        elif choice == '5':
            game.save_leaderboard()
            print("Exiting. Thanks for playing!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")
