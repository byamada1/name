# Simple pygame program

# Import and initialize the pygame library
import pygame
import math
import random

import fighter
import box

pygame.init()

size = [1280, 720]

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode(size)

# box+color+other -> function?

buttons = []
#f1 = pygame.Rect(50,600,180,80)
#f2 = (255,0,0)
#f3 = "Attack"
#f4 = (255,255,255)
buttons.append(box.box(pygame.Rect(50,600,180,80), (255,0,0), "Attack", (255,255,255)))
buttons.append(box.box(pygame.Rect(250,600,180,80), (128,128,128), "button 1", (255,255,255)))
buttons.append(box.box(pygame.Rect(450,600,180,80), (128,128,128), "button 2", (255,255,255)))
buttons.append(box.box(pygame.Rect(650,600,180,80), (128,128,128), "button 3", (255,255,255)))
buttons.append(box.box(pygame.Rect(850,600,180,80), (128,128,128), "button 4", (255,255,255)))
buttons.append(box.box(pygame.Rect(1050,600,180,80), (128,128,128), "button 5", (255,255,255)))


#################################################################################################################################

# move remaining buttons to left/right
# add update function (?)
# hide missing?
# 

boxes = []
box_colors = []
box_text = []
box_text_color = []

# button 6 (player tag)
boxes.append(pygame.Rect(230,410,150,50))
box_colors.append((128,128,128))
box_text.append("")
box_text_color.append((0,0,0))

# button 7 (player health)
boxes.append(pygame.Rect(230,410,150,50))
box_colors.append((255,0,0))
box_text.append("player")
box_text_color.append((0,0,0))

# button 8 (enemy tag)
boxes.append(pygame.Rect(840,410,150,50))
box_colors.append((128,128,128))
box_text.append("")
box_text_color.append((0,0,0))

# button 9 (enemy health)
boxes.append(pygame.Rect(840,410,150,50))
box_colors.append((255,0,0))
box_text.append("enemy")
box_text_color.append((0,0,0))

# button 10 (player attack)
boxes.append(pygame.Rect(0,260,150,50))
box_colors.append((220,50,50))
box_text.append("10-20")
box_text_color.append((0,0,0))

# button 11 (enemy attack)
boxes.append(pygame.Rect(1130,260,150,50))
box_colors.append((220,50,50))
box_text.append("5-25")
box_text_color.append((0,0,0))

# button 12 (player def)
boxes.append(pygame.Rect(0,310,150,50))
box_colors.append((50,80,220))
box_text.append("5")
box_text_color.append((0,0,0))

# button 13 (enemy Def)
boxes.append(pygame.Rect(1130,310,150,50))
box_colors.append((50,80,220))
box_text.append("10")
box_text_color.append((0,0,0))

# fighters
fighters = []

fighters.append(fighter.fighter("sitter", 10, 20, 5, 150))
fighters.append(fighter.fighter("shitter", 5, 25, 0, 150))

left = fighters[0]
right = fighters[1]

SPRITE_WIDTH = 300
SPRITE_HEIGHT = 300

img_crouch = pygame.image.load('P1-Crouch.png')
img_crouch = pygame.transform.scale(img_crouch, (SPRITE_WIDTH, SPRITE_HEIGHT))

img_enemy = pygame.image.load('P2-Attack1.png')
img_enemy = pygame.transform.flip(pygame.transform.scale(img_enemy, (SPRITE_WIDTH, SPRITE_HEIGHT)), True, False)

img_atk = pygame.image.load('attack_stat.png')
img_atk = pygame.transform.scale(img_atk, (int(SPRITE_WIDTH/6), int(SPRITE_HEIGHT/6)))

img_def = pygame.image.load('def_stat.png')
img_def = pygame.transform.scale(img_def, (int(SPRITE_WIDTH/6), int(SPRITE_HEIGHT/6)))

def update_screen():
    global boxes
    global buttons
    #draws background
    screen.fill((255,255,255));
    
    # filling in rectangles
    for index in range(len(boxes)):
        screen.fill(box_colors[index], boxes[index])
        # text for box
        font = pygame.font.SysFont(None, 36)
        img = font.render(box_text[index], True, box_text_color[index])
        screen.blit(img, (boxes[index].left + 10, boxes[index].top + 10))

    for button in buttons:
        screen.fill(button.color, button.rect)
        # text for box
        font = pygame.font.SysFont(None, 36)
        img = font.render(button.text, True, button.text_color)
        screen.blit(img, (button.rect.left + 10, button.rect.top + 10))
    
    # draw player
    screen.blit(img_crouch, (150, 120))
    # draw enemy
    screen.blit(img_enemy, (750, 100))
    # draw attack stat symbols
    screen.blit(img_atk, (150, 260))
    screen.blit(pygame.transform.flip(img_atk, True, False), (1070, 260))

    screen.blit(img_def, (150, 310))
    screen.blit(img_def, (1070, 310))

    font = pygame.font.SysFont(None, 24)
    img = font.render(f"Target FPS: {FPS}", True, (0,0,0))
    screen.blit(img, (60, 20))
    
    #Update the display
    pygame.display.update()
    fpsClock.tick(FPS)

def handle_click(event):
    global buttons

    for index in range(len(buttons)):
        if(buttons[index].rect.collidepoint(event.pos)):
            print("in ", index)
            if(index == 0):
                print("attack")
                #boxes[9].width -= random.randint(10,20)
                #boxes[7].width -= random.randint(5,25)
                
            elif (index == 1):
                print("heal or something")
                #boxes[9].width = 150
                #boxes[7].width = 150
        

    print(event.pos)


# Run until the user asks to quit
running = True

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_END:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event)

    #Draw the screen
    update_screen()
    

# Done! Time to quit.
pygame.quit()