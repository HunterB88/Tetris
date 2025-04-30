import turtle, random

# Global high score that persists until turtle window is closed
high_score = 0

TETROMINO_SHAPES = {
    'I': [(3, 0), (4, 0), (5, 0), (6, 0)],
    'J': [(3, 1), (3, 0), (4, 0), (5, 0)],
    'L': [(3, 0), (4, 0), (5, 0), (5, 1)],
    'O': [(4, 0), (5, 0), (4, 1), (5, 1)],
    'S': [(4, 0), (5, 0), (3, 1), (4, 1)],
    'T': [(3, 0), (4, 0), (5, 0), (4, 1)],
    'Z': [(3, 0), (4, 0), (4, 1), (5, 1)],
    'V': [(3, 0), (3, 1), (3, 2), (3, 3)],
}
TETROMINO_COLORS = {
    'I': '#00ffff',  # bright cyan
    'J': '#0000ff',  # deep blue
    'L': '#ff9900',  # vibrant orange
    'O': '#ffff00',  # bright yellow
    'S': '#00ff00',  # lime green
    'T': '#aa00ff',  # purple
    'Z': '#ff0000',  # bright red
    'V': '#ffffff',  # white 
}

SCALE = 30 #Controls how many pixels wide each grid square is

class Game:
    def __init__(self):
        #Setup window size based on SCALE value.
        turtle.setup(SCALE*12+20, SCALE*22+20)

        #Bottom left corner of screen is (-1.5,-1.5)
        #Top right corner is (10.5, 20.5)
        turtle.setworldcoordinates(-1.5, -1.5, 10.5, 20.5)
        cv = turtle.getcanvas()
        cv.adjustScrolls()

        #Ensure turtle is running as fast as possible
        turtle.hideturtle()
        turtle.delay(0)
        turtle.speed(0)
        turtle.tracer(0, 0)

        #Draw rectangular play area, height 20, width 10
        turtle.bgcolor('black')
        turtle.pencolor('white')
        turtle.penup()
        turtle.setpos(-0.525, -0.525)
        turtle.pendown()
        for i in range(2):
            turtle.forward(10.05)
            turtle.left(90)
            turtle.forward(20.05)
            turtle.left(90)
        
        self.active = Block()
        self.game_over = False
        self.occupied = [[None for _ in range(10)] for _ in range(24)]
        self.score = 0
        self.score_turtle = turtle.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.color('white')
        self.high_score_turtle = turtle.Turtle()
        self.high_score_turtle.hideturtle()
        self.high_score_turtle.penup()
        self.high_score_turtle.color('white')
        self.update_score_display()

        turtle.onkeypress(self.rotate, 'space')
        turtle.onkeypress(self.move_left, 'Left')
        turtle.onkeypress(self.move_right, 'Right')
        turtle.onkeypress(self.move_down, 'Down')
        turtle.ontimer(self.gameloop, 300)
        
        #These three lines must always be at the BOTTOM of __init__
        turtle.update()
        turtle.listen()
        turtle.mainloop()

    def update_score_display(self):
        self.score_turtle.clear()
        self.high_score_turtle.clear()
        self.score_turtle.goto(9, 19.8)
        self.high_score_turtle.goto(0, 19.8)
        self.score_turtle.write(f"Score: {self.score}", align="right", font=("Arial", 20, "bold"))
        self.high_score_turtle.write(f"High Score: {high_score}", align="left", font=("Arial", 20, "bold"))

    def add_score(self, points):
        self.score += points
        self.update_score_display()

    def show_game_over(self):
        global high_score
        # Update high score if current score is higher
        if self.score > high_score:
            high_score = self.score
        
        # Create a turtle for the game over text
        game_over_turtle = turtle.Turtle()
        game_over_turtle.hideturtle()
        game_over_turtle.penup()
        
        # Draw grey background rectangle
        game_over_turtle.goto(1, 3)
        game_over_turtle.color('grey')
        game_over_turtle.begin_fill()
        for _ in range(2):
            game_over_turtle.forward(7)
            game_over_turtle.left(90)
            game_over_turtle.forward(9)
            game_over_turtle.left(90)
        game_over_turtle.end_fill()
        
        # Write text on top of background
        game_over_turtle.color('white')
        game_over_turtle.goto(4.5, 10)  # Center of the play area
        game_over_turtle.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
        game_over_turtle.goto(4.5, 8)  # Center of the play area
        game_over_turtle.write(f"Final Score: {self.score}", align="center", font=("Arial", 16, "normal"))
        game_over_turtle.goto(4.5, 6)  # Center of the play area
        game_over_turtle.write(f"High Score: {high_score}", align="center", font=("Arial", 16, "normal"))
        game_over_turtle.goto(4.5, 4)  # Center of the play area
        game_over_turtle.write("Press 'R' to restart", align="center", font=("Arial", 16, "normal"))
        
        # Add restart functionality
        turtle.onkeypress(self.restart_game, 'r')
        turtle.onkeypress(self.restart_game, 'R')

    def restart_game(self):
        # Clear the screen
        turtle.clearscreen()
        # Reset the game
        self.__init__()

    def gameloop(self):
        if self.game_over:
            return

        if self.active.valid(0, -1, self.occupied):
            self.active.move(0, -1)
        else:
            for square in self.active.squares:
                x = int(square.xcor())
                y = int(square.ycor())
                if y >= 20:  # Changed from len(self.occupied) to 20 to match the top line
                    self.game_over = True
                    self.show_game_over()
                    return
                if 0 <= y < len(self.occupied):
                    self.occupied[y][x] = square

            self.clear_lines()
            self.active.locked = True
            self.active = Block()

        turtle.update()
        turtle.ontimer(self.gameloop, 300)  # ← always schedule next tick

    def move_left(self):
        if self.active.valid(-1, 0, self.occupied):
          self.active.move(-1, 0)
          turtle.update()

    def move_right(self):
        if self.active.valid(1, 0, self.occupied):
          self.active.move(1, 0)
          turtle.update()

    def move_down(self):
        if self.active.valid(0, -1, self.occupied):
          self.active.move(0, -1)
          turtle.update()

    def rotate(self):
      if not self.active.locked:
          self.active.rotate(self.occupied)
          turtle.update()

    def clear_lines(self):
        width = 10
        height = len(self.occupied)
        full_rows = []
        for y in range(height):
            if all(self.occupied[y][x] is not None for x in range(width)):
                full_rows.append(y)
                for square in self.occupied[y]:
                    square.hideturtle()
                self.occupied[y] = [None] * width

        if not full_rows:
            return

        # Award points based on number of lines cleared
        # 1 line = 100 points
        # 2 lines = 300 points
        # 3 lines = 600 points
        # 4 lines = 1000 points
        points = {1: 100, 2: 300, 3: 600, 4: 1000}
        self.add_score(points.get(len(full_rows), 1500))

        for cleared_y in sorted(full_rows, reverse=True):
            # Shift all rows above the cleared row down by 1
            for y in range(cleared_y, height - 1):
                for x in range(width):
                    square = self.occupied[y + 1][x]
                    self.occupied[y][x] = square
                    if square:
                        square.goto(x, y)
                    self.occupied[y + 1][x] = None



