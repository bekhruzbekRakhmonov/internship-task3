import sys
import hashlib
import hmac
import secrets
import pandas as pd

class KeyGenerator:
    @staticmethod
    def generate_key():
        return secrets.token_hex(32)

class HmacGenerator:
    @staticmethod
    def generate_hmac(key, message):
        key = bytes.fromhex(key)
        message = message.encode('utf-8')
        return hmac.new(key, message, hashlib.sha256).hexdigest()

class GameRules:
    def __init__(self, moves):
        self.moves = moves

    def determine_winner(self, user_move, computer_move):
        total_moves = len(self.moves)
        half_moves = total_moves // 2

        user_index = self.moves.index(user_move)
        computer_index = self.moves.index(computer_move)

        if (computer_index + half_moves) % total_moves == user_index:
            return "Lose"
        elif (user_index + half_moves) % total_moves == computer_index:
            return "Win"
        else:
            return "Draw"

class HelpTableGenerator:
    def __init__(self, moves):
        self.moves = moves

    def generate_help_table(self):
        table = [[' ' for _ in range(len(self.moves) + 2)] for _ in range(len(self.moves) + 1)]
        table[0][0] = 'PC\\User >'
        for i in range(len(self.moves)):
            table[0][i + 1] = self.moves[i]
            table[i + 1][0] = self.moves[i]

        for i in range(len(self.moves)):
            for j in range(len(self.moves)):
                result = GameRules(self.moves).determine_winner(self.moves[i], self.moves[j])
                table[i + 1][j + 1] = result

        return table

def main():
    moves = sys.argv[1:]
    if len(moves) < 3 or len(moves) % 2 == 0 or len(set(moves)) != len(moves):
        print("Error: Incorrect number of moves or moves are not unique.")
        print("Example usage: python game.py rock paper scissors")
        return

    key = KeyGenerator.generate_key()
    computer_move = secrets.choice(moves)

    print(f"HMAC key: {key}")
    print("Available moves:")
    for i, move in enumerate(moves):
        print(f"{i + 1} - {move}")
    print("0 - exit")
    print("? - help")

    user_input = input("Enter your move: ")

    if user_input == "?":
        help_table = HelpTableGenerator(moves).generate_help_table()
        cols = [col.pop(0) for col in help_table]
        help_table.pop(0)
        for i in range(len(cols[1:])):
            help_table[i].pop()
            help_table[i].insert(0, cols[1:][i])
        df = pd.DataFrame(help_table, columns = cols, index=[f"{n}th" for n in range(1, len(cols))])
        print(df)
    elif user_input.isdigit():
        user_choice = int(user_input)
        if user_choice == 0:
            print("Exiting the game.")
            return
        elif 1 <= user_choice <= len(moves):
            user_move = moves[user_choice - 1]
            print(f"Your move: {user_move}")
            print(f"Computer move: {computer_move}")

            winner = GameRules(moves).determine_winner(user_move, computer_move)
            print(f"You {winner.lower()}!")
            print(f"HMAC: {HmacGenerator.generate_hmac(key, user_move)}")
        else:
            print("Invalid input. Please try again.")
    else:
        print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()