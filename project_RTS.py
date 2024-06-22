import pygame
from random import randrange
import time


# Go, go, run!
def coords():
    return randrange(50, 451)


def create_rect(object, list):
    re = object.get_rect()
    re.center = (coords(), -50)
    list.append(re)


pygame.init()
WIDTH = 500
HEIGHT = 600
FPS = 30
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
run = True
gameMode = "main screen"
naruto = pygame.image.load("images/naruto.png").convert_alpha()
background = pygame.image.load("images/kanoha.jpg")
end = pygame.image.load("images/end.png")
start = pygame.image.load("images/start.png")
ramen = pygame.image.load("images/ramen.png").convert_alpha()
shuriken = pygame.image.load("images/shuriken.png").convert_alpha()
rect = naruto.get_rect()
x, y = 100, 550
rect.center = (x, y)
font = pygame.font.Font(None, 36)
button_rect = pygame.Rect(200, 200, 100, 25)
button_label = font.render("PLAY", True, (255, 255, 255))
button_rect2 = pygame.Rect(200, 230, 100, 25)
button_label2 = font.render("RULES", True, (255, 255, 255))
button_rect3 = pygame.Rect(200, 260, 100, 25)
button_label3 = font.render("TOP", True, (255, 255, 255))
res_rect = pygame.Rect(190, 150, 120, 30)
res_label = font.render("RESTART", True, (255, 255, 255))
back_rect = pygame.Rect(10, 10, 80, 30)
back_label = font.render("BACK", True, (255, 255, 255))

move_right = False
move_left = False
ramens = []
shurikens = []
timer = randrange(0, 10)
timer_2 = randrange(10, 20)
points = 0
life = 100
game_duration = 60
start_time = 0
rules = ["В этой игре вам предстоит играть за", "Наруто(персонаж) и собирать", "рамен(япоснкая лапша) и стараться",
         "не собирать сюрикены.", "Игра длится 60 секунд или", "до того момента пока вашa жизнь",
         "не станет нулевым."]
while run:
    if gameMode == 'main screen':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    gameMode = "game"
                    start_time = time.time()
                elif button_rect2.collidepoint(mouse_pos):
                    gameMode = 'rules'
                elif button_rect3.collidepoint(mouse_pos):
                    gameMode = 'top'
        window.blit(start, (0, 0))
        pygame.draw.rect(window, (0, 0, 0), button_rect)
        window.blit(button_label, (220, 200))
        pygame.draw.rect(window, (0, 0, 0), button_rect2)
        window.blit(button_label2, (210, 230))
        pygame.draw.rect(window, (0, 0, 0), button_rect3)
        window.blit(button_label3, (225, 260))
    elif gameMode == 'game':
        if time.time() - start_time > game_duration:
            gameMode = 'over'
            with open('results.txt', 'a') as writer:
                writer.write(str(points) + '\n')
        timer += 1
        timer_2 += 1
        if timer == 30:
            create_rect(ramen, ramens)
            timer = 0
        if timer_2 == 30:
            create_rect(shuriken, shurikens)
            timer_2 = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    move_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False
        window.blit(background, (0, 0))
        remaining_time = game_duration - (time.time() - start_time)
        text = font.render(f"Time: {remaining_time:.2f}", True, (0, 0, 0))
        window.blit(text, (10, 10))
        score = font.render(f"Score: {points}", True, (0, 0, 0))
        window.blit(score, (350, 10))
        score = font.render(f"Life: {life}", True, (255, 0, 0))
        window.blit(score, (350, 35))
        for r in ramens:
            window.blit(ramen, r)
            r.bottom += 10
            if rect.colliderect(r):
                ramens.remove(r)
                points += 10
        for sh in shurikens:
            window.blit(shuriken, sh)
            sh.bottom += 10
            if rect.colliderect(sh) and life == 10:
                gameMode = 'over'
                with open('results.txt', 'a') as writer:
                    writer.write(str(points) + '\n')
            elif rect.colliderect(sh):
                shurikens.remove(sh)
                life -= 10
        if move_right and rect.left <= WIDTH - naruto.get_size()[0]:
            x += 10
        if move_left and rect.left >= 0:
            x -= 10
        rect.left = x
        window.blit(naruto, rect)
    elif gameMode == 'rules':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos):
                    gameMode = "main screen"
        window.blit(start, (0, 0))
        pygame.draw.rect(window, (0, 0, 0), back_rect)
        window.blit(back_label, (15, 15))
        text = font.render("Правила:", True, (0, 0, 0))
        window.blit(text, (200, 180))
        line = 210
        for i in rules:
            text = font.render(i, True, (0, 0, 0))
            window.blit(text, (10, line))
            line += 20
    elif gameMode == 'top':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos):
                    gameMode = "main screen"
        try:
            with open('results.txt', 'r') as reader:
                results = list(map(int, reader.readlines()))
        except FileNotFoundError:
            results = [0]
        window.blit(start, (0, 0))
        pygame.draw.rect(window, (0, 0, 0), back_rect)
        window.blit(back_label, (15, 15))
        text = font.render(f"Top score: {max(results)}", True, (0, 0, 0))
        window.blit(text, (150, 200))
    elif gameMode == 'over':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if res_rect.collidepoint(mouse_pos):
                    gameMode = "main screen"
                    move_right = False
                    move_left = False
                    ramens = []
                    shurikens = []
                    timer = randrange(0, 10)
                    timer_2 = randrange(0, 10)
                    points = 0
                    life = 100
        window.blit(end, (0, 0))
        score = font.render(f"Score: {points}", True, (0, 0, 0))
        window.blit(score, (350, 10))
        pygame.draw.rect(window, (0, 0, 0), res_rect)
        window.blit(res_label, (195, 155))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
