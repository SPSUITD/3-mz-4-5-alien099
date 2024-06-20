import random
import arcade
import math

ALIEN_MOVEMENT_SPEED = 2
ALIEN_FIRE_RATE = 2


class Alien(arcade.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__("images/alien.png", scale=0.12)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_x = random.randint(0, screen_width * 3)
        self.center_y = random.randint(0, screen_height * 3)
        self.change_x = random.choice([-1, 1]) * ALIEN_MOVEMENT_SPEED
        self.change_y = random.choice([-1, 1]) * ALIEN_MOVEMENT_SPEED
        self.time_since_last_fire = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0 or self.right > self.screen_width * 3:
            self.change_x *= -1
        if self.bottom < 0 or self.top > self.screen_height * 3:
            self.change_y *= -1

    def can_fire(self, delta_time):
        self.time_since_last_fire += delta_time
        if self.time_since_last_fire >= 1 / ALIEN_FIRE_RATE:
            self.time_since_last_fire = 0
            return True
        return False

    def fire_projectile(self, target_x, target_y):
        projectile = AlienProjectile(self.center_x, self.center_y, target_x, target_y)
        return projectile


def generate_aliens(count, screen_width, screen_height):
    aliens_list = arcade.SpriteList()
    for x in range(count):
        alien = Alien(screen_width, screen_height)
        aliens_list.append(alien)
    return aliens_list


def update_aliens(aliens_list, ship, projectiles_list, delta_time):
    for alien in aliens_list:
        alien.update()
        if alien.can_fire(delta_time):
            projectile = alien.fire_projectile(ship.center_x, ship.center_y)
            projectiles_list.append(projectile)


class AlienProjectile(arcade.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__("images/alien_projectile.png", scale=0.02)
        self.center_x = x
        self.center_y = y
        self.change_x = 5
        self.change_y = -5

        angle_rad = math.atan2(y - target_y, x - target_x)
        angle_rad += math.atan2(target_y - y, target_x - x)

        self.angle = math.degrees(angle_rad)
        self.change_x = math.cos(angle_rad) * 5
        self.change_y = math.sin(angle_rad) * 5

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y



