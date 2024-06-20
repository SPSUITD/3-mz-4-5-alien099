import arcade
import math


class Ship(arcade.Sprite):
    def __init__(self, level):
        super().__init__("images/ship.png", 0.15)
        self.level = level
        self.change_x = 0
        self.change_y = 0
        self.speed = 3 + level * 2
        self.projectiles_list = arcade.SpriteList()
        self.fire_rate = 0.5
        self.fire_delay = 0.3
        self.fire_timer = 0.0

    def update(self):
        self.fire_timer += 1
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.change_x != 0 or self.change_y != 0:
            angle_rad = math.atan2(-self.change_x, self.change_y)
            self.angle = math.degrees(angle_rad)

    def on_key_press(self, key, level):
        self.speed = 3 + level * 2
        if key in [arcade.key.UP, arcade.key.W]:
            self.change_y = self.speed
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.change_y = -self.speed
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.change_x = -self.speed
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.change_x = self.speed

    def on_key_release(self, key):
        if key in [arcade.key.UP, arcade.key.W]:
            self.change_y = 0
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.change_y = 0
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.change_x = 0
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.change_x = 0

    def fire_projectile(self):
        if self.fire_timer >= self.fire_delay:
            angle_rad = math.radians(self.angle)
            nose_x = self.center_x + math.cos(angle_rad)
            nose_y = self.center_y + math.sin(angle_rad)
            projectile = ShipProjectile(nose_x, nose_y, self.angle, self.level)
            self.projectiles_list.append(projectile)
            self.fire_timer = 0.0


class ShipProjectile(arcade.Sprite):
    def __init__(self, x, y, angle, level):
        super().__init__("images/ship_projectile.png", scale=0.02)
        self.center_x = x
        self.center_y = y
        self.angle = angle
        self.level = level
        self.speed = 8 + level * 2
        angle_rad = math.radians(angle+90)
        self.change_x = math.cos(angle_rad) * self.speed
        self.change_y = math.sin(angle_rad) * self.speed

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
