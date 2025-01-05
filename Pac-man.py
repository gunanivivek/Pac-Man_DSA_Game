import pygame
import math
from queue import PriorityQueue
import random

pygame.init()
WINDOW_SIZE, CELL_SIZE = 800, 40
GRID_SIZE = WINDOW_SIZE // CELL_SIZE
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Colors and game constants
COLORS = {
    'black': (0, 0, 0), 'white': (255, 255, 255), 'yellow': (255, 255, 0),
    'blue': (0, 0, 255), 'red': (255, 0, 0), 'pink': (255, 192, 203),
    'cyan': (0, 255, 255), 'purple': (128, 0, 128)
}
GHOST_COLORS = [COLORS['red'], COLORS['pink'], COLORS['cyan']]
POWER_DURATION = 300

# Speed settings
PACMAN_SPEED = 0.8  # Base speed for Pac-Man
GHOST_SPEED_NORMAL = 0.5  # Normal ghost speed (half of Pac-Man's speed)
GHOST_SPEED_SCARED = 0.4  # Scared ghost speed (even slower)
MOVE_DELAY = 10  # Frames between ghost movements

class Character:
    def __init__(self, x, y, color, is_pacman=True):
        self.x, self.y = x, y
        self.color = self.original_color = color
        self.is_pacman = is_pacman
        self.scared = False
        self.size = CELL_SIZE - 10
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.move_counter = 0
        self.speed = PACMAN_SPEED if is_pacman else GHOST_SPEED_NORMAL
        
    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))
        if self.is_pacman:
            self._draw_pacman()
        else:
            self._draw_ghost()
        screen.blit(self.surface, (self.x * CELL_SIZE + 5, self.y * CELL_SIZE + 5))
        
    def _draw_pacman(self):
        color = COLORS['yellow']
        pygame.draw.circle(self.surface, color, (self.size//2, self.size//2), self.size//2-2)
        pygame.draw.rect(self.surface, color, (self.size//4, self.size//2, self.size//2, self.size//3))
        pygame.draw.circle(self.surface, COLORS['black'], (self.size//3, self.size//3), 3)
        pygame.draw.circle(self.surface, COLORS['black'], (2*self.size//3, self.size//3), 3)
        
    def _draw_ghost(self):
        color = COLORS['blue'] if self.scared else self.color
        offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        pygame.draw.circle(self.surface, color, (self.size//2, self.size//2 + offset), self.size//2-2)
        points = [(self.size//4, self.size//2), (self.size//4, self.size), 
                 (self.size//2, self.size*7//8), (3*self.size//4, self.size)]
        pygame.draw.polygon(self.surface, color, points)
        eye_color = COLORS['red'] if self.scared else COLORS['white']
        pygame.draw.circle(self.surface, eye_color, (self.size//3, self.size//2), 3)
        pygame.draw.circle(self.surface, eye_color, (2*self.size//3, self.size//2), 3)

    def move(self, dx, dy, walls):
        self.move_counter += self.speed
        if self.move_counter >= 1:
            self.move_counter = 0
            new_x, new_y = self.x + dx, self.y + dy
            if (new_x, new_y) not in walls and 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                self.x, self.y = new_x, new_y
                return True
        return False

class Game:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.walls = self._generate_maze()
        self.dots = {(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) 
                    if (x, y) not in self.walls}
        self.powerups = self._place_powerups()
        self.pacman = Character(*self._find_empty_spot(), COLORS['yellow'])
        self.ghosts = [Character(*self._find_empty_spot(), color, False) 
                      for color in GHOST_COLORS]
        self.score = 0
        self.lives = 3
        self.power_time = 0
        self.game_over = False
        self.move_timer = 0
        
    def _generate_maze(self):
        walls = {(x, y) for x in range(GRID_SIZE) for y in [0, GRID_SIZE-1]}
        walls |= {(x, y) for x in [0, GRID_SIZE-1] for y in range(GRID_SIZE)}
        for _ in range(GRID_SIZE * 3):
            x, y = random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)
            walls.add((x, y))
        return walls
        
    def _place_powerups(self):
        dots_list = list(self.dots)
        num_powerups = min(4, len(dots_list))
        if num_powerups == 0:
            return []
        chosen_spots = random.sample(dots_list, num_powerups)
        return [(x, y, 'power') for x, y in chosen_spots]
        
    def _find_empty_spot(self):
        while True:
            x, y = random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)
            if (x, y) not in self.walls:
                return x, y

    def move_ghosts(self):
        self.move_timer += 1
        if self.move_timer < MOVE_DELAY:
            return
        
        self.move_timer = 0
        for ghost in self.ghosts:
            ghost.speed = GHOST_SPEED_SCARED if ghost.scared else GHOST_SPEED_NORMAL
            if ghost.scared:
                dx = -1 if ghost.x > self.pacman.x else 1
                dy = -1 if ghost.y > self.pacman.y else 1
            else:
                dx = 1 if ghost.x < self.pacman.x else -1
                dy = 1 if ghost.y < self.pacman.y else -1
            
            if random.random() < 0.5:
                ghost.move(dx, 0, self.walls)
            else:
                ghost.move(0, dy, self.walls)
                
    def update(self):
        if self.game_over:
            return
            
        if self.power_time > 0:
            self.power_time -= 1
            if self.power_time == 0:
                for ghost in self.ghosts:
                    ghost.scared = False
                    
        pacman_pos = (self.pacman.x, self.pacman.y)
        if pacman_pos in self.dots:
            self.dots.remove(pacman_pos)
            self.score += 10
            
        for powerup in self.powerups[:]:
            if (powerup[0], powerup[1]) == pacman_pos:
                self.power_time = POWER_DURATION
                for ghost in self.ghosts:
                    ghost.scared = True
                self.powerups.remove(powerup)
                self.score += 50
                
        for ghost in self.ghosts:
            if abs(ghost.x - self.pacman.x) < 1 and abs(ghost.y - self.pacman.y) < 1:
                if ghost.scared:
                    ghost.x, ghost.y = self._find_empty_spot()
                    self.score += 200
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self._reset_positions()
                        
    def _reset_positions(self):
        self.pacman.x, self.pacman.y = self._find_empty_spot()
        for ghost in self.ghosts:
            ghost.x, ghost.y = self._find_empty_spot()
                
    def draw(self):
        screen.fill(COLORS['black'])
        
        for x, y in self.walls:
            pygame.draw.rect(screen, COLORS['blue'], 
                           (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for x, y in self.dots:
            pygame.draw.circle(screen, COLORS['white'],
                             (x * CELL_SIZE + CELL_SIZE//2, 
                              y * CELL_SIZE + CELL_SIZE//2), 3)
                              
        for x, y, _ in self.powerups:
            pygame.draw.circle(screen, COLORS['purple'],
                             (x * CELL_SIZE + CELL_SIZE//2,
                              y * CELL_SIZE + CELL_SIZE//2), 8)
                              
        self.pacman.draw(screen)
        for ghost in self.ghosts:
            ghost.draw(screen)
            
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score} Lives: {self.lives}', True, COLORS['white'])
        screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over = font.render('Game Over! Press R to restart', True, COLORS['white'])
            screen.blit(game_over, (WINDOW_SIZE//3, WINDOW_SIZE//2))
            
        pygame.display.flip()

def main():
    game = Game()
    running = True
    
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game = Game()
                
        if not game.game_over:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT]: dx = -1
            elif keys[pygame.K_RIGHT]: dx = 1
            elif keys[pygame.K_UP]: dy = -1
            elif keys[pygame.K_DOWN]: dy = 1
            
            game.pacman.move(dx, dy, game.walls)
            game.move_ghosts()
            game.update()
            
        game.draw()
        
    pygame.quit()

if __name__ == "__main__":
    main()