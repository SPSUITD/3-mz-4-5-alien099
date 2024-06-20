import arcade


class EndGameManager:
    def __init__(self, width, height):
        self.win = None
        self.width = width
        self.height = height
        self.background = arcade.load_texture("images/menu_background.png")
        self.gui_camera = arcade.Camera(width, height)

    def draw_end_game(self, trash, kills, level):
        self.gui_camera.use()
        arcade.start_render()
        if self.win:
            arcade.draw_text(
                "Уровень пройден",
                self.width // 2,
                self.height // 2 + 50,
                arcade.csscolor.WHITE,
                36,
                anchor_x="center",
                anchor_y="center"
            )
        else:
            arcade.draw_text(
                "Игра закончена",
                self.width // 2,
                self.height // 2 + 50,
                arcade.csscolor.WHITE,
                36,
                anchor_x="center",
                anchor_y="center"
            )
        level_text = f"Уровень корабля: {level}"
        score_text = f"Собрано космического мусора: {trash}"
        kills_text = f"Уничтожено инопланетян: {kills}"
        arcade.draw_text(
            level_text,
            self.width // 2,
            self.height // 2 - 25,
            arcade.csscolor.WHITE,
            18,
            anchor_x="center"
        )
        arcade.draw_text(
            score_text,
            self.width // 2,
            self.height // 2 - 50,
            arcade.csscolor.WHITE,
            18,
            anchor_x="center"
        )
        arcade.draw_text(
            kills_text,
            self.width // 2,
            self.height // 2 - 75,
            arcade.csscolor.WHITE,
            18,
            anchor_x="center"
        )
        arcade.draw_text(
            "Для выхода в главное меню нажмите Esc",
            self.width // 2,
            self.height // 2 - 100,
            arcade.csscolor.WHITE,
            14,
            anchor_x="center",
            anchor_y="center"
        )
