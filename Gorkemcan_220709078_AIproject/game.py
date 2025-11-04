import random
import sys
from dataclasses import dataclass

import pygame

from ai_agent import SimplePaddleAI

# ---------------------
# Oyun sabitleri
# ---------------------
WIDTH, HEIGHT = 900, 600
PADDLE_W, PADDLE_H = 12, 100
BALL_SIZE = 14
MARGIN = 20
PADDLE_SPEED = 420.0  # px/s
BALL_SPEED = 360.0    # px/s (başlangıç)
WIN_SCORE = 5
FPS = 60

BG_COLOR = (18, 18, 18)
FG_COLOR = (235, 235, 235)
ACCENT = (0, 200, 255)


@dataclass
class Paddle:
    rect: pygame.Rect

    def move(self, dy: float):
        self.rect.y += int(dy)
        # Ekran dışına çıkmayı engelle
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    @property
    def center_y(self) -> float:
        return self.rect.centery


@dataclass
class Ball:
    rect: pygame.Rect
    vx: float
    vy: float

    def reset(self, direction: int):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        angle = random.uniform(-0.35, 0.35)
        speed = BALL_SPEED
        self.vx = speed * direction
        self.vy = speed * angle


class PongGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 28)
        self.big_font = pygame.font.SysFont("consolas", 48, bold=True)

        # Obje kurulum
        left_rect = pygame.Rect(MARGIN, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
        right_rect = pygame.Rect(WIDTH - MARGIN - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
        ball_rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

        self.left = Paddle(left_rect)
        self.right = Paddle(right_rect)
        self.ball = Ball(ball_rect, vx=BALL_SPEED * random.choice([-1, 1]), vy=BALL_SPEED * random.uniform(-0.35, 0.35))

        # Skor ve durumlar
        self.score_left = 0
        self.score_right = 0
        self.paused = False
        self.game_over = False

        # AI: Sağ paddle kontrol edilir
        self.ai = SimplePaddleAI(dead_zone=8.0, track_only_when_approaching=True)

    def draw_center_line(self):
        for y in range(0, HEIGHT, 24):
            pygame.draw.rect(self.screen, (60, 60, 60), (WIDTH // 2 - 2, y, 4, 12))

    def draw_scores(self):
        txt = self.big_font.render(f"{self.score_left} : {self.score_right}", True, FG_COLOR)
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 20))

    def handle_input_left(self, dt):
        keys = pygame.key.get_pressed()
        dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= PADDLE_SPEED * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += PADDLE_SPEED * dt
        self.left.move(dy)

    def handle_ai_right(self, dt):
        action = self.ai.decide(self.ball.rect.centery, self.ball.vx, self.right.center_y)
        dy = action * PADDLE_SPEED * dt
        self.right.move(dy)

    def physics(self, dt):
        # Top hareketi
        self.ball.rect.x += int(self.ball.vx * dt)
        self.ball.rect.y += int(self.ball.vy * dt)

        # Üst/alt çarpması
        if self.ball.rect.top <= 0:
            self.ball.rect.top = 0
            self.ball.vy = abs(self.ball.vy)
        elif self.ball.rect.bottom >= HEIGHT:
            self.ball.rect.bottom = HEIGHT
            self.ball.vy = -abs(self.ball.vy)

        # Sol paddle çarpışması
        if self.ball.rect.colliderect(self.left.rect) and self.ball.vx < 0:
            self.ball.rect.left = self.left.rect.right
            self.ball.vx = abs(self.ball.vx) * 1.03  # hafif hızlandır
            # Vuruş noktasına göre açı ver
            offset = (self.ball.rect.centery - self.left.center_y) / (PADDLE_H / 2)
            self.ball.vy = max(-1, min(1, offset)) * max(180, abs(self.ball.vy))

        # Sağ paddle çarpışması
        if self.ball.rect.colliderect(self.right.rect) and self.ball.vx > 0:
            self.ball.rect.right = self.right.rect.left
            self.ball.vx = -abs(self.ball.vx) * 1.03
            offset = (self.ball.rect.centery - self.right.center_y) / (PADDLE_H / 2)
            self.ball.vy = max(-1, min(1, offset)) * max(180, abs(self.ball.vy))

        # Skor kontrolü
        if self.ball.rect.right < 0:
            self.score_right += 1
            self.ball.reset(direction=1)
        elif self.ball.rect.left > WIDTH:
            self.score_left += 1
            self.ball.reset(direction=-1)

        if self.score_left >= WIN_SCORE or self.score_right >= WIN_SCORE:
            self.game_over = True

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_center_line()

        # Objeler
        pygame.draw.rect(self.screen, FG_COLOR, self.left.rect)
        pygame.draw.rect(self.screen, ACCENT, self.right.rect)
        pygame.draw.ellipse(self.screen, FG_COLOR, self.ball.rect)

        self.draw_scores()

        if self.paused:
            t = self.big_font.render("PAUSE (P)", True, (255, 230, 0))
            self.screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 30))

        if self.game_over:
            winner = "SOL" if self.score_left > self.score_right else "SAĞ (AI)"
            t1 = self.big_font.render(f"Oyun Bitti - Kazanan: {winner}", True, (0, 255, 120))
            t2 = self.font.render("Yeniden başlatmak için R, çıkış için ESC", True, FG_COLOR)
            self.screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 30))
            self.screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 + 30))

        pygame.display.flip()

    def reset(self):
        self.left.rect.centery = HEIGHT // 2
        self.right.rect.centery = HEIGHT // 2
        self.ball.reset(direction=random.choice([-1, 1]))
        self.score_left = 0
        self.score_right = 0
        self.paused = False
        self.game_over = False

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.reset()

            if not self.paused and not self.game_over:
                self.handle_input_left(dt)
                self.handle_ai_right(dt)
                self.physics(dt)

            self.draw()

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    PongGame().run()
