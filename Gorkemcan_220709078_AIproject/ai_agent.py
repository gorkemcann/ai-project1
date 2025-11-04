from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimplePaddleAI:
    dead_zone: float = 10.0 
    track_only_when_approaching: bool = True 

    def decide(self, ball_y: float, ball_vx: float, paddle_center_y: float) -> int:


        for v in (ball_y, ball_vx, paddle_center_y):
            if not isinstance(v, (int, float)):
                raise ValueError("Numerik olmayan giriş")

        if self.track_only_when_approaching and ball_vx <= 0:
            return 0

        dy = ball_y - paddle_center_y
        if abs(dy) <= self.dead_zone:
            return 0
        return 1 if dy > 0 else -1


@dataclass
class AlwaysCenterAI:
    screen_center_y: float
    dead_zone: float = 10.0

    def decide(self, ball_y: float, ball_vx: float, paddle_center_y: float) -> int:
        dy = self.screen_center_y - paddle_center_y
        if abs(dy) <= self.dead_zone:
            return 0
        return 1 if dy > 0 else -1