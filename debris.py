import random
import arcade


class DebrisManager:
    def __init__(self, width, height):
        self.debris_list = arcade.SpriteList()
        self.collided_debris = {}
        self.width = width
        self.height = height
        self.debris_images = ["images/trash1.png", "images/trash2.png", "images/trash3.png"]

    def create_debris(self, count=100):
        for x in range(count):
            debris_image = random.choice(self.debris_images)
            debris = arcade.Sprite(debris_image, scale=0.13)
            debris.center_x = random.randrange(0, self.width * 5)
            debris.center_y = random.randrange(0, self.height * 5)
            debris.change_x = random.uniform(-1, 1)
            debris.change_y = random.uniform(-1, 1)
            debris.change_angle = random.uniform(-1, 1)
            self.debris_list.append(debris)
            self.collided_debris[debris] = False

    def update(self):
        for debris in self.debris_list:
            debris.center_x += debris.change_x
            debris.center_y += debris.change_y
            debris.angle += debris.change_angle
            if debris.left < 0 or debris.right > self.width * 3:
                debris.change_x *= -1
            if debris.bottom < 0 or debris.top > self.height * 3:
                debris.change_y *= -1

    def check_collisions(self, ship):
        score_increment = 0
        trash_increment = 0
        for debris in self.debris_list:
            if arcade.check_for_collision(ship, debris) and not self.collided_debris[debris]:
                score_increment += 1
                trash_increment += 1
                self.collided_debris[debris] = True
                debris.remove_from_sprite_lists()
        return score_increment, trash_increment

    def draw(self):
        self.debris_list.draw()
