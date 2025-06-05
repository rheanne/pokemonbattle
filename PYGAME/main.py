import pygame
import os


pygame.font.init()
pygame.mixer.init()
print(os.path.abspath(os.path.join('ASSETS', 'pokemonbattletheme.mp3')))

pygame.mixer.music.load(os.path.join('ASSETS','pokemonbattletheme.mp3')) # added background music
pygame.mixer.music.play(loops=15, start=0.0, fade_ms=0)

all_fonts = pygame.font.get_fonts()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("POKEMON BATTLE!")

GREEN = (102, 204, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(0, HEIGHT//2-5, WIDTH, 10)


CHAR_FIRE_SOUND = pygame.mixer.Sound(os.path.join('ASSETS', 'rawr.mp3' ))
PIKA_FIRE_SOUND = pygame.mixer.Sound(os.path.join('ASSETS', 'pikachu.mp3' ))
BOOM_HIT_SOUND = pygame.mixer.Sound(os.path.join('ASSETS', 'boom.wav'))


HEALTH_FONT = pygame.font.SysFont('arial', 40)
WINNER_FONT = pygame.font.SysFont('arial', 60)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
IMAGE_WIDTH, IMAGE_HEIGHT = 90, 75

CHARIZARD_HIT = pygame.USEREVENT + 1
PIKA1_HIT = pygame.USEREVENT + 2

CHARIZARD_IMAGE = pygame.image.load(
     os.path.join('ASSETS', 'charizard.png'))
CHARIZARD_IMAGE = pygame.transform.rotate(pygame.transform.scale(CHARIZARD_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT)), 0)

PIKA1_IMAGE = pygame.image.load(
     os.path.join('ASSETS', 'pika1.png'))
PIKA1_IMAGE = pygame.transform.rotate(pygame.transform.scale(PIKA1_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT)), 0 )

GRASS = pygame.transform.scale(pygame.image.load(os.path.join('ASSETS', 'grass.png')), (WIDTH, HEIGHT))
STADIUM = pygame.transform.scale(pygame.image.load(os.path.join('ASSETS', 'stadium.png' )), (WIDTH, HEIGHT))

def draw_window(charizard, pika1, pika1_bullets, charizard_bullets, charizard_health, pika1_health):
        WIN.blit(STADIUM, (0, 0))
        pygame.draw.rect(WIN, WHITE, BORDER)

        charizard_health_text = HEALTH_FONT.render(
              "HEALTH: " + str(charizard_health), 1, WHITE)
        pika1_health_text = HEALTH_FONT.render(
              "HEALTH: " + str(pika1_health), 1, WHITE)
        WIN.blit(charizard_health_text,  (10, 10))
        WIN.blit(pika1_health_text, (WIDTH - pika1_health_text.get_width() - 10, 10))

        WIN.blit(CHARIZARD_IMAGE, (charizard.x, charizard.y ))
        WIN.blit(PIKA1_IMAGE, (pika1.x, pika1.y))
        


        for bullet in charizard_bullets:
              pygame.draw.rect(WIN, YELLOW, bullet)
        
        for bullet in pika1_bullets:
              pygame.draw.rect(WIN, RED, bullet)

        pygame.display.update()

def charizard_movement(keys_pressed, charizard):
    if keys_pressed[pygame.K_a] and charizard.x - VEL > 0:  # left
        charizard.x -= VEL
    if keys_pressed[pygame.K_w] and charizard.y - VEL > 0:  # up
        charizard.y -= VEL
    if keys_pressed[pygame.K_s] and charizard.y + VEL + charizard.height < BORDER.y:  # down
        charizard.y += VEL
    if keys_pressed[pygame.K_d] and charizard.x + VEL + charizard.width < WIDTH:  # right
        charizard.x += VEL


def pika1_movement(keys_pressed, pika1):
    if keys_pressed[pygame.K_LEFT] and pika1.x - VEL > 0:  # left
        pika1.x -= VEL
    if keys_pressed[pygame.K_UP] and pika1.y - VEL > BORDER.y:  # up
        pika1.y -= VEL
    if keys_pressed[pygame.K_DOWN] and pika1.y + VEL + pika1.height < HEIGHT:  # down
        pika1.y += VEL
    if keys_pressed[pygame.K_RIGHT] and pika1.x + VEL + pika1.width < WIDTH:  # right
        pika1.x += VEL

def handle_bullets(charizard_bullets, pika1_bullets, charizard, pika1):
        for bullet in pika1_bullets:
            bullet.y -= BULLET_VEL
            if charizard.colliderect(bullet):
                  pygame.event.post(pygame.event.Event(CHARIZARD_HIT))
                  pika1_bullets.remove(bullet)
            elif bullet.y < 0:
                  pika1_bullets.remove(bullet)
      
      
      

        for bullet in charizard_bullets:
            bullet.y += BULLET_VEL
            if pika1.colliderect(bullet):
                  pygame.event.post(pygame.event.Event(PIKA1_HIT))
                  charizard_bullets.remove(bullet)
            elif bullet.y > HEIGHT:
                  charizard_bullets.remove(bullet)



def draw_winner(text):
      draw_text = WINNER_FONT.render(text, 1, WHITE)
      WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                           2, HEIGHT/2 - draw_text.get_height()/2))
      pygame.display.update()
      pygame.time.delay(5000)

def main():
    charizard = pygame.Rect(425, 0, 80, 60)
    pika1 = pygame.Rect(425, 300, IMAGE_WIDTH, IMAGE_HEIGHT)

    charizard_bullets = []
    pika1_bullets = []

    charizard_health = 10
    pika1_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(charizard_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                              charizard.x, charizard.y + charizard.height//2 - 2, 10, 5)
                        charizard_bullets.append(bullet)
                        CHAR_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(pika1_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                              pika1.x + pika1.width, pika1.y + pika1.height//2 - 2, 10, 5)
                        pika1_bullets.append(bullet)
                        PIKA_FIRE_SOUND.play()

            if event.type == CHARIZARD_HIT:
               charizard_health -= 1
               BOOM_HIT_SOUND.play()

            if event.type == PIKA1_HIT:
                pika1_health -= 1
                BOOM_HIT_SOUND.play()


        winner_text = ""
        if charizard_health <= 0:
                winner_text = "PIKACHU WINS!!! PIKA PIKA"

        if pika1_health <= 0:
                winner_text = "CHARIZARD WINS!!! RAWRRRRR" 

        if winner_text != "":
                draw_winner(winner_text)
                break

        keys_pressed = pygame.key.get_pressed()
        
        charizard_movement(keys_pressed, charizard)#charizard
        pika1_movement(keys_pressed, pika1)#pika1

        handle_bullets(charizard_bullets, pika1_bullets, charizard, pika1)

        draw_window(charizard, pika1, charizard_bullets, pika1_bullets, charizard_health, pika1_health)


    main()

if __name__ == "__main__":

    main()