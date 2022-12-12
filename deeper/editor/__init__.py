import math
import arcade
import glm
import imgui

from deeper.dimgui import Gui

from deeper import Space, Block
from deeper.constants import *
from deeper.camera import WorldCamera

from .catalog import Catalog

class Hover:
    def __init__(self, space, position):
        self.space = space
        self.position = position


class Deeper(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Deeper", resizable=True)
        self.gui = Gui(self)
        self.camera = WorldCamera(self, glm.vec3(), 1)
        #self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*4, 0, CELL_DEPTH*4), 1.25)
        # self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*8, 0, CELL_DEPTH*8), 1.25)
        self.tiles = arcade.SpriteList()

        self.space = Space()
        self.hover = None

        self.catalog = Catalog(self)
        self.selection = None
        self.current = 0

        self.create_blocks()
        self.create_sprites()

    def create_blocks(self):
        rotation = glm.vec3()
        for ty in range(0, 8):
            y_distance = CELL_DEPTH * ty
            for tx in range(0, 8):
                x_distance = CELL_WIDTH * tx
                position = glm.vec3(x_distance, 0, y_distance)
                print("position: ", position)
                self.space.add_child(
                    Block(position, rotation, glm.vec3(CELL_WIDTH, 16, CELL_DEPTH))
                )

    def create_sprites(self):
        sorted_spaces = sorted(self.space.children, key=lambda space: space.position.z)
        for space in sorted_spaces:
            sprite = arcade.Sprite(
                ":deeper:tiles/FloorD3.png", scale=1 / self.camera.zoom
            )
            position = self.camera.project(space.position).xy
            #print("position: ", pos)
            sprite.set_position(*position)
            self.tiles.append(sprite)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.tiles.draw()

        for space in self.space.children:
            self.draw_aabb(space)

        pos = self.camera.project(self.camera.target).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)

        if self.hover:
            pos = self.camera.project(self.hover.position).xy
            arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)

        imgui.new_frame()
        self.draw_catalog()
        self.gui.draw()

        arcade.finish_render()

    def draw_catalog(self):
        imgui.begin('Catalog')
        clicked, self.current = imgui.combo(
            "Category", self.current, self.catalog.category_names
        )
        for item in self.catalog.categories[self.current].items:
            #_, item.selected = imgui.selectable(item.text, item.selected)
            _, selected = imgui.selectable(item.name, item.selected)
            if selected:
                if self.selection:
                    self.selection.selected = False
                self.selection = item
                item.selected = selected
            item.draw()
        imgui.end()

    def draw_aabb(self, space):
        aabb = space.aabb
        bbl = self.camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.minz))
        bbr = self.camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.minz))
        fbl = self.camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.maxz))
        fbr = self.camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.maxz))

        arcade.draw_line(bbl.x, bbl.y, bbr.x, bbr.y, arcade.color.YELLOW)
        #arcade.draw_line(fbl.x, fbl.y, fbr.x, fbr.y, arcade.color.YELLOW)
        arcade.draw_line(bbl.x, bbl.y, fbl.x, fbl.y, arcade.color.YELLOW)

    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        print("mouse: ", mouse_x, mouse_y)
        ray = self.camera.mouse_to_ray(mouse_x, mouse_y)
        result = self.space.cast_ray(ray)
        #print(contact)
        if result:
            space, contact = result
            self.hover = Hover(space, glm.vec3(contact))
        else:
            self.hover = None


def main():
    window = Deeper()
    arcade.run()


if __name__ == "__main__":
    main()
