import arcade


class ControlsScreen:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.gui_camera = arcade.Camera(width, height)
        self.background = arcade.load_texture("images/menu_background.png")
        self.back_button = arcade.Sprite("images/back_button.png", 0.3)
        self.setup()

    def setup(self):
        self.back_button.center_x = self.width // 2
        self.back_button.center_y = self.height // 2 - 200

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2,
                                      self.width, self.height, self.background)
        arcade.draw_text("Управление", self.width // 2, self.height // 2 + 250,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Управление кораблем: W, A, S, D и стрелки", self.width // 4,
                         self.height // 2 + 50, arcade.color.WHITE, font_size=20, anchor_x="left")
        arcade.draw_text("Стрельба: SPACE и ЛКМ", self.width // 4,
                         self.height // 2, arcade.color.WHITE, font_size=20, anchor_x="left")
        arcade.draw_text("Смена режима экрана: F", self.width // 4,
                         self.height // 2 - 50, arcade.color.WHITE, font_size=20, anchor_x="left")
        self.back_button.draw()

    def on_mouse_press(self, x, y):
        if self.back_button.collides_with_point((x, y)):
            self.window.show_menu()
