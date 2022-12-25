import arcade


SPRITE_WIDTH = 64
SPRITE_HEIGHT = 32

FRAMES = 15

class AnimatedSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Animation timing
        self.time = 1
        self.update_time = 0
        self.rate = 1/60
        self.cur_texture = 0

        # --- Load Textures ---
        texture_coords = []
        for i in range(FRAMES):
            texture_coords.append( (i*SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT) )

        #self.walk_textures = arcade.load_textures(asset('sprites/butterflies.png'), texture_coords)
        self.walk_textures = arcade.load_textures(args[0], texture_coords)
        self.texture = self.walk_textures[0]

    def update_animation(self, delta_time: float = 1/60):
        self.time += delta_time

        if self.update_time > self.time:
            return
        self.update_time = self.time + self.rate

        self.cur_texture += 1

        if self.cur_texture > FRAMES-1:
            self.cur_texture = 0

        self.texture = self.walk_textures[self.cur_texture]
