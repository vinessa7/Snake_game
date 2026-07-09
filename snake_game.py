import turtle
import random


delay = 0.15

# Score 
score = 0
high_score = 0

#Set up the screen
window = turtle.Screen()
window.title("Snake Game")
window.bgcolor("black")  # fallback in case
window.bgpic('background.gif')
window.setup(width=600, height=700)
window.tracer(0) #turn off the animation on the screen, turn off automatic updates

# Refinstering images/gif
window.register_shape("background.gif")
window.register_shape("apple.gif")


# Border
border = turtle.Turtle()
border.speed(0)
border.color("white")
border.pensize(2)
border.penup()
border.goto(-290, -290)
border.pendown()
for _ in range(2):
    border.forward(580)
    border.left(90)
    border.forward(580)
    border.left(90)
border.penup()
border.goto(-290, 290)
border.pendown()
border.forward(580)
border.penup()
border.hideturtle()


# Snake head
head = turtle.Turtle()
head.speed(0) # animation speed of turtle module. Its the fastest animation speed
head.shape("square")
head.color("orange")
# Prevent the head from drawinf anything
head.penup() 
# this will make the head start from the middle of the screen. 
# Turtle module always starts at the middle of the scrren, but its good practice.
head.goto(0,0) 
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0) 
food.shape("apple.gif")
food.color("red")
food.penup() 
food.goto(0,100) 

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape('square')
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0,300)
pen.write("Score: 0  Hight Score: 0", 
          align = "center", font = ("Courier", 28, "bold"))

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"
def go_down():
    if head.direction != "up":
        head.direction = "down"
def go_left():
    if head.direction != "right":
            head.direction = "left"
def go_right():
    if head.direction != "left":
            head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def clear_score():
        global score
        score = 0
        pen.clear()
        pen.write("Score: {} High Score: {}".format(score, high_score), 
                  align="center",  font = ("Courier", 28, "bold"))

# Keyboard binding
window.listen()
for key in ("Up", "w"):
    window.onkeypress(go_up, key)
for key in ("Down", "s"):
    window.onkeypress(go_down, key)
for key in ("Left", "a"):
    window.onkeypress(go_left, key)
for key in ("Right", "d"):
    window.onkeypress(go_right, key)


# Main game loop
def game_tick():
    global score, high_score

    window.update()


    # Check for a collision with the border
    if head.xcor() > 290 or head.xcor() < -290 \
    or head.ycor() > 290 or head.ycor() < -290:
        head.goto(0,0)
        head.direction = "stop"

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)

        # Clear the segments list
        segments.clear()
        clear_score()
        window.ontimer(game_tick, int(delay * 1000))
        return 


    # Check for a collsion with the food
    if head.distance(food) < 20:
        # Move the food to a random spot on the screen
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        food.goto(x,y)

        # Need to add a segment to the snake
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color('orange')
        new_segment.penup()
        segments.append(new_segment)

        # Increase the score
        score += 1
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write("Score: {} High Score: {}".format(score, high_score), 
                  align="center", font = ("Courier", 28, "bold"))

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move the segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for head collisions with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            head.goto(0,0)
            head.direction = "stop"

            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)

            # Clear the segments list
            segments.clear()
            clear_score()
            window.ontimer(game_tick, int(delay * 1000))
            return

    window.ontimer(game_tick, int(delay * 1000))  

game_tick()
window.mainloop()
