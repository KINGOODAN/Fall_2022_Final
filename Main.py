from Map import *
from Home import *
from Rooms import *
from Player import *
from Monster import *

import pygame

pygame.init()
pygame.display.set_caption("Wave Function Collapse")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenX, screenY = screen.get_size()
Running = True

YTC = 10
XTC = int(YTC * 1.5)

roomList: list[room] = []

grid = makeGrid(screenX, screenY, screen, XTC, YTC)

ranX = random.randint(0, XTC - 1)
ranY = random.randint(0, YTC - 1)

while True:
    if grid[ranY][ranX].tile.sides == [0, 0, 0, 0]:
        ranX = random.randint(0, XTC)
        ranY = random.randint(0, YTC)
    else:
        MapXPos = ranX
        MapYPos = ranY
        break

player = pygame.Rect(screenX // 2, screenY // 2, 50, 100)

PlayerSpeed = int(screenX // 750)
print(screenX)
print(PlayerSpeed)

for i in range(YTC):
    roomList.append([])
    for j in range(XTC):
        roomList[i].append(
            room(
                0,
                grid[i][j].tile.sides,
                grid[i][j].tile.ID,
                screenX,
                screenY,
                screen,
                (player.width, player.height),
            )
        )

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    screen.fill((0, 0, 0))

    roomList[MapYPos][MapXPos].draw()

    pygame.draw.rect(screen, (255, 0, 0), player)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        while True:
            screen.fill((0, 0, 0))
            start(screenY, XTC, YTC)
            if keys[pygame.K_LSHIFT]:
                break
    if keys[pygame.K_LCTRL]:
        Running = False

    if player.x == 0 and grid[MapYPos][MapXPos].tile.sides[3] == 1:
        MapXPos -= 1
        player.x = screenX - player.w - 10
    if player.x == screenX - player.w and grid[MapYPos][MapXPos].tile.sides[1] == 1:
        MapXPos += 1
        player.x = 10
    if player.y == 0 and grid[MapYPos][MapXPos].tile.sides[0] == 1:
        MapYPos -= 1
        player.y = screenY - player.h - 10
    if player.y == screenY - player.h and grid[MapYPos][MapXPos].tile.sides[2] == 1:
        MapYPos += 1
        player.y = 10

    # player.colliderect(roomList[MapYPos][MapXPos].center_square)

    if (
        keys[pygame.K_a]
        and player.left >= 0
        and roomList[MapYPos][MapXPos].collision(player)
    ):
        player.x -= PlayerSpeed
    if (
        keys[pygame.K_d]
        and player.right <= screenX
        and roomList[MapYPos][MapXPos].collision(player)
    ):
        player.x += PlayerSpeed
    if (
        keys[pygame.K_w]
        and player.top >= 0
        and roomList[MapYPos][MapXPos].collision(player)
    ):
        player.y -= PlayerSpeed
    if (
        keys[pygame.K_s]
        and player.bottom <= screenY
        and roomList[MapYPos][MapXPos].collision(player)
    ):
        player.y += PlayerSpeed

    pygame.display.flip()
