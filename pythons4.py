import pygame
import random
import math

pygame.init()


WIDTH, HEIGHT = 1200, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I Love You Heart")


clock = pygame.time.Clock()


font = pygame.font.SysFont("Arial", 22, bold=True)


TEXT = "ILoveYou"

POINTS = 1700


CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2



# -----------------------------------
# Создаем сердце
# -----------------------------------

heart = []


for i in range(POINTS):

    t = random.uniform(0, math.pi * 2)


    x = 16 * math.sin(t) ** 3


    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )


    # немного внутрь сердца
    inside = random.uniform(0.72, 1.0)


    scale = 22


    tx = CENTER_X + x * scale * inside

    ty = CENTER_Y - y * scale * inside


    heart.append((tx, ty))



# -----------------------------------
# Частицы текста
# -----------------------------------

particles = []


for tx, ty in heart:


    particles.append({

        "x": random.uniform(-500, WIDTH + 500),

        "y": random.uniform(-500, HEIGHT + 500),


        "tx": tx,

        "ty": ty,


        "speed": random.uniform(0.03, 0.08),


        "offset":
            random.uniform(0, math.pi * 2)

    })



time = 0



# -----------------------------------
# Главный цикл
# -----------------------------------

running = True


while running:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False



    screen.fill((8, 0, 18))



    # дыхание сердца

    pulse = 1 + math.sin(time * 2) * 0.035



    for p in particles:



        # собираем сердце

        p["x"] += (
            p["tx"] - p["x"]
        ) * p["speed"]


        p["y"] += (
            p["ty"] - p["y"]
        ) * p["speed"]



        draw_x = p["x"]

        draw_y = p["y"]



        # -----------------------------------
        # движение текста
        # -----------------------------------


        # плавное покачивание

        wave_x = math.sin(
            time * 2 + p["offset"]
        ) * 2


        wave_y = math.cos(
            time * 2 + p["offset"]
        ) * 2



        # маленькое кружение вокруг точки

        radius = 1.5


        circle_angle = (
            time * 2 +
            p["offset"]
        )


        orbit_x = math.cos(circle_angle) * radius

        orbit_y = math.sin(circle_angle) * radius



        draw_x += wave_x + orbit_x

        draw_y += wave_y + orbit_y



        # пульсация

        draw_x = (
            CENTER_X +
            (draw_x - CENTER_X) *
            pulse
        )


        draw_y = (
            CENTER_Y +
            (draw_y - CENTER_Y) *
            pulse
        )



        # -----------------------------------
        # цвет
        # -----------------------------------

        color = (

            255,

            random.randint(100, 190),

            random.randint(180, 255)

        )



        text = font.render(
            TEXT,
            True,
            color
        )



        # -----------------------------------
        # легкий поворот каждой надписи
        # -----------------------------------

        rotate = math.sin(
            time * 2 +
            p["offset"]
        ) * 12

        text = pygame.transform.rotozoom(
            text,
            rotate,
            1
        )

        rect = text.get_rect(
            center=(
                draw_x,
                draw_y
            )
        )

        screen.blit(
            text,
            rect
        )

    pygame.display.flip()

    time += 0.03

    clock.tick(60)

pygame.quit()