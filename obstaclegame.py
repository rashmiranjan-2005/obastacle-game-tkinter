import tkinter as tk
import random

root = tk.Tk()
root.title("Obstacle Game - Premium")

canvas = tk.Canvas(root, width=800, height=400, bg="white")
canvas.pack()

# Ground
ground = canvas.create_line(0, 350, 800, 350, width=3)

# Variables
velocity = 0
gravity = 0.8
game_over = False
score = 0
speed = 6

# Score
score_text = canvas.create_text(700, 30, text="Score: 0", font=("Arial", 14))

# Player (stick human)
head = canvas.create_oval(60, 270, 80, 290, fill="black")
body = canvas.create_line(70, 290, 70, 330, width=4)
arm1 = canvas.create_line(70, 300, 55, 315, width=3)
arm2 = canvas.create_line(70, 300, 85, 315, width=3)
leg1 = canvas.create_line(70, 330, 60, 350, width=3)
leg2 = canvas.create_line(70, 330, 80, 350, width=3)

# Obstacles
obstacles = []

def create_obstacle():
    obstacle_type = random.choice(["small", "big"])

    if obstacle_type == "small":
        height = 30
        obs = canvas.create_rectangle(800, 350-height, 830, 350, fill="red")
    else:
        height = 70
        obs = canvas.create_rectangle(800, 350-height, 830, 350, fill="purple")

    obstacles.append(obs)

# Create first obstacle
create_obstacle()

def jump(event):
    global velocity
    if canvas.coords(body)[3] >= 330:
        velocity = -15

root.bind("<space>", jump)

def move_player():
    canvas.move(head, 0, velocity)
    canvas.move(body, 0, velocity)
    canvas.move(arm1, 0, velocity)
    canvas.move(arm2, 0, velocity)
    canvas.move(leg1, 0, velocity)
    canvas.move(leg2, 0, velocity)

def reset_player():
    canvas.coords(head, 60, 270, 80, 290)
    canvas.coords(body, 70, 290, 70, 330)
    canvas.coords(arm1, 70, 300, 55, 315)
    canvas.coords(arm2, 70, 300, 85, 315)
    canvas.coords(leg1, 70, 330, 60, 350)
    canvas.coords(leg2, 70, 330, 80, 350)

def update():
    global velocity, game_over, score, speed

    if game_over:
        return

    velocity += gravity
    move_player()

    if canvas.coords(body)[3] > 330:
        reset_player()
        velocity = 0

    for obs in obstacles[:]:
        canvas.move(obs, -speed, 0)

        # When obstacle goes out
        if canvas.coords(obs)[2] < 0:
            canvas.delete(obs)
            obstacles.remove(obs)

            create_obstacle()  # ONLY ONE at a time

            score += 1
            if score % 5 == 0:
                speed += 1

            canvas.itemconfig(score_text, text=f"Score: {score}")

    # Collision detection
    player = canvas.bbox(head)

    for obs in obstacles:
        obs_pos = canvas.coords(obs)

        if (player[2] > obs_pos[0] and
            player[0] < obs_pos[2] and
            player[3] > obs_pos[1]):
            end_game()

    root.after(30, update)

def end_game():
    global game_over
    game_over = True

    canvas.create_text(400, 150, text="Obstacle Game Over", font=("Arial", 24))
    canvas.create_text(400, 200, text="Press ENTER to Restart", font=("Arial", 14))

def restart(event):
    global game_over, score, speed, velocity
    global head, body, arm1, arm2, leg1, leg2, obstacles, score_text, ground

    game_over = False
    score = 0
    speed = 6
    velocity = 0

    canvas.delete("all")

    ground = canvas.create_line(0, 350, 800, 350, width=3)

    score_text = canvas.create_text(700, 30, text="Score: 0", font=("Arial", 14))

    head = canvas.create_oval(60, 270, 80, 290, fill="black")
    body = canvas.create_line(70, 290, 70, 330, width=4)
    arm1 = canvas.create_line(70, 300, 55, 315)
    arm2 = canvas.create_line(70, 300, 85, 315)
    leg1 = canvas.create_line(70, 330, 60, 350)
    leg2 = canvas.create_line(70, 330, 80, 350)

    obstacles = []
    create_obstacle()

    update()

root.bind("<Return>", restart)

update()
root.mainloop()