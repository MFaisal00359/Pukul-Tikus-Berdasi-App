import pygame
import os
import random
from os import path
from pygame. locals import *

# game_folder = os.path.dirname(__file__)
# img_folder = os.path.join(game_folder, 'Image')

# SETTING WINDOW GAME
width, height = 1000,700
window = pygame.display.set_mode((width,height))
FPS = 60

# SETTING VARIABEL COLOUR/WARNA
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# GRID MOLE HOLE
COL = 3
ROW = 3

def random_tikus_posisi():
    random_tanah = random.choice(tanah_list_rect)
    tikus_rect.midbottom = random_tanah.midtop

def draw_tanah():
    x, y = 0, 0
    for row in range(ROW):
        x = 0
        for col in range(COL):
            screen.blit(tanah, (x * 180 + 250, y * 200 + 120))
            rect = pygame.Rect(x * 180 + 250, y * 200 + 160, 130, 60)
            # pygame.draw.rect(screen, BLUE, (rect))
            tanah_list_rect.append(rect)
            x+=1
        y+=1

def draw_text(text, font_size, font_color, x, y):
    font = pygame.font.SysFont(None, font_size)
    font_surface = font.render(text, True, font_color)
    screen.blit(font_surface, (x, y))

pygame. init() 
pygame.mixer.init()

screen =pygame.display.set_mode((width, height))

bg_img = pygame.image.load('background.png')
bg_img = pygame.transform.scale(bg_img,(width, height))
 
# CAPTION
pygame.display.set_caption("Pukul Tikus Berdasi")
clock = pygame.time.Clock()

# game variables
mouse_position = (0, 0)
pygame.mouse.set_visible(False)
hitung_mundur = 5
last_update = pygame.time.get_ticks()
score = 0

# load sounds
pop_sfx = pygame.mixer.Sound("../Pukul-Tikus-Berdasi-main/Audios/Pop.mp3")

# Load images tikus
tikus = pygame.transform.scale(pygame.image.load("../Pukul-Tikus-Berdasi-main/Image/tikus.png"), (100, 100))
tikus_rect = tikus.get_rect()

# Load images tanah
tanah = pygame.transform.scale(pygame.image.load("../Pukul-Tikus-Berdasi-main/Image/tanah.png").convert_alpha(), (130, 100))

tanah_list_rect = []

# Load images palu
# array animasi palu
animasi_palu = []
for i in range(1, 3):
    img_palu = pygame.image.load("../Pukul-Tikus-Berdasi-main/Image/palu{}.png". format(i)).convert_alpha()
    animasi_palu.append(img_palu)

load_palu = animasi_palu[0]
palu_rect = load_palu.get_rect()

i = 0
runing = True
while runing:
    window.blit(bg_img,(0,0))
    i-=1
    for event in pygame.event.get():
        if event.type == QUIT:
            runing = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if tikus_rect.collidepoint(mouse_position):
                    pop_sfx.play()
                    score += 1
                    random_tikus_posisi()
                else:
                    random_tikus_posisi()
                load_palu = animasi_palu[1]
                
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                load_palu = animasi_palu[0]

        mouse_position = pygame.mouse.get_pos()
        palu_rect.center = (mouse_position[0], mouse_position[1])
    
    now = pygame.time.get_ticks()
    if now - last_update > 1000 and hitung_mundur > 0:
        last_update = now
        hitung_mundur -= 1
        random_tikus_posisi()

    if hitung_mundur > 0:
        draw_text(str(hitung_mundur), 60, WHITE, width//2, 20)
    else:
        screen.blit(tikus, tikus_rect)
        draw_text(f"Score: {score}", 60, WHITE, 10, 20)
    draw_tanah()
    screen.blit(load_palu, palu_rect)

    pygame.display.update()
pygame.quit()
        