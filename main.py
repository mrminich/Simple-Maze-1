# REPLACE WITH YOUR NAME2

# WORKS CITED:
# REPLACE THIS WITH WEBSITE LINKS

# UPGRADES: 
# REPLACE THIS WITH A DESCRIPTION OF YOUR UPGRADE(S)

######### imports

# for getkey & use arrow keys
from getkey import getkey, keys 

######### constants 

TITLE = "Simple Maze"
INSTRUCTIONS = "Use the arrow keys to reach the end of the maze!"

VERTICAL_OFFSET_TITLE = 1     # num of lines from top of screen for the title
VERTICAL_OFFSET_MAZE = 4      # num of lines from top of screen for the maze board
VERTICAL_OFFSET_STATUS_PANEL = 15   # num of lines from top of screen for the status panel

MOVES_ALLOWED = 9     # num of moves player has to complete the maze w/o losing
ROWS = 5              # maze height (# of rows), must match gameboard
COLUMNS = 5           # maze width (# of columns), must match gameboard

PLAYER_START_ROW = 1  # row # of player's starting position
PLAYER_START_COL = 1  # column # of player's starting position

F = " "               # fill character for empty positions
P = "\N{mouse face}"  # player's symbol https://unicode.org/emoji/charts/full-emoji-list.html
V = "|"               # vertical wall symbol
H = "-"               # horizontal wall symbol
E = "F"               # symbol for the end of the maze
B = "*"               # symbol for border

########## global variables

movesRemaining = MOVES_ALLOWED    # num moves remaining to complete maze

playerRow = PLAYER_START_ROW      # player row #
playerCol = PLAYER_START_COL      # player column #
gameStatus = ""                   # game status (win, lose)
isGameOver = False                # flag variable to control game loop  
message = ""                      # error message to display to user

# make sure that the correct symbols are placed in desired rows and columns
gameboard = [
  # columns
  # 0 1 2 3 4  # rows
  [B,B,B,B,B],  # 0 
  [B,P,V,F,B],  # 1 
  [B,F,F,F,B],  # 2
  [B,F,V,E,B],  # 3
  [B,B,B,B,B]   # 4
]

########## functions

def displayStatusPanel():
  # display status panel

  # set cursor to position of status panel
  print("\033[" + str(VERTICAL_OFFSET_STATUS_PANEL) + ";0H")
  print("Remaining Moves: " + str(movesRemaining) + " out of " + str(MOVES_ALLOWED))
  print("Current Location: Row " + str(playerRow) + " Column " + str(playerCol))
  print()
  if message != "":
    print("Message: " + message)

########### main program

###### initial setup

# hide cursor (use h instead of l to show cursor)
print("\033[?25l")  

# clear screen and set cursor to top left corner
print("\033[2J", end = "") 

# set blue (34) as text color, see Works Cited
print("\033[34m", end = "")

# set cursor to position of title    
print("\033[" + str(VERTICAL_OFFSET_TITLE) + ";0H", end = "")

print(TITLE)

# reset color to normal (0)
print("\033[0m", end = "")

print(INSTRUCTIONS)

# set cursor to position of maze
print("\033[" + str(VERTICAL_OFFSET_MAZE) + ";0H", end = "")

# place the player's symbol in the maze
gameboard[playerRow][playerCol] = P

# loop through the gameboard printing each symbol
# to display the initial maze
for row in range(ROWS):
  for col in range(COLUMNS):
    print(gameboard[row][col], end = " ")
  print()

displayStatusPanel()



############ main game loop

# keep looping until the game is won or lost
while not isGameOver:
  previousPlayerRow = playerRow
  previousPlayerCol = playerCol 
  previousSymbol = gameboard[playerRow][playerCol] 
  playerMove = getkey()
  movesRemaining -= 1

  # player moves right
  if playerMove in [keys.RIGHT, "d"]:

    if playerCol < COLUMNS:
      playerCol += 1
      # don't let player leave maze
      if playerCol >= COLUMNS - 1:
        playerCol = COLUMNS - 1

  # player moves left
  elif playerMove in [keys.LEFT, "a"]:
    
    if playerCol > 0:
      playerCol -= 1
      # don't let player leave maze
      if playerCol <= 0:
        playerCol = 0

  # player moves down
  elif playerMove in [keys.DOWN, "s"]:
   
    if playerRow < ROWS - 1:
      playerRow += 1
      # don't let player leave maze
      if playerRow >= ROWS:
        playerRow = ROWS - 1

  # player moves up
  elif playerMove in [keys.UP, "w"]:
    if playerRow > 0:
      playerRow -= 1  
      # don't let player leave maze
      if playerRow <= 0:  
        playerRow = 0

  # win detection
  if gameboard[playerRow][playerCol] == E:
    message = "You won. Congratulations."
    gameStatus = "win"
    isGameOver = True

  # collision detection with walls
  elif gameboard[playerRow][playerCol] in [B, H, V]:
    message = "You hit a wall. Game over."
    gameStatus = "lose"
    isGameOver = True
  
  # check remaining moves
  if movesRemaining <= 0:
    message = "You ran out of moves. Game Over."
    gameStatus = "lose"
    isGameOver = True

  gameboard[playerRow][playerCol] = P
  gameboard[previousPlayerRow][previousPlayerCol] = F

  buffer = ""

  # previous row from player's current position
  for col in range(COLUMNS):
    if playerRow > 0:
      buffer += (gameboard[playerRow - 1][col] + " ")
  buffer += "\n"

  # row of player's current position
  for col in range(COLUMNS):
    buffer += (gameboard[playerRow][col] + " ")
  buffer += "\n"

  # next row after player's current position
  for col in range(COLUMNS):
    if playerRow < ROWS - 1:
      buffer += (gameboard[playerRow + 1][col] + " ")

  # print area of board above 1-3 rows 
  # around player's current position
  
  print("\033[" + str(playerRow - 1 + VERTICAL_OFFSET_MAZE) + ";0H", end = "")
  
  # print the rows where the player moved
  print(buffer)
  
  displayStatusPanel()