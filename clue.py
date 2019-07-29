import random
import os
import pickle
from cs50 import get_string
from termcolor import colored

# canonical list of cards
SUSPECTS = {"Mr. Green","Colonel Mustard","Mrs. Peacock","Professor Plum","Mrs. White"}
WEAPONS = {"candlestick","dagger","lead pipe","revolver","rope","wrench"}
ROOMS = {"ballroom","billiard room","conservatory","dining room","hall","kitchen", "library","lounge","study"}
ALL_CARDS = SUSPECTS|WEAPONS|ROOMS

# how many cards each player gets
CARDS_PER_PERSON = [7,7,6]

def main():
    """ allows playing of 2-person clue. quits when game() returns false"""
    while True:
        if not game():
            break

def game():
    """ implements functionality of clue game"""
    # determine players' cards, either randomly or by recovering previous game
    while True:
        answer = get_string("Type 'recover' to recover last game's cards, or 'random' to get random cards: ")
        if answer == "recover":
            try:
                # load previous game data
                with open("prev_game.p","rb") as file:
                    gameData = pickle.load(file)
                    guilty = gameData["guilty"]
                    players = gameData["players"]
                    player0 = gameData["player0"]
                    player1 = gameData["player1"]
                    computerCards = gameData["computerCards"]
            except Exception as e:
                print(colored("Unable to load previous game data","red"))
                raise e
                return False
            break
        elif answer == "random":
            # make dictionary for players
            players = dict()

            # get player names
            os.system("clear")
            player0 = get_string("Player 0 name: ")
            player1 = get_string("Player 1 name: ")
            os.system("clear")

            # make list of cards to play with
            suspects, weapons, rooms = list(SUSPECTS), list(WEAPONS), list(ROOMS)

            # shuffle cards
            random.shuffle(suspects)
            random.shuffle(weapons)
            random.shuffle(rooms)

            # determine winning combination
            guilty = {suspects.pop(), weapons.pop(), rooms.pop()}

            # give players cards
            allCards = suspects + weapons + rooms
            random.shuffle(allCards)
            players[player0] = {allCards.pop() for _ in range(CARDS_PER_PERSON[0])}
            players[player1] = {allCards.pop() for _ in range(CARDS_PER_PERSON[1])}
            computerCards = set(allCards)

            # save data in case we need to recover it
            with open("prev_game.p","wb") as file:
                pickle.dump({"players":players,"guilty":guilty,"player0":player0,"player1":player1,"computerCards":computerCards}, file)

            break
    # reveal players' cards
    show_cards(player0, players)
    show_cards(player1, players)

    # implement gameplay
    while True:
        print(colored("Enter your desired action:\n[l]ist all cards\n[d]isplay a player's cards\n[s]uspect\n[a]ccuse\n[r]estart\n[q]uit\nshow [p]layers' names\nreveal [c]orrect answer\n","yellow"))
        action = get_string("Action: ")
        os.system("clear")
        # restart game
        if action == "r":
            return True

        # quit game
        elif action == "q":
            return False

        # show a player's cards
        elif action == "d":
            player = get_string("Name of player to whose cards you want to reveal: ")
            if player not in players:
                print(colored("ERROR: player name not found. Press 'p' to show players' names", "red"))
            else:
                show_cards(player, players)

        # list all cards in game
        elif action == "l":
            print("List of cards:\n"+", ".join(ALL_CARDS) + "\n")

        # list all players' names
        elif action =="p":
            print("List of players:\n"+", ".join(players) + "\n")

        # allow player to suspect
        elif action == "s":
            # get and compare guess
            guess = get_guess("I suspect")
            if guess == "cancel":
                continue
            result = guess & computerCards

            # disprove if possible
            if not result:
                print(colored("The computer cannot disprove.","yellow"))
            else:
                print(colored("That suspicion is false. The computer has the card: "+result.pop(),"yellow"))

            # clear screen
            while get_string("type 'c' to clear terminal\n").lower() != "c":
                continue
            os.system('clear')

        # allow player to accuse
        elif action == "a":
            # get and compare guess
            guess = get_guess("I accuse")
            if guess == "cancel":
                continue
            if guess == guilty:
                print(colored("Correct!", "green"))
            else:
                print(colored("Incorrect.","red"))

        elif action == "c":
            if get_string("Are you sure you want to reveal the answer? Type 'yes' to continue:\n") == "yes":
                print("Answer: " + colored(", ".join(guilty),"yellow"))
                        # clear screen
            while get_string("type 'c' to clear terminal\n").lower() != "c":
                continue
            os.system('clear')

def show_cards(player, players):
    """Shows the given player's cards"""
    os.system("clear")
    while get_string(f"type 'c' to reveal {player}'s cards\n").lower() != "c":
        os.system('clear')
        continue
    os.system('clear')
    print(f"{player}'s cards:\n")
    [print(card) for card in players[player]]
    print()
    while get_string("type 'c' to clear terminal\n").lower() != "c":
        continue
    os.system('clear')

def get_guess(prompt):
    """gets the guess from the user and checks against valid cards"""
    # get guess
    print(colored("List of cards:\n"+", ".join(ALL_CARDS) + "\n", "yellow"))
    print(prompt + " _ with the _ in the _.")
    guess = get_string("Type your guess in this format: person,weapon,room\nType 'cancel' to cancel guess\nGuess: ")

    # check if user cancelled
    if guess == "cancel":
        os.system("clear")
        return "cancel"

    # parse guess
    try:
        person,weapon,room = guess.split(",")
    except:
        print("Invalid guess format.")
        return "cancel"

    # validate guess
    if not person in SUSPECTS:
        print(colored("ERROR: Invalid person.","red"))
        return "cancel"
    if not weapon in WEAPONS:
        print(colored("ERROR: Invalid weapon.","red"))
        return "cancel"
    if not room in ROOMS:
        print(colored("ERROR: Invalid room.","red"))
        return "cancel"

    # return guess
    return {person, weapon, room}

if __name__ == "__main__":
    main()