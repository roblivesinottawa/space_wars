import os
import random
import time

import turtle
turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
# add background image
turtle.bgpic("starfield.gif")
# change window title
turtle.title("Space War")
turtle.hideturtle()
turtle.setundobuffer(1)
turtle.tracer(0)


class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        # boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.right(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.right(60)
        if self.ycor() > 290:
            self.sety(290)
            self.right(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.right(60)

    def is_collision(self, other):
        if self.xcor() >= other.xcor() -20 and \
        self.xcor() <= other.xcor() + 20 and \
        self.ycor() >= other.ycor() - 20 and \
        self.ycor() <= other.ycor() + 20:
            return True
        return False



class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4
        self.lives = 3

    def turn_left(self):
        self.left(45)

    
    def turn_right(self):
        self.right(45)

    
    def accelelate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed)

        # boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.left(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.left(60)
        if self.ycor() > 290:
            self.sety(290)
            self.left(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.left(60)

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            # play missile sound
            # os.system("afplay laser.mp3&")

            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)


        if self.status == "firing":
            self.fd(self.speed)
        

        # border check
        if self.xcor() < - 290 or self.xcor() > 290 or self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.got(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame < 15:
            self.frame = 0
            self.goto(-1000, -1000)


class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.right(90)
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = f"Score: {self.score}"
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial",16, "normal"))

# create game object
game = Game()

# draw the border
game.draw_border()

# show the game status

game.show_status()

# create sprites
player = Player("triangle", "white", 0, 0)
# enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
# ally = Ally("square", "blue", 100, 0)

enemies = []
for e in range(6):
    enemies.append(Enemy("circle", "red", -100, 0))

allies = []
for a in range(6):
    enemies.append(Ally("square", "blue", 100, 0))

particles = []
for i in range(20):
    particles.append(Particle("circle", "orange", 0, 0))

# keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelelate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()




# main game loop
while True:
    turtle.update()
    time.sleep(0.02)
    player.move()
    # enemy.move()
    missile.move()
    # ally.move()

    for enemy in enemies:
        enemy.move()

        # check for collision with player
        if player.is_collision(enemy):
            # play explosion sound
            # os.system("afplay explosion.mp3&")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250) 
            enemy.goto(x, y)
            game.score -= 100
            game.show_status()
       
        if missile.is_collision(enemy):
            # play missile sound
            # os.system("afplay explosion.mp3&")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            # increase score
            game.score += 100
            game.show_status()
            # do the explosion
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())
                

    for ally in allies:
        ally.move()
        
        # check for collision between missile and ally
        if missile.is_collision(ally):
            # play missile sound
            # os.system("afplay explosion.mp3&")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            # decrease the score
            game.score -= 50
            game.show_status()
            
    for particle in particles:
        particle.move()
           
               

  


  
    
    
   



turtle.exitonclick()

