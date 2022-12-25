import arcade


class AnimatedSprite(arcade.Sprite):
    def __init__(self, filename, image_width, image_height, frames, rate=1):
        super().__init__(image_width=image_width, image_height=image_height)
        self.frames = frames
        # Animation timing
        self.time = 1
        self.update_time = 0
        self.interval = 1/(60*rate)

        # Load Textures
        texture_coords = []
        for i in range(frames):
            texture_coords.append( (i*image_width, 0, image_width, image_height) )

        self.textures = arcade.load_textures(filename, texture_coords)
        self.texture = self.textures[0]

    def update_animation(self, delta_time: float = 1/60):
        self.time += delta_time

        if self.time < self.update_time:
            return

        self.update_time = self.time + self.interval

        self.cur_texture_index += 1

        if self.cur_texture_index > self.frames-1:
            self.cur_texture_index = 0

        self.texture = self.textures[self.cur_texture_index]
