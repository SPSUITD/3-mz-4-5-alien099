import arcade


class MainMenu:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.gui_camera = arcade.Camera(width, height)
        self.button_list = []

        self.background = arcade.load_texture("images/menu_background.png")
        self.game_name = arcade.Sprite("images/game_name.png")
        self.start_button = arcade.Sprite("images/start_button.png", scale=0.3)
        self.continue_button = arcade.Sprite("images/continue_button.png", scale=0.3)
        self.controls_button = arcade.Sprite("images/controls_button.png", scale=0.3)
        self.exit_button = arcade.Sprite("images/exit_button.png", scale=0.3)

        self.game_name.center_x = self.width // 2
        self.game_name.center_y = self.height // 2 + 250
        self.start_button.center_x = self.width // 2
        self.start_button.center_y = self.height // 2 + 100
        self.continue_button.center_x = self.width // 2
        self.continue_button.center_y = self.height // 2
        self.controls_button.center_x = self.width // 2
        self.controls_button.center_y = self.height // 2 - 100
        self.exit_button.center_x = self.width // 2
        self.exit_button.center_y = self.height // 2 - 200

        self.button_list = [
            self.start_button,
            self.continue_button,
            self.controls_button,
            self.exit_button
        ]

    def draw(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)
        self.game_name.draw()
        for button in self.button_list:
            button.draw()

    def on_mouse_press(self, x, y):
        if self.start_button.collides_with_point((x, y)):
            self.window.show_intro_screen()
        elif self.continue_button.collides_with_point((x, y)):
            self.window.continue_game()
        elif self.controls_button.collides_with_point((x, y)):
            self.window.show_controls_screen()
        elif self.exit_button.collides_with_point((x, y)):
            arcade.close_window()
