import random

# DIMENSIONS AND COLOR OF THE WINDOW IN WHICH THE GAME WILL BE DISPLAYED.
TAB_WIDTH = 200
TAB_LENGTH = 400
TAB_COLOR = 210

# DIMENSIONS OF THE TETRIS RUSH GRID
NUMS_ROWS = 20
NUMS_COLUMNS = 10

# THE BLOCK SIZE, A 2D LIST OF ITS POSSIBLE COLORS, RANDOM COLOR ASSIGNER FOR BLOCK, AND STORAGE FOR ITS RANDOMLY CHOSEN COLOR--RESPECTIVELY
BLOCK_SIZE = TAB_WIDTH//NUMS_COLUMNS
BLOCK_COLORS = [[255, 51, 52], [12, 150, 228], [30, 183, 66], [246, 187, 0], [76, 0, 153], [255, 255, 255], [0, 0, 0]]
#CHOSEN_RANDOM_COLOR = random.randint(0, len(BLOCK_COLORS)-1)
#ASSIGN_RANDOM_COLOR = color(BLOCK_COLORS[CHOSEN_RANDOM_COLOR][0], BLOCK_COLORS[CHOSEN_RANDOM_COLOR][1], BLOCK_COLORS[CHOSEN_RANDOM_COLOR][2])

# INITIALLIZING VARIABLES AND BOOLEANS
START_GAME = True
FALLING_SPEED = 0
SCORE_COUNT = 0
NO_FALLING_BLOCK = True
CONTINUE_PLAYING = True
# ALL_COLUMNS_CHECKER IS A DYNAMIC 2D LIST THAT CONTAINS ANY DESIRED NUMBER OF COLUMNS IN ROW ZERO AND WILL BE USED TO CHECK WHEN THE GAME HAS ENDED.
ALL_COLUMNS_CHECKER = []
for C in range(NUMS_COLUMNS):
    ALL_COLUMNS_CHECKER.append(C)
 
# A DYNAMIC 2D LIST THAT STORES 0 FOR EMPTY CELLS AND WILL EVENTUALLY STORE 1 FOR OCCUPIED CELLS IN ORDER TO MAKE BLOCK MOVEMENTS SIMPLER AND LESS ERROR PRONE TO CODE.
BLOCK_INDEXER = []
for C in range(NUMS_COLUMNS):
    COLUMNS = []
    for R in range(NUMS_ROWS):
        COLUMNS.append(0)
    BLOCK_INDEXER.append(COLUMNS)
###########################################################################################################################################################################################################################

