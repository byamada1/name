# Simple pygame program

# Import and initialize the pygame library
import pygame
import math
import random

# classes
import fighter
import box

# serial commands
#import commands

# defining modes (different screens)
START = 0
CREATE = 1
BATTLE = 2
LEVEL = 3
CHOOSE = 4

def update_screen():
    global left_info, right_info
    global buttons
    #draws background
    screen.fill((255,255,255));
    

    display_mode()

    font = pygame.font.SysFont(None, 24)
    img = font.render(f"Target FPS: {FPS}", True, (0,0,0))
    screen.blit(img, (60, 20))
    
    #Update the display
    pygame.display.update()
    fpsClock.tick(FPS)

def display_mode():
    global mode
    # choosing button text
    if(mode == BATTLE):
        for index in range(len(buttons)):
            button = buttons[index]
            screen.fill(button.color, button.rect)
            # text for box
            font = pygame.font.SysFont(None, 36)
            img = font.render(battle_labels[index], True, button.text_color)
            screen.blit(img, (button.rect.left + 10, button.rect.top + 10))

    elif(mode == LEVEL):
        for index in range(len(buttons)):
            button = buttons[index]
            screen.fill(button.color, button.rect)
            # text for box
            font = pygame.font.SysFont(None, 36)
            img = font.render(level_labels[index], True, button.text_color)
            screen.blit(img, (button.rect.left + 10, button.rect.top + 10))

    elif(mode == CHOOSE):
        for index in range(len(buttons)):
            button = buttons[index]
            screen.fill(button.color, button.rect)
            # text for box
            font = pygame.font.SysFont(None, 36)
            img = font.render(switch_labels[index], True, button.text_color)
            screen.blit(img, (button.rect.left + 10, button.rect.top + 10))
        
    
    if(mode == LEVEL or mode == BATTLE or mode == CHOOSE):
        if(left != -1):
            # draw player
            screen.blit(fighters[left].sprite, (200, 100))

            # draw player info
            for l_info in left_info:
                screen.fill(l_info.color, l_info.rect)
                # text for box
                font = pygame.font.SysFont(None, 36)
                img = font.render(l_info.text, True, l_info.text_color)
                screen.blit(img, (l_info.rect.left + 10, l_info.rect.top + 10))    
            
            # draw attack stat symbols
            screen.blit(img_atk, (150, 160))
            # drawing def stat symbol
            screen.blit(img_def, (150, 210))
        else:
            screen.fill((255,255,255), pygame.Rect(0,150,600,400))

    if(mode == BATTLE or mode == CHOOSE):
        # draw enemy
        if(right != -1):
            screen.blit(pygame.transform.flip(fighters[right].sprite, True, False), (700, 100))
            
            # draw enemy info
            for r_info in right_info:
                screen.fill(r_info.color, r_info.rect)
                # text for box
                font = pygame.font.SysFont(None, 36)
                img = font.render(r_info.text, True, r_info.text_color)
                screen.blit(img, (r_info.rect.left + 10, r_info.rect.top + 10))
            
            # draw attack stat symbols
            screen.blit(pygame.transform.flip(img_atk, True, False), (1080, 160))
            # drawing def stat symbol
            screen.blit(pygame.transform.flip(img_def, True, False), (1080, 210))
            
        else:
            screen.fill((255,255,255), pygame.Rect(700,150,600,400))

def handle_click(event):
    global buttons
    global mode
    global right, left

    print("mode: " + str(mode))
    for index in range(len(buttons)):
        if(buttons[index].rect.collidepoint(event.pos)):
            if(mode == BATTLE):
                if(index == 0):
                    attack()
                    
                elif (index == 1):
                    switch_player()
                elif (index == 2):
                    print("button2")
                    add_weapon(0, 5)
                    add_weapon(2,50)
                elif (index == 3):
                    print("set")
                    set_enemy()
                elif (index == 4):
                    print("clear")
                    clear_enemy()
                elif (index == 5):
                    heal_all()
                elif (index == 6):
                    mode = CHOOSE

            elif(mode == LEVEL):
                if(index == 0):
                    fighters[left].atk_min += 5
                    fighters[left].atk_max += 10
                if(index == 1):
                    fighters[left].arm += 5
                if(index == 2):
                    fighters[left].hp_max += 25
                    fighters[left].hp += 25
                if(index == 4):
                    fighters[left].hp_max += random.randint(-25,25)
                    fighters[left].arm += random.randint(-25,25)
                    fighters[left].atk_min += random.randint(-25,25)
                    fighters[left].atk_max += random.randint(-25,25)
                    
                
                update_info()
                print("info updated")
                mode = BATTLE
                heal_all()
            
            elif(mode == CHOOSE):
                if(index == 0):
                    left = (left + 1) % len(fighters)
                elif(index == 1):
                    right = (right + 1) % len(fighters)    
                elif(index == 5):
                    if(left != right):
                        mode = BATTLE    
                update_info()
                    

    print(event.pos)

