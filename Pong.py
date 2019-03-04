import pygame as pg
import sys,random
from pygame.locals import *

# INITIALIZE GLOBALS
WIDTH = 800
HEIGHT = 600
BALL_RADIUS = 12
PAD_WIDTH = 8
PAD_HEIGHT = 80
LEFT = False
RIGHT = True
paddle1_pos = HEIGHT/2 # stores Y-coordinate of the centre of paddle1
paddle2_pos = HEIGHT/2 # stores Y-coordinate of the centre of paddle2
paddle1_vel = 0
paddle2_vel = 0
ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [24,20]
BLACK = (0,0,0)
WHITE = (255,255,255)


def iround(x):
	return int(round(x))

def spawn_ball(direction):
	# global ball_pos, ball_vel # these are vectors stored as lists
	ball_pos[0] = WIDTH/2
	ball_pos[1] = HEIGHT/2
	ball_vel[0] = random.randrange(120,240)/fps
	ball_vel[1] = -1*random.randrange(60,180)/fps
	if direction == LEFT:
		ball_vel[0] = -1*ball_vel[0]

def new_game():
	global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
	global score1, score2
	score1 = 0
	score2 = 0
	paddle1_pos = HEIGHT/2
	paddle2_pos = HEIGHT/2
	paddle1_vel = 0
	paddle2_vel = 0
	spawn_ball(LEFT)

def updateBall():
	ball_pos[0] += ball_vel[0]
	ball_pos[1] += ball_vel[1]
	ball_pos[0] = iround(ball_pos[0])
	ball_pos[1] = iround(ball_pos[1])
	if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
		ball_vel[1] = -1*ball_vel[1]

def updatePaddle():
	global paddle1_pos,paddle2_pos

	paddle1_pos += paddle1_vel
	paddle2_pos += paddle2_vel
	if paddle1_pos > HEIGHT - PAD_HEIGHT//2:
		paddle1_pos = HEIGHT - PAD_HEIGHT//2
	if paddle1_pos < PAD_HEIGHT//2:
		paddle1_pos = PAD_HEIGHT//2
	if paddle2_pos > HEIGHT - PAD_HEIGHT//2:
		paddle2_pos = HEIGHT - PAD_HEIGHT//2
	if paddle2_pos < PAD_HEIGHT//2:
		paddle2_pos = PAD_HEIGHT//2

	paddle1_pos = iround(paddle1_pos)
	paddle2_pos = iround(paddle2_pos)

def detectCollision():
	global score1, score2
	collided = False
	if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:	#paddle 1
		if abs(ball_pos[1]-paddle1_pos) <= PAD_HEIGHT//2 + BALL_RADIUS - 5:
			ball_vel[0] = -1.05*ball_vel[0]
			collided = True
		else:
			score2 += 1
			spawn_ball(RIGHT)
	elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:	#paddle 2
		if abs(ball_pos[1]-paddle2_pos) <= PAD_HEIGHT//2 + BALL_RADIUS - 5:
			ball_vel[0] = -1.05*ball_vel[0]
			collided = True
		else:
			score1 += 1
			spawn_ball(LEFT)
	return collided

def draw(canvas):
		
	# draw mid line and gutters
	pg.draw.line(canvas,WHITE,[WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
	pg.draw.line(canvas,WHITE,[PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
	pg.draw.line(canvas,WHITE,[WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)

	updateBall()

	# draw ball
	pg.draw.circle(canvas,WHITE,ball_pos, BALL_RADIUS,0)

	updatePaddle()

	# draw paddles
	pg.draw.line(canvas,WHITE,[PAD_WIDTH//2,paddle1_pos-PAD_HEIGHT//2],[PAD_WIDTH//2,paddle1_pos+PAD_HEIGHT//2],PAD_WIDTH)
	pg.draw.line(canvas,WHITE,[WIDTH-PAD_WIDTH//2,paddle2_pos-PAD_HEIGHT//2],[WIDTH-PAD_WIDTH//2,paddle2_pos+PAD_HEIGHT//2],PAD_WIDTH)

	# determine whether paddle and ball collide    
	detectCollision()

	# draw scores
	score1_surf = myfont.render(str(score1),False,WHITE)
	score2_surf = myfont.render(str(score2),False,WHITE)
	canvas.blit(score1_surf,[WIDTH/4,HEIGHT/4])
	canvas.blit(score2_surf,[WIDTH- WIDTH/4,HEIGHT/4])

def keydown(key):
	global paddle1_vel, paddle2_vel
	acc = 8
	if key == pg.K_DOWN:
		paddle2_vel += acc

	if key == pg.K_UP:
		paddle2_vel -= acc

	if key == pg.K_w:
		paddle1_vel -= acc

	if key == pg.K_s:
		paddle1_vel += acc

def keyup(key):
	global paddle1_vel, paddle2_vel
	if key == pg.K_DOWN or key == pg.K_UP:
		paddle2_vel = 0
	if key == pg.K_w or key == pg.K_s:
		paddle1_vel = 0
def restart():
	new_game()

pg.init()

frame = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('Pong')
fps = 30
clock = pg.time.Clock()
myfont = pg.font.SysFont('Comic Sans MS',36)
new_game()

while True:
	frame.fill(BLACK)
	draw(frame)
	for event in pg.event.get():
		if event.type == QUIT:
			pg.quit()
			sys.exit()
		if event.type == pg.KEYDOWN:
			keydown(event.key)
		if event.type == pg.KEYUP:
			keyup(event.key)

	pg.display.update()
	clock.tick(fps)