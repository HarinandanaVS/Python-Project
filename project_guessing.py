import random
import time
import json
import os


LEADERBOARD_FILE = "leaderboard.json"


# --------------------------------------------------
# Player Class
# --------------------------------------------------

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.attempts = 0
        self.games_played = 0
        self.games_won = 0
        self.total_time = 0
        self.best_score = 0

    def update_statistics(self, score, attempts, time_taken):
        self.score = score
        self.attempts = attempts
        self.games_played += 1
        self.total_time += time_taken

        if score > 0:
            self.games_won += 1

        if score > self.best_score:
            self.best_score = score

    def to_dictionary(self):
        return {
            "name": self.name,
            "score": self.score,
            "attempts": self.attempts,
            "games_played": self.games_played,
            "games_won": self.games_won,
            "total_time": self.total_time,
            "best_score": self.best_score
        }

    @staticmethod
    def from_dictionary(data):
        player = Player(data["name"])
        player.score = data.get("score", 0)
        player.attempts = data.get("attempts", 0)
        player.games_played = data.get("games_played", 0)
        player.games_won = data.get("games_won", 0)
        player.total_time = data.get("total_time", 0)
        player.best_score = data.get("best_score", 0)
        return player


# --------------------------------------------------
# Load and Save Leaderboard
# --------------------------------------------------

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as file:
                data = json.load(file)

            return {
                name: Player.from_dictionary(details)
                for name, details in data.items()
            }

        except (json.JSONDecodeError, KeyError):
            print("Leaderboard file is invalid. Starting with an empty leaderboard.")

    return {}


def save_leaderboard(leaderboard):
    data = {
        name: player.to_dictionary()
        for name, player in leaderboard.items()
    }

    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)


# --------------------------------------------------
# Display Rules
# --------------------------------------------------

def display_rules():
    print("\n" + "=" * 55)
    print("              GAME RULES")
    print("=" * 55)
    print("1. The game supports 2 to 5 players.")
    print("2. Every player must have a unique name.")
    print("3. Players take turns in a randomized order.")
    print("4. Each player receives a limited number of attempts.")
    print("5. Correct guesses earn points.")
    print("6. Incorrect guesses reduce points.")
    print("7. Quick correct guesses receive a time bonus.")
    print("8. A player gets zero points if all attempts are used.")
    print("9. The leaderboard is saved after every game.")
    print("=" * 55)


# --------------------------------------------------
# Difficulty Selection
# --------------------------------------------------

def choose_difficulty():
    difficulties = {
        "1": ("Easy", 1, 50, 5, 100),
        "2": ("Medium", 1, 100, 4, 150),
        "3": ("Hard", 1, 500, 3, 250)
    }

    while True:
        print("\nChoose Difficulty:")
        print("1. Easy   (1-50, 5 attempts)")
        print("2. Medium (1-100, 4 attempts)")
        print("3. Hard   (1-500, 3 attempts)")

        choice = input("Enter your choice: ").strip()

        if choice in difficulties:
            return difficulties[choice]

        print("Invalid difficulty choice. Please select 1, 2, or 3.")


# --------------------------------------------------
# Get Players
# --------------------------------------------------

def get_players(leaderboard):
    while True:
        try:
            count = int(input("\nEnter number of players (2-5): "))

            if count < 2 or count > 5:
                print("Please enter a number between 2 and 5.")
                continue

            break

        except ValueError:
            print("Invalid input. Please enter a number.")

    players = []
    names_used = set()

    for i in range(count):
        while True:
            name = input(f"Enter name for Player {i + 1}: ").strip()

            if not name:
                print("Name cannot be empty.")
                continue

            # Case-insensitive duplicate checking
            name_key = name.lower()

            if name_key in names_used:
                print("Duplicate name in this game. Choose another name.")
                continue

            names_used.add(name_key)

            # Reuse previous statistics if the name exists
            existing_player = None

            for saved_name, saved_player in leaderboard.items():
                if saved_name.lower() == name_key:
                    existing_player = saved_player
                    break

            if existing_player:
                player = existing_player
                print(f"Welcome back, {player.name}!")
            else:
                player = Player(name)
                leaderboard[name] = player

            players.append(player)
            break

    return players


# --------------------------------------------------
# Generate Hint
# --------------------------------------------------

def get_hint(guess, secret_number):
    difference = abs(guess - secret_number)

    if difference <= 5:
        return "Very Close!"

    if guess < secret_number:
        return "Too Low!"

    return "Too High!"


# --------------------------------------------------
# Calculate Score
# --------------------------------------------------

def calculate_score(base_points, attempts_used, time_taken):
    # Penalty: 20 points for every incorrect attempt
    penalty = (attempts_used - 1) * 20

    # Time bonus for answering quickly
    if time_taken <= 5:
        time_bonus = 50
    elif time_taken <= 10:
        time_bonus = 25
    else:
        time_bonus = 0

    score = base_points - penalty + time_bonus

    return max(score, 0)


# --------------------------------------------------
# Play One Player's Turn
# --------------------------------------------------

