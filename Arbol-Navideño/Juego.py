import pygame
import random

pygame.init()

# Variables de configuración
WIDTH, HEIGHT = 600, 400
Puntuacion = (255, 0, 0)  
FPS = 60
BALL_FALL_SPEED = 4
BALL_FREQUENCY = 90

fondo = pygame.image.load("assets/Background.jpg")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))  
Iarbol = pygame.image.load("assets/arbol.png")
Iarbol = pygame.transform.scale(Iarbol, (60, 80)) 
Ibola = pygame.image.load("assets/bola.png")
Ibola = pygame.transform.scale(Ibola, (30, 30)) 
GG = pygame.image.load("assets/ganador.jpg")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.music.load("assets/musica.mp3")
pygame.mixer.music.play(-1)

class Ball:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = 0
    def fall(self):
        self.y += BALL_FALL_SPEED
    def draw(self, screen):
        screen.blit(Ibola, (self.x, self.y))

def get_jugador():
    input_box = pygame.Rect(200, 150, 140, 32)
    color_inactive = pygame.Color('red')
    color_active = pygame.Color('red')
    color = color_inactive
    text = ''
    active = False
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = pygame.font.Font(None, 32).render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(fondo, (0, 0))
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def main():
    jugador = get_jugador()
    if jugador is None:
        return

    clock = pygame.time.Clock()
    score = 0
    bolas = []
    arbol_x = WIDTH // 2
    arbol_y = HEIGHT - 80
    running = True

    while running:
        screen.blit(fondo, (0, 0)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and arbol_x > 0:
            arbol_x -= 5
        if keys[pygame.K_LEFT] and arbol_x > 0:
            arbol_x -= 5

        if keys[pygame.K_d] and arbol_x < WIDTH - 60:
            arbol_x += 5
        if keys[pygame.K_RIGHT] and arbol_x < WIDTH - 60:
            arbol_x += 5
        
        if random.randint(1, BALL_FREQUENCY) == 1:
            bolas.append(Ball())

        for bola in bolas[:]:
            bola.fall()
            if bola.y > HEIGHT:
                bolas.remove(bola)
            if bola.y + 15 >= arbol_y and arbol_x < bola.x < arbol_x + 60:
                score += 1
                bolas.remove(bola)
            bola.draw(screen)

        screen.blit(Iarbol, (arbol_x, arbol_y))
        font = pygame.font.Font("assets/Fuente.ttf", 45)
        score_text = font.render(f"Puntuacion de {jugador}: {score}", True, Puntuacion)
        screen.blit(score_text, (10, 10))

        if score > 4:
            screen.blit(GG, (50, -50))
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