class Block():
    def __init__(self):
        # GENERATES A RANDOM X COORDINATE FOR THE BLOCK TO OCCUPY THE CELL IN THE FORM OF 1 IN THE BLOCK_INDEXER LIST.
        self.x = random.randint(0, NUMS_COLUMNS-1)
        self.y = 0
        self.key_handler = {LEFT: False, RIGHT: False}
        while BLOCK_INDEXER[self.x][0] == 1:
            self.x = random.randint(0, NUMS_COLUMNS-1)
        self.ASSIGN_RANDOM_COLOR()

    # RANDOMLY PICKS AN ELEMENT FROM THE BLOCK_COLORS LIST
    def ASSIGN_RANDOM_COLOR(self):
        self.CHOSEN_RANDOM_COLOR = random.randint(0, len(BLOCK_COLORS)-1)
    
    # RESPONSIBLE FOR GENERATING RANDOM BLOCKS AND ASSIGNING THEM ITS PROPERTIES AND MOVEMENTS.
    def block_generator(self):
        global NO_FALLING_BLOCK
        fill(color(BLOCK_COLORS[self.CHOSEN_RANDOM_COLOR][0], BLOCK_COLORS[self.CHOSEN_RANDOM_COLOR][1], BLOCK_COLORS[self.CHOSEN_RANDOM_COLOR][2])) # GIVES THE RANDOM BLOCK A COLOR.
        rect(self.x*BLOCK_SIZE, self.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        
        # LETS EACH BLOCK FALL DOWN TO THE APPROPRIATE ROW
        if self.y < NUMS_ROWS-1-BLOCK_INDEXER[self.x].count(1):
            self.regenerate_grid()
            NO_FALLING_BLOCK = False
            
        elif self.y == NUMS_ROWS-1:
            NO_FALLING_BLOCK = True
    
    # GIVES THE RANDOM BLOCK THE APPERANCE OF FALLING DOWN WITH THE GIVEN SPEED FOR IT AT THE TIME.
    def regenerate_grid(self):
        self.y = self.y + 1
        
        if self.key_handler[LEFT] == True and self.x != 0 and BLOCK_INDEXER[self.x-1][self.y] != 1:
            self.x = self.x - 1
        elif self.key_handler[RIGHT] == True and self.x != NUMS_COLUMNS - 1 and BLOCK_INDEXER[self.x+1][self.y] != 1:
           self.x = self.x + 1                 
###########################################################################################################################################################################################################################

class Game():
    def __init__(self):
        self.block_store = [] # BLOCK_STORE IS A 2D LIST THAT WILL BE USED TO STORE BLOCKS IN ORDER TO MAKE BLOCK DELETION MORE INTUITIVE TO CODE.
        self.gameover = False

    def grid_generator(self):
        stroke(180)
        for R in range(1, NUMS_ROWS+1):
            line(0, R*BLOCK_SIZE, TAB_WIDTH, R*BLOCK_SIZE)
            for C in range(NUMS_COLUMNS):
                line(C*BLOCK_SIZE, 0, C*BLOCK_SIZE, TAB_LENGTH)
            
    def game_start(self):
        global NO_FALLING_BLOCK, CONTINUE_PLAYING, FALLING_SPEED
        
        self.grid_generator()
        self.score_board()

        
        if NO_FALLING_BLOCK == True:
            self.write_block()
            
        for b in self.block_store:
            b.block_generator()
                
        if NO_FALLING_BLOCK == True:
            BLOCK_INDEXER[self.block_store[-1].x][self.block_store[-1].y] = 1 # STORES A 1 IN THE BLOCK_INDEXER 2D LIST TO REGISTER AN OCCUPIED CELLS.
            
            self.unwrite_block()
            FALLING_SPEED = FALLING_SPEED + 0.25
            self.check_if_game_over()
                        
    def score_board(self):
        global SCORE_COUNT

        fill(0, 0, 0)
        textSize(15)
        text("Score: "+str(SCORE_COUNT), 120, 20)
    
    # INSTANTIATES BLOCK    
    def write_block(self):
        self.block = Block()
        self.block_store.append(self.block)
        
    def unwrite_block(self):
        global SCORE_COUNT, FALLING_SPEED, CHOSEN_RANDOM_COLOR
        
        same_color_checker = self.block_store[-1].CHOSEN_RANDOM_COLOR
        same_column_checker = self.block_store[-1].x
        same_row_checker = self.block_store[-1].y
        
        block_counter = 0 # BLOCK_COUNTER IS A VARIABLE THAT IS USED TO COUNT THE NUMBER OF SAME-COLORED, VERTICALLY-CONSECUTIVE BLOCKS.
        winning_blocks = [] # WINNING_BLOCKS IS A 2D LIST THAT THAT STORES POTENTIAL WINNING BLOCKS THAT TRANSFERS THEM FROM BLOCK_STORE TO THIS LIST BY REMOVING THE BLOCKS FROM BLOCK_STORE.
        
        # CHECKS FOR 4 VERTICAL BLOCKS OF THE SAME COLOR AND ADJUSTS THE GAME ACCORDINGLY.
        for b in self.block_store:
            try:
                if b.CHOSEN_RANDOM_COLOR == same_color_checker:
                    for k in range(4):
                        if b.x == same_column_checker and b.y == same_row_checker + k:
                            block_counter = block_counter + 1
                            winning_blocks.append(b)
                else:
                    continue
                
                if block_counter == 4:
                    for b in winning_blocks:
                        self.block_store.remove(b)
                        BLOCK_INDEXER[b.x][b.y] = 0
                        
                    SCORE_COUNT = SCORE_COUNT + 1
                    FALLING_SPEED = 0
                    
            except:
                pass
     
     # CHECKS IF THE GAME IS OVER BY CHECKING IF THE FIRST ROW OF THE GRID IF FULL (THROUGH 1 AND 0), THEN REMOVES THE 1 ELEMENTS FROM THE BLOCK_INDEXER UNTIL REACHES ZERO ELEMENTS FOR GAME OVER.          
    def check_if_game_over(self):
        global ALL_COLUMNS_CHECKER, CONTINUE_PLAYING
        
        for C in range(NUMS_COLUMNS):
            if BLOCK_INDEXER[C][0] == 1:
                try:
                    ALL_COLUMNS_CHECKER.remove(C)
                except:
                    pass
        
        if len(ALL_COLUMNS_CHECKER) == 0:
            game.game_is_active = False
            CONTINUE_PLAYING = False
            START_GAME = False
            self.end_the_game()
            
    def end_the_game(self):
        global SCORE_COUNT
        
        START_GAME = False
        background(0, 0, 0)
        fill(255,255,255)
        ellipse(100, 197, 180, 180)
        fill(0, 0, 0)
        textSize(26)
        text("GAME OVER", 26, 190)
        textSize(20)
        text("Score: "+str(SCORE_COUNT), 60, 221)
        textSize(15)
        text("Click to restart", 45, 250)  
###########################################################################################################################################################################################################################


game = Game()
block = Block()


    
def setup():
    size(TAB_WIDTH, TAB_LENGTH)
    stroke(180)
    strokeWeight(1.3)
       # function that creates a grid showing both 'filled' and 'empty' cells
    frameRate(60)
    
def draw():
    global FALLING_SPEED, START_GAME, SCORE_COUNT
    #slows down the game by not displaying every frame
    if frameCount%(max(1, int(8 - FALLING_SPEED)))==0 or frameCount==1:
        background(TAB_COLOR)
        #this calls the display method of the game class
        game.game_start()
        


def keyPressed():
    if keyCode == LEFT:
        game.block.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.block.key_handler[RIGHT] = True
    
def keyReleased():
    if keyCode == LEFT:
        game.block.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.block.key_handler[RIGHT] = False
        
def mouseClicked():
    if len(ALL_COLUMNS_CHECKER)==0:
        BLOCK_INDEXER.clear()
        game = Game()
        block = Block()

        
        
    
