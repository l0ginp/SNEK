import pygame
import time
import random
import pygame_menu

DIFFICULTY = 10

pygame.init()
width,height=800,600#screen
disp=pygame.display.set_mode((width,height))
pygame.display.set_caption("SNEK")
green,red,black,white=(0,204,153),(255,8,0),(0,0,0),(255,255,255)
font_style=pygame.font.SysFont(None,30)
cell=20

def set_difficulty(value, difficulty):
    global DIFFICULTY
    DIFFICULTY = difficulty
    return DIFFICULTY

def get_food_position(width, height, body):
    while True:
        food_x=round(random.randrange(0,width-cell)/cell)*cell
        food_y=round(random.randrange(0,height-cell)/cell)*cell

        if [food_x, food_y] not in body:
            return food_x, food_y

def gameloop():
    end=0
    x,y,x1,y1=width/2,height/2,0,0#x,y->head pos;x1,y1->change in pos
    snake_speed=DIFFICULTY
    body,blen=[],1
    clk=pygame.time.Clock()
    food_x, food_y= get_food_position(width,height, body)
    while not end:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end=1
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x1,y1=-cell,0
                elif event.key==pygame.K_UP:
                    x1,y1=-0,-cell
                elif event.key==pygame.K_RIGHT:
                    x1,y1=cell,0
                elif event.key==pygame.K_DOWN:
                    x1,y1=0,cell
        x+=x1;y+=y1
        if x>width or x<0 or y>height or y<0:#screen boundary condition
            break
        disp.fill(black)
        pygame.draw.rect(disp,red,[food_x,food_y,cell,cell])
        head=[]
        head.append(x);head.append(y)
        body.append(head)#append new head to body
        for block in body[:blen-1]:
            if block==head:#snake head touches body
                end=1
        if len(body)>blen:#snake movement display
            del body[0]
        for block in body:
            pygame.draw.rect(disp,green,[block[0],block[1],cell,cell])
        score=font_style.render("Score: "+str(blen-1),True,white)
        disp.blit(score,[0,0])
        pygame.display.update()
        if food_x==x and food_y==y:#contact with food
            food_x, food_y= get_food_position(width,height, body)
            blen+=1#body length increases
            if snake_speed<30:
                snake_speed+=0.5
        clk.tick(snake_speed)#fps
    clk.tick(snake_speed)
    disp.fill(black)
    m=font_style.render("Game Over",True,red)
    disp.blit(m,[(width/2)-40,height/2])
    f_score=font_style.render("Score: "+str(blen-1),True,white)
    disp.blit(f_score,[(width/2)-30,(height/2)+27])
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()

if __name__ == "__main__":
    menu = pygame_menu.Menu('SNEK', 400, 300,
                       theme=pygame_menu.themes.THEME_SOLARIZED)

    menu.add.selector('Difficulty :', [('Nornal', 10), ('Hard', 24), ('Easy', 5)], onchange=set_difficulty)
    menu.add.button('Play', gameloop)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(disp)
    gameloop()