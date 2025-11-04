# CENG 3511 - midterm project report

1. Game Description

The selected game is the classic Pong, which is not included in the provided list. The game consists of two paddles and a ball. The left paddle is controlled by the user using the W/S or arrow keys; the right paddle is controlled by a simple artificial intelligence (AI). The ball bounces off the walls and gains an angle when it hits a paddle. If the ball exits the screen from the left side, the right player (AI) scores 1 point; if it exits from the right side, the left player scores 1 point. The first player to reach 5 points wins.

2. Artificial Intelligence Design

Method: Simple rule-based tracker

Input: ball_y (vertical position of the ball center), ball_vx (horizontal velocity of the ball), paddle_center_y (vertical position of the paddle center)

Output: -1 (move up), 0 (stay), +1 (move down)

Logic: If the ball is not moving toward the AI (ball_vx <= 0), the paddle stays still. If the ball is approaching, the AI moves up or down depending on the ball’s Y position. The dead_zone parameter prevents small unnecessary movements and reduces jitter.

This approach does not include learning (no ML/RL); it is very simple, understandable, and has easily adjustable parameters.

3. Development

Language/Libraries: Python 3.9+, Pygame 2.5+

Files:

game.py: Game loop, physics, and rendering

ai_agent.py: AI decision logic (independent of Pygame)

requirements.txt: Dependencies

README.md: Installation and usage

4. Testing and Evaluation

In-game testing: The AI successfully follows the ball as it approaches, effectively blocking shots. When dead_zone is small, the AI becomes more sensitive; when larger, its movement is smoother. The score target is set to 5.

Observation: When track_only_when_approaching=True, the AI does not move unnecessarily and appears more natural visually.

5. Challenges and Solutions

Jitter/Vibration: When the ball and paddle centers were very close, rapid direction changes occurred. To prevent this, the dead_zone parameter was added.

Angle Control: The bounce angle was adjusted based on the collision point between the ball and paddle, making the gameplay smoother and more dynamic.

6. Conclusion

The Pong game was successfully implemented with a simple rule-based AI. The project demonstrates a fundamental example of decision-making logic in games. As future work, a learning-based paddle agent (e.g., Q-Learning or DQN) could be added to enable dynamic difficulty and adaptive AI behavior.