def update_health():
    print("updating health")
    left_info[1].rect.width = int(150 * (fighters[left].hp / fighters[left].hp_max))
    left_info[1].text = str(fighters[left].hp) + '/' + str(fighters[left].hp_max)
    right_info[1].rect.width = int(150 * (fighters[right].hp / fighters[right].hp_max))
    right_info[1].text = str(fighters[right].hp) + '/' + str(fighters[right].hp_max)

def attack():
    global left, right, mode
    print("Attacking")

    if(left != -1 and right != -1 ):
        if(fighters[left].hp > 0):
            left_hit = random.randint(fighters[left].atk_min + fighters[left].weapon_atk, fighters[left].atk_max + fighters[left].weapon_atk)
            left_hit -= fighters[right].arm + fighters[right].armor_arm
            print("left attacks for " + str(left_hit))
            if(left_hit > 0):
                fighters[right].hp -= left_hit
    
        if(fighters[right].hp > 0):
            right_hit = random.randint(fighters[right].atk_min + fighters[right].weapon_atk, fighters[right].atk_max + fighters[right].weapon_atk)
            right_hit -= fighters[left].arm + fighters[left].armor_arm
            print("right attacks for " + str(right_hit))
            if(right_hit > 0):
                fighters[left].hp -= right_hit
    
        if(fighters[left].hp <= 0):
            fighters[left].hp = 0
        if(fighters[right].hp <= 0):
            fighters[right].hp = 0
            mode = LEVEL
            heal_all()
        

    update_health()    

def switch_player():
    global left_info, right_info
    global left, right
    print("switch")
    left += 1
    if(left == right):
        left += 1
    if(left == len(fighters)):
        left = 0

    left_info[2].text = fighters[left].atk_str
    left_info[3].text = fighters[left].arm_str
    left_info[4].text = fighters[left].name
    
    update_health()

def heal_all():
    
    for ft in fighters:
        ft.hp = ft.hp_max
    update_health()

def set_enemy():
    global right, saved_right
    if(right == -1):
        right = saved_right
    update_health()

def clear_enemy():
    global right, saved_right
    saved_right = right
    right = -1

def add_weapon(ft, power):
    global fighters
    fighters[ft].weapon_atk = power
    fighters[ft].update()
    update_info()

def update_info():
    global left_info, right_info

    update_fighters()

    left_info[1].text = str(fighters[left].hp) + "/" + str(fighters[left].hp_max)
    left_info[2].text = fighters[left].atk_str
    left_info[3].text = fighters[left].arm_str
    left_info[4].text = fighters[left].name
    
    right_info[1].text = str(fighters[right].hp) + "/" + str(fighters[right].hp_max)
    right_info[2].text = fighters[right].atk_str
    right_info[3].text = fighters[right].arm_str
    right_info[4].text = fighters[right].name

def update_fighters():
    for ft in fighters:
        ft.update()

pygame.init()

size = [1280, 720]

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode(size)

# loading images
SPRITE_WIDTH = 300
SPRITE_HEIGHT = 300

img_p0 = pygame.image.load('P1-Crouch.png')
img_p0 = pygame.transform.scale(img_p0, (SPRITE_WIDTH, SPRITE_HEIGHT))

img_p1 = pygame.image.load('P2-Attack1.png')
img_p1 = pygame.transform.scale(img_p1, (SPRITE_WIDTH, SPRITE_HEIGHT))

img_p2 = pygame.image.load('P3-Run1.png')
img_p2 = pygame.transform.scale(img_p2, (SPRITE_WIDTH, SPRITE_HEIGHT))

img_p3 = pygame.image.load('p4.png')
img_p3 = pygame.transform.scale(img_p3, (SPRITE_WIDTH, SPRITE_HEIGHT))