def play_turn(player, secret_number, max_attempts, base_points, lower, upper):
    print(f"\n{'-' * 50}")
    print(f"{player.name}'s Turn")
    print(f"You have {max_attempts} attempts.")
    print(f"Guess a number between {lower} and {upper}.")
    print(f"{'-' * 50}")

    attempts_used = 0
    start_time = time.time()
    correct = False

    while attempts_used < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts_used + 1}: "))

            if guess < lower or guess > upper:
                print(f"Please enter a number between {lower} and {upper}.")
                continue

        except ValueError:
            print("Invalid guess. Please enter a numeric value.")
            continue

        attempts_used += 1

        if guess == secret_number:
            correct = True
            time_taken = time.time() - start_time
            score = calculate_score(
                base_points,
                attempts_used,
                time_taken
            )

            print("\nCorrect guess!")
            print(f"Time taken: {time_taken:.2f} seconds")
            print(f"Points earned: {score}")

            return score, attempts_used, time_taken

        # Penalty information
        current_penalty = attempts_used * 20
        print(get_hint(guess, secret_number))
        print(f"Penalty applied: {current_penalty} points")

    # Player failed to guess correctly
    time_taken = time.time() - start_time

    print("\nYou have used all your attempts.")
    print(f"The secret number was: {secret_number}")
    print("Points earned: 0")

    return 0, attempts_used, time_taken


# --------------------------------------------------
# Start New Game
# --------------------------------------------------

def start_new_game(leaderboard):
    print("\n" + "=" * 55)
    print("          MULTIPLAYER NUMBER GUESSING")
    print("              CHAMPIONSHIP")
    print("=" * 55)

    players = get_players(leaderboard)

    difficulty, lower, upper, max_attempts, base_points = choose_difficulty()

    secret_number = random.randint(lower, upper)

    # Randomize player turn order
    random.shuffle(players)

    print(f"\nDifficulty selected: {difficulty}")
    print("Player order has been randomized!")
    print("Let the championship begin!")

    results = []

    for player in players:
        score, attempts, time_taken = play_turn(
            player,
            secret_number,
            max_attempts,
            base_points,
            lower,
            upper
        )

        player.update_statistics(score, attempts, time_taken)

        results.append({
            "name": player.name,
            "score": score,
            "attempts": attempts,
            "time": time_taken
        })

    # Save after every completed game
    save_leaderboard(leaderboard)

    display_game_results(results)
    display_leaderboard(leaderboard)


# --------------------------------------------------
# Display Game Results
# --------------------------------------------------

def display_game_results(results):
    print("\n" + "=" * 60)
    print("                 GAME RESULTS")
    print("=" * 60)

    sorted_results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    for position, result in enumerate(sorted_results, start=1):
        print(
            f"{position}. {result['name']:<15} "
            f"Score: {result['score']:<5} "
            f"Attempts: {result['attempts']:<3} "
            f"Time: {result['time']:.2f}s"
        )

    if sorted_results:
        winner = sorted_results[0]
        print(f"\n🏆 Winner: {winner['name']}!")
        print(f"Winning score: {winner['score']}")

    print("=" * 60)


# --------------------------------------------------
# Display Leaderboard
# --------------------------------------------------

def display_leaderboard(leaderboard):
    print("\n" + "=" * 75)
    print("                     PERSISTENT LEADERBOARD")
    print("=" * 75)

    if not leaderboard:
        print("No leaderboard records available.")
        print("=" * 75)
        return

    players = sorted(
        leaderboard.values(),
        key=lambda player: (
            player.best_score,
            player.games_won,
            -player.total_time
        ),
        reverse=True
    )

    print(
        f"{'Rank':<6}{'Player':<18}{'Best Score':<13}"
        f"{'Games':<10}{'Wins':<10}{'Avg Time'}"
    )
    print("-" * 75)

    for rank, player in enumerate(players, start=1):
        if player.games_played > 0:
            average_time = player.total_time / player.games_played
        else:
            average_time = 0

        print(
            f"{rank:<6}{player.name:<18}{player.best_score:<13}"
            f"{player.games_played:<10}{player.games_won:<10}"
            f"{average_time:.2f}s"
        )

    print("=" * 75)


# --------------------------------------------------
# Search Player Statistics
# --------------------------------------------------

def search_player_statistics(leaderboard):
    if not leaderboard:
        print("\nNo player statistics available.")
        return

    name = input("\nEnter player name to search: ").strip()

    found_player = None

    for saved_name, player in leaderboard.items():
        if saved_name.lower() == name.lower():
            found_player = player
            break

    if found_player is None:
        print("Player not found.")
        return

    player = found_player

    print("\n" + "=" * 45)
    print(f"       STATISTICS: {player.name}")
    print("=" * 45)
    print(f"Current Score  : {player.score}")
    print(f"Best Score     : {player.best_score}")
    print(f"Games Played   : {player.games_played}")
    print(f"Games Won      : {player.games_won}")
    print(f"Last Attempts  : {player.attempts}")
    print(f"Total Time     : {player.total_time:.2f} seconds")

    if player.games_played > 0:
        print(
            f"Average Time   : "
            f"{player.total_time / player.games_played:.2f} seconds"
        )

    print("=" * 45)


# --------------------------------------------------
# Main Menu
# --------------------------------------------------

def main():
    leaderboard = load_leaderboard()

    while True:
        print("\n" + "=" * 55)
        print("       MULTIPLAYER NUMBER GUESSING CHAMPIONSHIP")
        print("=" * 55)
        print("1. Start New Game")
        print("2. Display Rules")
        print("3. Show Leaderboard")
        print("4. Search Player Statistics")
        print("5. Exit")
        print("=" * 55)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            start_new_game(leaderboard)

        elif choice == "2":
            display_rules()

        elif choice == "3":
            display_leaderboard(leaderboard)

        elif choice == "4":
            search_player_statistics(leaderboard)

        elif choice == "5":
            save_leaderboard(leaderboard)
            print("\nThank you for playing!")
            print("Leaderboard saved successfully.")
            break

        else:
            print("Invalid choice. Please select 1-5.")


# --------------------------------------------------
# Program Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    main()