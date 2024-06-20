import random
import arcade


class Star:
    def __init__(self, x, y, size, alpha):
        self.x = x
        self.y = y
        self.size = size
        self.alpha = alpha
        self.alpha_change_rate = random.uniform(2.0, 5.0)
        self.fading_out = random.choice([True, False])
        self.move_rate_x = random.uniform(-0.1, 0.1)
        self.move_rate_y = random.uniform(-0.1, 0.1)

    def update(self):
        if self.fading_out:
            self.alpha -= self.alpha_change_rate
            if self.alpha <= 0:
                self.alpha = 0
                self.fading_out = False
        else:
            self.alpha += self.alpha_change_rate
            if self.alpha >= 255:
                self.alpha = 255
                self.fading_out = True
        self.x += self.move_rate_x
        self.y += self.move_rate_y


class GalacticBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stars = []

    def create_starry_background(self):
        for i in range(1000):
            x = random.randint(0, self.width * 5)
            y = random.randint(0, self.height * 5)
            size = random.randint(1, 4)
            alpha = random.randint(0, 255)
            star = Star(x, y, size, alpha)
            self.stars.append(star)

    def draw(self):
        for star in self.stars:
            arcade.draw_circle_filled(star.x, star.y, star.size, (255, 255, 255, star.alpha))

    def update(self):
        for star in self.stars:
            star.update()

    def on_resize(self, width, height):
        self.width = width
        self.height = height
        self.stars.clear()
        self.create_starry_background()
