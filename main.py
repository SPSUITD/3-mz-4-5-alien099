import os
import arcade

from background import GalacticBackground
from ship import Ship
from alien import generate_aliens, update_aliens
from debris import DebrisManager
from camera import CameraManager
from end_game import EndGameManager
from planets import Planet
from main_menu import MainMenu
from controls import ControlsScreen
from intro import IntroManager

SCREEN_TITLE = "Космическая одиссея"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class GalacticCleanup(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
        self.menu = MainMenu(self, self.width, self.height)
        self.current_screen = "menu"
        self.controls_screen = ControlsScreen(self, self.width, self.height)
        self.intro_screen = IntroManager(self, self.width, self.height)
        self.ship = None
        self.planet = None
        self.background = None
        self.aliens_list = None
        self.ship_invulnerable = False
        self.ship_flash_timer = 0.0
        self.ship_flash_interval = 0.2
        self.ship_flash_count = 0
        self.max_ship_flash_count = 6
        self.lives = 3
        self.lives_left = self.lives
        self.aliens_count = 3
        self.aliens_left = self.aliens_count
        self.ship_disappeared = False
        self.game_over = False
        self.planet_studied = False
        self.study_timer = 0
        self.study_time = 10
        self.projectiles_list = arcade.SpriteList()
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        self.score = 0
        self.trash = 0
        self.kills = 0
        self.level = 1
        self.mouse_x = 0
        self.mouse_y = 0
        self.game_started = False
        self.debris_manager = DebrisManager(width, height)
        self.camera_manager = CameraManager(self.width, self.height)
        self.end_game_manager = EndGameManager(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        self.life_image = arcade.load_texture("images/life.png")
        self.level_image = arcade.load_texture("images/ship.png")
        arcade.set_background_color(arcade.color.BLACK)

    def show_game(self):
        self.score = 0
        self.trash = 0
        self.kills = 0
        self.level = 1
        self.lives = 3
        self.game_over = False
        self.planet_studied = False
        self.study_timer = 0
        self.debris_manager.debris_list.clear()
        self.aliens_list = generate_aliens(self.aliens_count, self.width, self.height)
        self.debris_manager.create_debris()
        self.current_screen = "game"
        self.setup()
        self.set_mouse_visible(False)

    def continue_game(self):
        self.game_over = False
        self.lives = self.lives_left
        self.aliens_list = generate_aliens(self.aliens_left, self.width, self.height)
        self.debris_manager.debris_list = arcade.SpriteList()
        self.debris_manager.create_debris()
        self.current_screen = "game"
        self.setup()
        self.set_mouse_visible(False)

    def show_controls_screen(self):
        self.current_screen = "controls"
        self.controls_screen.setup()
        self.set_mouse_visible(True)

    def show_intro_screen(self):
        self.current_screen = "intro"
        self.intro_screen.setup()
        self.set_mouse_visible(True)

    def show_menu(self):
        self.current_screen = "menu"
        self.set_mouse_visible(True)

    def reduce_life(self):
        self.lives -= 1
        self.lives_left -= 1
        if self.lives <= 0:
            self.game_over = True
            self.end_game_manager.draw_end_game(self.trash, self.kills, self.level)
        else:
            self.ship_invulnerable = True
            self.ship_flash_timer = 0.0
            self.ship_flash_count = 3
            self.ship_disappeared = False
            self.ship.visible = True

    def setup(self):
        width, height = self.get_size()
        self.background = GalacticBackground(width, height)
        self.background.create_starry_background()
        self.ship = Ship(self.level)
        self.planet = Planet(width, height)
        self.aliens_list = generate_aliens(self.aliens_count, width, height)
        self.debris_manager.create_debris()
        self.ship.center_x = width // 2
        self.ship.center_y = height // 2
        self.planet.exploration_progress = 0

    def on_draw(self):
        arcade.start_render()
        if self.current_screen == "menu":
            self.menu.draw()
        elif self.current_screen == "intro":
            self.intro_screen.on_draw()
        elif self.current_screen == "controls":
            self.controls_screen.on_draw()
        else:
            self.camera_manager.use_camera()
            self.background.draw()
            if not self.game_over:
                self.debris_manager.draw()
                self.ship.draw()
                self.planet.draw()
                self.aliens_list.draw()
                self.projectiles_list.draw()
                self.ship.projectiles_list.draw()
                self.camera_manager.use_gui_camera()

                for i in range(self.lives):
                    arcade.draw_texture_rectangle(30 + i * 40, self.height - 30, 30, 30, self.life_image)

                    arcade.draw_texture_rectangle(30, self.height - 70, 30, 30, self.level_image)
                    arcade.draw_text(f"x {self.level}", 50, self.height - 80, arcade.csscolor.WHITE, 18)
            else:
                self.end_game_manager.draw_end_game(self.trash, self.kills, self.level)

    def on_update(self, delta_time):
        if self.current_screen == "intro":
            self.intro_screen.update()
            if self.intro_screen.finished:
                self.show_game()
        elif self.current_screen == "menu" or self.current_screen == "controls" or self.current_screen == "intro":
            return
        elif self.game_started and not self.game_over:
            self.camera_manager.center_camera_to_player(self.ship)
            self.background.update()
            self.debris_manager.update()
            self.ship.update()
            score_increment, trash_increment = self.debris_manager.check_collisions(self.ship)
            self.score += score_increment
            self.trash += trash_increment
            self.update_level()
            update_aliens(self.aliens_list, self.ship, self.projectiles_list, delta_time)
            self.projectiles_list.update()
            self.ship.projectiles_list.update()

            if self.ship_invulnerable:
                self.ship_flash_timer += delta_time
                if self.ship_flash_timer >= self.ship_flash_interval:
                    self.ship_flash_timer = 0.0
                    self.ship.visible = not self.ship.visible
                    self.ship_flash_count += 1
                    if self.ship_flash_count >= self.max_ship_flash_count:
                        self.ship_invulnerable = False
                        self.ship.visible = True

            for projectile in self.projectiles_list:
                if arcade.check_for_collision(self.ship, projectile) and not self.ship_invulnerable:
                    self.reduce_life()
                    projectile.remove_from_sprite_lists()

            for projectile in self.ship.projectiles_list:
                for alien in self.aliens_list:
                    if arcade.check_for_collision(projectile, alien):
                        self.aliens_list.remove(alien)
                        alien.remove_from_sprite_lists()
                        projectile.remove_from_sprite_lists()
                        self.score += 10
                        self.kills += 1
                        self.aliens_left -= 1

            if arcade.check_for_collision(self.ship, self.planet):
                self.study_timer += delta_time
                if self.study_timer >= self.study_time:
                    self.planet_studied = True
                    self.game_over = True
                    self.end_game_manager.win = True
                self.planet.update_exploration((self.study_timer / self.study_time) * 100)

    def update_level(self):
        if self.level == 1 and self.score >= 5:
            self.level = 2
        elif self.level == 2 and self.score >= 20:
            self.level = 3
        elif self.level == 3 and self.score >= 50:
            self.level = 4
        elif self.level == 4 and self.score >= 90:
            self.level = 5

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)
            self.camera_manager.camera = arcade.Camera(width, height)
            self.camera_manager.gui_camera = arcade.Camera(width, height)
        if self.current_screen == "menu":
            return
        if self.game_over:
            if key == arcade.key.ESCAPE:
                self.show_menu()
        else:
            self.ship.on_key_press(key, self.level)
            self.game_started = True
            if key == arcade.key.SPACE:
                if self.ship and not self.game_over:
                    self.ship.fire_projectile()
            elif key == arcade.key.ESCAPE:
                self.show_menu()

    def on_key_release(self, key, modifiers):
        if self.current_screen != "menu":
            self.ship.on_key_release(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_screen == "menu":
            self.menu.on_mouse_press(x, y)
        elif self.current_screen == "controls":
            self.controls_screen.on_mouse_press(x, y)
        elif self.current_screen == "intro":
            self.intro_screen.on_mouse_press()
        elif self.current_screen == "game":
            if button == arcade.MOUSE_BUTTON_LEFT:
                if self.ship and not self.game_over:
                    self.ship.fire_projectile()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.set_viewport(0, width, 0, height)
        self.camera_manager.camera = arcade.Camera(self.width, self.height)
        self.camera_manager.gui_camera = arcade.Camera(self.width, self.height)
        self.end_game_manager = EndGameManager(width, height)
        self.menu = MainMenu(self, width, height)
        self.controls_screen = ControlsScreen(self, width, height)
        self.intro_screen = IntroManager(self, width, height)


def main():
    game = GalacticCleanup()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
