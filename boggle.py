from time import time

# Function to load the Boggle board from a file
def load_board() -> list:
    with open('3x3.txt', 'r') as file:
        board = [list(line.strip().replace(" ", "").lower()) for line in file]
    return board

# Function to print the Boggle board
def print_board(board: list) -> None:
    for row in board:
        print(" ".join(row))
    print()

# Function to determine the possible moves from a given position on the board
def possible_moves(pair: tuple, board: list) -> set:
    x, y = pair
    moves = set()

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            # Check if the move is within the bounds of the board and not the current position
            if 0 <= x + i < len(board) and 0 <= y + j < len(board[0]) and (i, j) != (0, 0):
                moves.add((x + i, y + j))

    return moves

# Function to determine legal moves based on the current path
def legal_moves(possible_moves: set, path: list) -> set:
    return possible_moves - set(path)

# Function to check if a given word is a prefix of any words in the dictionary
def is_prefix(word: str, dictionary: set) -> bool:
    for entry in dictionary:
        if entry.startswith(word):
            return True
    return False

# Recursive function to explore the Boggle board and find words
def examine_state(x: int, y: int, current_word: str, visited: list, board: list, dictionary: set, smart_flag: bool, move_count: list, found_words_list: list) -> None:
    move_count[0] += 1
    current_word += board[x][y]
    visited.append((x, y))

    # Check if the current_word is in the dictionary, and print it if found
    if current_word in dictionary:
        found_words_list.append(current_word)

    # Early stop if using smart search and the current_word is not a prefix
    if smart_flag:
        if not is_prefix(current_word, dictionary):
            return

    possible_moves_set = possible_moves((x, y), board)
    legal_moves_set = legal_moves(possible_moves_set, visited)

    # Recursively explore legal moves
    for move in legal_moves_set:
        next_x, next_y = move
        examine_state(next_x, next_y, current_word, visited.copy(), board, dictionary, smart_flag, move_count, found_words_list)

    visited.pop()

# Function to solve the Boggle board using either smart search or regular search
def solve_boggle(board: list, dictionary: set, smart_flag: bool, move_count: list) -> list:
    found_words_list = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            examine_state(i, j, '', [], board, dictionary, smart_flag, move_count, found_words_list)
    return found_words_list

# Main function
def main() -> None:
    start = time()

    move_count = [0]

    # Set the smart_flag to choose between smart search and regular search
    smart_flag = True

    if smart_flag:
        print("Running with cleverness on!\n")
    else:
        print("Running with cleverness off!\n")

    # Load dictionary from file
    with open('dictionary.txt', 'r') as dictionary_file:
        dictionary = set(word.strip() for word in dictionary_file)

    # Load Boggle board
    boggle_board = load_board()

    # Print the initial Boggle board
    print("Initial Boggle Board:")
    print_board(boggle_board)

    # Solve the Boggle board 
    found_words_list = solve_boggle(boggle_board, dictionary, smart_flag, move_count)

    found_words_list = set(found_words_list) 

    # Organize words by length
    words_by_length = {}
    for word in found_words_list:
        length = len(word)
        if length not in words_by_length:
            words_by_length[length] = [word]
        else:
            words_by_length[length].append(word)

    end = time()

    print(f"\nNumber of moves: {move_count[0]}")

    print(f"\nWords found: {len(set(found_words_list))}\n")
    for length, words in sorted(words_by_length.items()):
        print(f"{length}-letter words: {', '.join(sorted(words))}")
    print(f"Alpha-sorted list: {sorted(set(found_words_list))}")
    print(f"\nTime elapsed: {round((end - start), 5)} seconds")

main()