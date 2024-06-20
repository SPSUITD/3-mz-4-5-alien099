import random
import arcade


class Planet(arcade.Sprite):
    def __init__(self, width, height):
        super().__init__("images/planet.png", 0.2)
        self.center_x = random.randrange(width, width * 5)
        self.center_y = random.randrange(width, height * 5)
        self.exploration_progress = 0

    def update_exploration(self, progress):
        self.exploration_progress = min(max(progress, 0), 100)

    def draw(self):
        super().draw()
        self.draw_exploration_bar()

    def draw_exploration_bar(self):
        bar_width = 100
        bar_height = 10
        bar_x = self.center_x
        bar_y = self.center_y - self.height // 2 - 20

        arcade.draw_rectangle_outline(bar_x, bar_y, bar_width, bar_height, arcade.color.WHITE)

        filled_width = bar_width * (self.exploration_progress / 100)
        arcade.draw_rectangle_filled(bar_x - (bar_width - filled_width) / 2, bar_y, filled_width, bar_height,
                                     (71, 56, 142))
