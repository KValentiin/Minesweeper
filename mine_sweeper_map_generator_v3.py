"""
The is a terminal based Python implementation of the classic game Minesweeper,
allowing the user to change the difficulty of the game by modifying the parameters.
"""

#! ########################           IMPORTS          ########################


import random   # Generating random numbers, selecting random

import os       # Operating system dependent functionality, such as

import colorama # Importing to use colours in print statements
from colorama import Fore, Back, Style # Importing text, background, and style
from colorama import just_fix_windows_console # Fix the console colour issue
just_fix_windows_console()


# Text colours for less clutter and readability
alert     = Fore.RED     + Back.WHITE   + Style.BRIGHT
cyan      = Fore.CYAN                   + Style.BRIGHT
green     = Fore.GREEN                  + Style.BRIGHT
yellow    = Fore.YELLOW                 + Style.BRIGHT
magenta   = Fore.MAGENTA                + Style.BRIGHT
white     = Fore.WHITE                  + Style.BRIGHT
red       = Fore.RED                    + Style.BRIGHT
reset_all =                               Style.RESET_ALL


#! ########################     DEFINING FUNCTIONS     ########################


def clear_screen():
    """
    The function `clear_screen()` clears the terminal screen.
    """
    os.system("clear||cls")


def generate_minesweeper_map(size, num_mines):
    """
    Generates a minesweeper map of a given size with a specified
    number of mines, where each cell contains either a mine or the number of
    adjacent mines.
    """
    # Create a blank map
    minefield = [[' ' for _ in range(size)] for _ in range(size)]
    
    # Place mines randomly
    mine_positions = random.sample(range(size * size), num_mines)
    for mine_position in mine_positions:
        row = mine_position // size
        col = mine_position % size
        minefield[row][col] = 'M'
    
    # Update adjacent mine counts
    for row in range(size):
        for col in range(size):
            if minefield[row][col] == 'M':
                continue  # Skip counting for mines
            
            mine_count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= row + i < size and 0 <= col + j < size and minefield[row + i][col + j] == 'M':
                        mine_count += 1
            
            # Update the current cell with the mine count
            minefield[row][col] = str(mine_count)
    
    return minefield


def print_hidden_minesweeper_map(minefield):
    """
    Prints a hidden minesweeper map, replacing empty cells with '#'
    symbols.
    """
    for row in minefield:
        print("\t" + '  '.join(['#' if cell == '  ' else cell for cell in row]))


def print_minesweeper_map(minefield):
    """
    Prints a minesweeper map by iterating through each row of the
    minefield and joining the elements with a space in between.
    """
    for row in minefield:
        print(' '.join(row))


