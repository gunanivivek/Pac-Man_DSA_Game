🟡 Pac-Man Game 


🎮A fun, grid-based implementation of the classic Pac-Man game using Python and Pygame. 
This project features dynamic gameplay with procedurally generated mazes, ghosts with different behaviors, and power-ups for an engaging experience.

📜 Features
Dynamic Gameplay: Randomly generated maze with collectible dots and power-ups.


Ghosts with AI Behavior: Ghosts alternate between chasing and fleeing Pac-Man based on power-up status.

Power-ups: Collect power-ups to scare the ghosts and earn extra points.

Score Tracking: Keep track of your score and lives.

Game Over and Restart: A seamless game loop with a reset feature.



![image](https://github.com/user-attachments/assets/3c82b757-cbdf-4932-b643-0f7d609bf569)




🚀 How to Play
Start the Game: Use the arrow keys to navigate Pac-Man through the maze.

Objective: Collect all the dots while avoiding the ghosts.

Power-ups: Eat purple power-ups to scare the ghosts and earn bonus points by catching them.

Game Over: Lose a life when a ghost catches you (unless they're scared).

Restart: Press R to reset the game after a game over.


🛠️ Installation and Setup
    Prerequisites    
    Python 3.7+
    Pygame library
    Installation Steps
    Clone the repository:
    Copy code
    
        git clone https://github.com/yourusername/pacman-game.git
        cd pacman-game
        

        pip install pygame
        
        python pacman.py

    
🎮 Controls

    Key	Action
    
    Arrow Keys	Move Pac-Man
    
    R	Restart the game after losing

    
🧠 Game Mechanics

Maze Generation

The maze is procedurally generated with walls, collectible dots, and power-ups.

Ghost Behavior

Normal State: Ghosts chase Pac-Man.

Scared State: Ghosts flee after Pac-Man eats a power-up.

Scoring

Dots: +10 points each.

Power-ups: +50 points each.

Ghosts (Scared State): +200 points for each ghost caught.

    
🎨 Game Design
    The game follows a pixel-art inspired design for a retro feel. 
    Characters and collectibles are dynamically animated for better visual feedback.

🤝 Contribution
    Contributions, issues, and feature requests are welcome! Feel free to check the issues page.    

Happy Gaming! 🎉
