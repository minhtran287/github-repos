import pgzrun
import random

WIDTH = 400
HEIGHT = 500

GRAVITY = 0.3
GAP = 130
SPEED = 3
current_speed = SPEED
FLAP_VELOCITY = -6.5

bird = Actor('bird1', (75, 200))
pipe_top = Actor('top', anchor=('left', 'bottom'))
pipe_bottom = Actor('bottom', anchor=('left', 'top'))

score = 0
high_score = 0
game_started = False
pipe_scored = False

bird.dead = False
bird.vy = 0


def draw():
    screen.blit('background', (0, 0))

    pipe_top.draw()
    pipe_bottom.draw()
    bird.draw()

    
    if not game_started:
        screen.draw.text(
        "FLAPPY BIRD",
        center=(WIDTH // 2, 150),
        fontsize=100,
        fontname="flappy",
        color="yellow"
        )

        screen.draw.text(
        "Press SPACE to start",
        center=(WIDTH // 2, 250),
        fontsize=60,
        fontname="flappy",
        color="white"
        )   
    
    screen.draw.text(
        "Score: " + str(score),
        (20, 20),
        fontsize=40,
        color="white"
    )

    screen.draw.text(
    "High Score: " + str(high_score),
    (20, 60),
    fontsize=30,
    color="white"
)
    
    if bird.dead:
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=100,
            fontname="flappy",
            color="red"
        )

        screen.draw.text(
            "Press R to restart",
            center=(WIDTH // 2, HEIGHT // 2 + 55),
            fontsize=60,
            fontname="flappy",
            color="white"
        )


def reset_pipes():
    global pipe_scored

    pipe_gap_y = random.randint(200, HEIGHT - 200)

    pipe_top.pos = (WIDTH, pipe_gap_y - GAP // 2)
    pipe_bottom.pos = (WIDTH, pipe_gap_y + GAP // 2)

    pipe_scored = False


def update_bird():
    bird.vy += GRAVITY
    bird.y += bird.vy
    bird.x = 75

    if not bird.dead:
        if bird.vy < -3:
            bird.image = 'bird2'
        else:
            bird.image = 'bird1'

    
    if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom):
        bird.dead = True
        bird.image = 'birddead'

    
    if bird.y < 0 or bird.y > HEIGHT:
        bird.dead = True
        bird.image = 'birddead'


def update_pipes():
    global score
    global high_score
    global pipe_scored
    global current_speed

    if not bird.dead:
        pipe_top.left -= current_speed
        pipe_bottom.left -= current_speed

       
        if pipe_top.right < bird.x and not pipe_scored:
            score += 1
            pipe_scored = True

            
            if score > high_score:
                high_score = score

            
            current_speed = SPEED + (score // 5) * 0.25

        if pipe_top.right < 0:
            reset_pipes()


def update():
    if game_started and not bird.dead:
        update_pipes()
        update_bird()


def on_key_down(key):
    global score
    global game_started

    
    if key == keys.SPACE and not game_started:
        game_started = True
        bird.vy = FLAP_VELOCITY

    
    elif key == keys.SPACE and not bird.dead:
        bird.vy = FLAP_VELOCITY

    
    elif key == keys.R and bird.dead:
        score = 0
        bird.pos = (75, 200)
        bird.dead = False
        bird.vy = 0
        bird.image = 'bird1'

        reset_pipes()

        
        game_started = False

pgzrun.go()