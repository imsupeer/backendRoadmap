import random
import time

HIGH_SCORES = {"Easy": None, "Medium": None, "Hard": None}

DIFFICULTY_LEVELS = {"1": ("Easy", 10), "2": ("Medium", 5), "3": ("Hard", 3)}


def choose_difficulty():
    print("Please select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")
    choice = input("Enter your choice: ").strip()
    while choice not in DIFFICULTY_LEVELS:
        print("Invalid choice. Please select 1, 2 or 3.")
        choice = input("Enter your choice: ").strip()
    level, chances = DIFFICULTY_LEVELS[choice]
    print(
        f"\nGreat! You have selected the {level} difficulty level. You have {chances} chances."
    )
    return level, chances


def play_round():
    level, chances = choose_difficulty()
    target = random.randint(1, 100)
    attempt_count = 0
    start_time = time.time()
    won = False

    while attempt_count < chances:
        guess_str = input("\nEnter your guess: ").strip()
        try:
            guess = int(guess_str)
        except ValueError:
            print("Please enter a valid integer.")
            continue
        attempt_count += 1

        if guess == target:
            elapsed = time.time() - start_time
            print(
                f"\nCongratulations! You guessed the correct number in {attempt_count} attempts in {elapsed:.2f} seconds."
            )
            won = True
            if HIGH_SCORES[level] is None or attempt_count < HIGH_SCORES[level]:
                HIGH_SCORES[level] = attempt_count
                print(f"New high score for {level} difficulty!")
            break
        elif guess < target:
            print(f"Incorrect! The number is greater than {guess}.")
        else:
            print(f"Incorrect! The number is less than {guess}.")

    if not won:
        print(f"\nYou ran out of chances. The correct number was {target}.")


def main():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    play_again = "y"
    while play_again.lower() == "y":
        play_round()
        play_again = input("\nDo you want to play again? (y/n): ").strip()
    print("\nThank you for playing! Goodbye.")


if __name__ == "__main__":
    main()