def play_game():
    
    """
    The `play_game` function allows the user to play a game of Minesweeper by
    generating a minesweeper map, taking user input for row and column, and
    updating the hidden map accordingly.
    """
    #! CHANGEABLE PARAMETERS    
    
    max_size = 30
    max_mines_fraction = 0.25

    while True:
        try:
            print()
            size = int(input(yellow + "Enter the size of the Minesweeper grid " + white + "(" + cyan + "1 " + yellow + "to "+ cyan + str(max_size) + white + ")" + yellow + ": " + reset_all))
            if 1 <= size <= max_size:
                break
            else:
                print()
                print(alert + "Error: Size must be between 1 and " + str(max_size) + ". Please try again." + reset_all)
                print()
        except ValueError:
            print()
            print(alert + "Invalid input. Please enter a valid number." + reset_all)
            print()
    
    while True:
        try:
            max_mines = int(size * size * max_mines_fraction)
            print()
            num_mines = int(input(yellow + "Enter the number of mines " + white + "(" + cyan + "1 " + yellow + "to "+ cyan + str(max_mines) + white + ")" + yellow + ": " + reset_all))
            if 1 <= num_mines <= max_mines:
                break
            else:
                print()
                print(alert + "Error: Number of mines must be between 1 and " + str(int(max_mines)) + ". Please try again." + reset_all)
                print()
        except ValueError:
            print()
            print(alert + "Invalid input. Please enter a valid number." + reset_all)
            print()
    
    # Now you have valid inputs for size and num_mines
    print()
    print("Size: " + str(size) + ", Number of Mines: " + str(num_mines))
    print()
    
    clear_screen()
    
    minesweeper_map = generate_minesweeper_map(size, num_mines)
    hidden_map = [['#' for _ in range(size)] for _ in range(size)]
    
    print_hidden_minesweeper_map(hidden_map)
    
    
    
    """
    Continuously prompt the user for input. The user can enter the row and column 
    of a cell they want to uncover, or they can enter specific commands such as 
    'menu' to go back to the menu, 'exit' to exit the game, or 'done' to check if 
    they have cleared the minefield.
    """
    while True:
        
        print()
        user_input = input(yellow + """
Enter """ + cyan +  """row """  + yellow + """and """ + magenta + """column""" + white + """ (e.g., """ + cyan + """1 """ + magenta + """2""" + white + """)
      """ + green + """done """ + yellow + """to finish
      """ + white + """menu """ + yellow + """to go back to the menu
      """ + red +   """exit """ + yellow + """to exit game
      """ + reset_all)
        
        if user_input.lower() == 'menu':
            clear_screen()
            return
        
        elif user_input.lower() == 'exit':
            exit()
            
        elif user_input.lower() == 'done':
            remaining_uncovered = [(i, j) for i, row in enumerate(hidden_map) for j, cell in enumerate(row) if cell == '#']
            
            if not remaining_uncovered:
                clear_screen()
                print()
                print(green + "Congratulations! You've cleared the minefield. You Won!" + reset_all)
                print()
                break
            
            else:                
                non_mine_remaining = [minesweeper_map[i][j] for i, j in remaining_uncovered if minesweeper_map[i][j] != 'M']
                if not non_mine_remaining:
                    clear_screen()
                    print()
                    print(green + "Congratulations! You've cleared the minefield. You Won!" + reset_all)
                    print()
                    break
                
                else:
                    print()
                    print(alert + "There are still uncovered non-mine positions at. Continue uncovering or use 'done' again." + reset_all)
                    print()
                    continue
        
        # Input for the row and column of the cell they want to uncover
        try:
            row, col = map(int, user_input.split())
            if 1 <= row <= size and 1 <= col <= size:
                
                row -= 1
                col -= 1
                
                if minesweeper_map[row][col] == 'M':
                    clear_screen()
                    print()
                    print(alert + "Game Over! You hit a mine." + reset_all)
                    print()
                    break
                
                elif hidden_map[row][col] == '#':
                    clear_screen()
                    hidden_map[row][col] = minesweeper_map[row][col]
                    print_hidden_minesweeper_map(hidden_map)
                    
                else:
                    print()
                    print(alert + "Cell already uncovered. Choose another position." + reset_all)
                    print()
                    
            else:
                print()
                print(alert + "Invalid input. Row and column must be between 1 and " + str(size) + '!' + reset_all)
                print()
                
        except ValueError:
            print()
            print(alert + "Invalid input. Please enter row and column as numbers." + reset_all)
            print()




#! ########################           MAIN           ########################


clear_screen()

# It's only executed if the script is run directly, and not if it is imported as a module.
if __name__ == "__main__":
    
    while True:
        print(yellow + """
    Welcome to the terminal based""" + reset_all)
        
        print("""
        ┳┳┓•                  
        ┃┃┃┓┏┓┏┓┏┓┏┏┏┓┏┓┏┓┏┓┏┓
        ┛ ┗┗┛┗┗ ┛┗┻┛┗ ┗ ┣┛┗ ┛ 
                        ┛""")
        print(white + """
            Main Menu""" + reset_all)
        print()
        print(cyan + "1 " + white + "- " + cyan + "Start New Game" + reset_all)
        print( red + "2 " + white + "- " + red + "Exit" + reset_all)
        print()
        choice = input(white + "Enter your choice (" + cyan + "1" + white + " or " + red + "2" + white + ")" + white + ": " + reset_all)
        
        if choice == '1':
            clear_screen()
            play_game()
            
        elif choice == '2':
            exit()
            
        else:
            clear_screen()
            print()
            print(alert + "Invalid choice. Please enter 1 or 2." + reset_all)
            print()

