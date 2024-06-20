import arcade


class CameraManager:
    def __init__(self, width, height):
        self.camera = arcade.Camera(width, height)
        self.gui_camera = arcade.Camera(width, height)

    def center_camera_to_player(self, player):
        screen_center_x = max(player.center_x - (self.camera.viewport_width / 2), 0)
        screen_center_y = max(player.center_y - (self.camera.viewport_height / 2), 0)

        world_width, world_height = self.camera.viewport_width * 5, self.camera.viewport_height * 5
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        screen_center_x = min(screen_center_x, world_width - self.camera.viewport_width)
        screen_center_y = min(screen_center_y, world_height - self.camera.viewport_height)
        player_centered = (screen_center_x, screen_center_y)

        self.camera.move_to(player_centered)

    def use_camera(self):
        self.camera.use()

    def use_gui_camera(self):
        self.gui_camera.use()
