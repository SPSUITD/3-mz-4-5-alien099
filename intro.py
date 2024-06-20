import arcade


class IntroManager:
    def __init__(self, window, width, height):
        self.background = arcade.load_texture("images/menu_background.png")
        self.window = window
        self.width = width
        self.height = height
        self.rect_width = width // 2
        self.rect_height = height // 2
        self.rect_color = (9, 23, 36, 179)
        self.rect_x = width // 4
        self.rect_y = height // 4
        self.waiting_for_click = True
        self.text = ("Далекое будущее. Галактика на грани катастрофы. "
                     "Командование назначило вас капитаном на ответственное задание - "
                     "изучить планеты, на которых вы найдете ответы, способные спасти галактику от уничтожения. "
                     "Помните, ваша миссия опасна, но ваши навыки и умения делают вас нашей последней надеждой. "
                     "Собирайте космический мусор - это не только способ улучшить ваш корабль, но и шанс спасти мир "
                     "от гибели. "
                     "Приготовьтесь, капитан! Ваша космическая одиссея начинается...")
        self.index = 0
        self.text_speed = 0.5
        self.finished = False
        self.setup()

    def setup(self):
        pass

    def update(self):
        self.index += self.text_speed
        if self.waiting_for_click:
            return
        if self.index >= len(self.text):
            self.finished = True

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)
        arcade.draw_rectangle_filled(self.width // 2, self.height // 2,
                                     self.width - 300, self.height - 300,
                                     self.rect_color)
        text_x = self.width // 2
        text_y = self.height // 2
        arcade.draw_text(self.text[:int(self.index)],
                         text_x, text_y,
                         arcade.color.WHITE, font_size=20,
                         width=self.rect_width - 20,
                         align="center", anchor_x="center", anchor_y="center")

    def on_mouse_press(self):
        if self.waiting_for_click:
            self.waiting_for_click = False
            self.window.show_game()