img_p4 = pygame.image.load('p5.png')
img_p4 = pygame.transform.scale(img_p4, (SPRITE_WIDTH, SPRITE_HEIGHT))

img_p5 = pygame.image.load('p6.png')
img_p5 = pygame.transform.scale(img_p5, (SPRITE_WIDTH, SPRITE_HEIGHT))

img_p6 = pygame.image.load('potato.png')
img_p6 = pygame.transform.scale(img_p6, (SPRITE_WIDTH, SPRITE_HEIGHT))

#img_atk = pygame.image.load('attack_stat.png')
img_atk = pygame.image.load('atk.png')
img_atk = pygame.transform.scale(img_atk, (int(SPRITE_WIDTH/6), int(SPRITE_HEIGHT/6)))

#img_def = pygame.image.load('def_stat.png')
img_def = pygame.image.load('def.png')
img_def = pygame.transform.scale(img_def, (int(SPRITE_WIDTH/6), int(SPRITE_HEIGHT/6)))


buttons = []

buttons.append(box.box(pygame.Rect(50,600,180,80), (255,0,0), "", (255,255,255)))
buttons.append(box.box(pygame.Rect(250,600,180,80), (128,128,128), "", (255,255,255)))
buttons.append(box.box(pygame.Rect(450,600,180,80), (128,128,128), "", (255,255,255)))
buttons.append(box.box(pygame.Rect(650,600,180,80), (128,128,128), "", (255,255,255)))
buttons.append(box.box(pygame.Rect(850,600,180,80), (128,128,128), "", (255,255,255)))
buttons.append(box.box(pygame.Rect(1050,600,180,80), (128,230,128), "", (255,255,255)))
buttons.append(box.box(pygame.Rect(1130,25,100,50), (128,128,128), "", (255,255,255)))

battle_labels = ["Attack", "Switch", "Add Weapon", "Set", "Clear", "Heal All", "Switch"]
level_labels= ["ATK", "DEF", "HP", "??", "ö█.öÅ", "Reset",""]
switch_labels = ["Left", "Right", "", "", "", "Confirm", ""]

#################################################################################################################################

# move remaining buttons to left/right
# add update function (?)
# hide missing?
# 

# fighters
fighters = []
# name, atk min/max, arm, hp
fighters.append(fighter.fighter("sitter", 10, 20, 5, 150, img_p0))
fighters.append(fighter.fighter("shitter", 5, 25, 0, 150, img_p1))
fighters.append(fighter.fighter("naruto", 0, 50, 0, 100, img_p2))
fighters.append(fighter.fighter("₧UÄ»╖σb½", random.randint(-10,30), random.randint(30,90), random.randint(-50,50), random.randint(50,500), img_p3))
fighters.append(fighter.fighter(":(", random.randint(0,20), random.randint(20,30), random.randint(0,5), random.randint(100,200), img_p4))
fighters.append(fighter.fighter("3 or some shit", 4, 44, 4, 444, img_p5))
fighters.append(fighter.fighter(";)", 20, 50, 15, 500, img_p6))

left = 0
right = 1
saved_right = right

# background of health
# health+name
# attack
# defense
left_info = []
left_info.append(box.box(pygame.Rect(280,410,150,50), (128,128,128), "", (0,0,0)))
left_info.append(box.box(pygame.Rect(280,410,150,50), (255,0,0), "", (0,0,0)))
left_info.append(box.box(pygame.Rect(0,160,150,50), (220,50,50), "", (0,0,0)))
left_info.append(box.box(pygame.Rect(0,210,150,50), (50,80,220), "", (0,0,0)))
left_info.append(box.box(pygame.Rect(280,360,150,50), (255,255,255), "", (0,0,0)))


right_info = []
right_info.append(box.box(pygame.Rect(790,410,150,50), (128,128,128), "", (0,0,0)))
right_info.append(box.box(pygame.Rect(790,410,150,50), (255,0,0), "", (0,0,0)))
right_info.append(box.box(pygame.Rect(1130,160,150,50), (220,50,50), "", (0,0,0)))
right_info.append(box.box(pygame.Rect(1130,210,150,50), (50,80,220), "", (0,0,0)))
right_info.append(box.box(pygame.Rect(790,360,150,50), (255,255,255), "", (0,0,0)))

update_info()

mode = BATTLE

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