import pygame
import sys
from settings import Settings
from level import Level
from grid import Grid

class TowerDefenseGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load(self.settings.background_image).convert()
        self.background = pygame.transform.scale(self.background,
                                                 (self.settings.screen_width, self.settings.screen_height))

        self.level = Level(self)
        self.grid = Grid(self)

        self.font = pygame.font.SysFont("Arial", 24)

        self.shoot_sound = pygame.mixer.Sound(self.settings.shoot_sound)
        self.selected_tower_type = 'basic'
        self.is_game_over = False

    def game_over(self):
        self.is_game_over = True

    def is_position_inside(self, pos):
        """Check if a given position is inside the game screen boundaries."""
        return 0 <= pos.x <= self.settings.screen_width and 0 <= pos.y <= self.settings.screen_height

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_tower_type = 'basic'
                    print("Selected basic tower.")
                elif event.key == pygame.K_2:
                    self.selected_tower_type = 'sniper'
                    print("Selected sniper tower.")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.selected_tower_type:
                    mouse_pos = pygame.mouse.get_pos()
                    self.level.attempt_place_tower(mouse_pos, self.selected_tower_type)
                else:
                    print("No tower type selected.")

    def _update_game(self):
        self.level.update()
        self.grid.update()

    def _draw_win_screen(self):
        win_text = "You Win!"
        win_render = self.font.render(win_text, True, (255, 215, 0))
        win_rect = win_render.get_rect(center=(self.settings.screen_width/2, self.settings.screen_height/2))
        self.screen.blit(win_render, win_rect)

    def _draw_game_over_screen(self):
        self.screen.fill((0, 0, 0))

        game_over_text = "Game Over!"
        game_over_render = self.font.render(game_over_text, True, (255, 0, 0))
        game_over_rect = game_over_render.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2))

        self.screen.blit(game_over_render, game_over_rect)

    def _draw(self):
        if self.is_game_over:
            self._draw_game_over_screen()
        else:
            self.screen.blit(self.background, (0, 0))
            self.level.draw(self.screen)
            self.grid.draw()

            money_text = self.font.render(f"Money: ${self.settings.starting_money}", True, (255, 255, 255))
            tower_text = self.font.render(
                f"Selected Tower: {self.selected_tower_type if self.selected_tower_type else 'None'}", True,
                (255, 255, 255))
            waves_text = self.font.render(f"Waves Left: {len(self.level.waves) - self.level.current_wave}", True,
                                          (255, 255, 255))
            enemies_text = self.font.render(f"Enemies Left: {len(self.level.enemies)}", True, (255, 255, 255))

            self.screen.blit(money_text, (10, 10))
            self.screen.blit(tower_text, (10, 40))
            self.screen.blit(waves_text, (10, 70))
            self.screen.blit(enemies_text, (10, 100))

            if self.level.all_waves_complete:
                self._draw_win_screen()

        pygame.display.flip()

    def run_game(self):
        while True:
            self._check_events()
            self._update_game()

            if len(self.level.enemies) == 0 and not self.level.all_waves_complete:
                self.level.start_next_wave()

            self._draw()
            self.clock.tick(60)


if __name__ == '__main__':
    td_game = TowerDefenseGame()
    td_game.run_game()
