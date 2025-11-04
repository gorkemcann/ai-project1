Controls
Left Paddle: W (up), S (down) or Up / Down arrow keys

P: Pause / Resume

R: Reset / Restart

ESC: Exit

Artificial Intelligence (Summary)
The SimplePaddleAI inside ai_agent.py is an extremely basic decision-maker:

Input: ball_y, ball_vx, paddle_center_y

Output: -1 (up), 0 (wait), +1 (down)

Logic: If the ball is above/below the paddle's center, move in the corresponding direction; a dead_zone is used to prevent jittering for small differences. If the ball is not coming towards the AI's side, it prefers to wait.

Structure
game.py: Pygame loop, physics, collisions, scoring, drawing, and keyboard input.

ai_agent.py: AI classes (Pygame independent).

requirements.txt: Required dependencies.

REPORT.md: Brief project report.

Notes
Screen resolution is 900x600, the first player to reach a score of 5 wins.

Difficulty can be adjusted with AI parameters (dead_zone, track_only_when_approaching).

Pygame wheels might sometimes not support the very latest Python versions simultaneously. If you encounter installation issues, try creating the virtual environment with a Python version in the range of 3.10–3.12.

To see available Python versions: py -0p

If only 3.14 is visible, install Python 3.12 and then use: py -3.12 -m venv .venv