class Square(turtle.Turtle):
    
    def __init__(self, x, y, color):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.shapesize(stretch_wid=(SCALE / 20) * 0.95, stretch_len=(SCALE / 20) * 0.95)
        self.speed(0)
        self.fillcolor(color)
        self.pencolor('black')  
        self.penup()
        self.goto(int(x), int(y))



class Block:
    def __init__(self):
        self.squares = []
        self.shape = random.choice(list(TETROMINO_SHAPES.keys()))
        self.coords = TETROMINO_SHAPES[self.shape]
        color = TETROMINO_COLORS[self.shape]
        self.pivot = self.coords[1]

        for x, y in self.coords:
            self.squares.append(Square(int(x), int(y + 21), color))

        self.locked = False

    def move(self, dx, dy):
        for square in self.squares:
            x = square.xcor()
            y = square.ycor()
            square.goto(x + dx, y + dy)

    def valid(self, dx, dy, occupied):
      for square in self.squares:
          x = int(square.xcor() + dx)
          y = int(square.ycor() + dy)

          if x < 0 or x > 9 or y < 0:
              return False

          if y < len(occupied) and occupied[y][x]:
              return False

      return True

    def rotate(self, occupied):
        if self.shape == 'O':  # Don't rotate square blocks
            return

        pivot_x = int(self.squares[1].xcor())
        pivot_y = int(self.squares[1].ycor())

        new_positions = []

        for square in self.squares:
            x = int(square.xcor())
            y = int(square.ycor())

            rel_x = x - pivot_x
            rel_y = y - pivot_y

            # Rotate 90 degrees clockwise: (x, y) → (y, -x)
            new_x = pivot_x - rel_y
            new_y = pivot_y + rel_x

            if not (0 <= new_x <= 9 and 0 <= new_y < len(occupied)):
                return  # out of bounds
            if occupied[new_y][new_x]:
                return  # collision

            new_positions.append((new_x, new_y))

        # If all new positions are valid, move squares
        for square, (new_x, new_y) in zip(self.squares, new_positions):
            square.goto(new_x, new_y)



if __name__ == '__main__':
    Game()
