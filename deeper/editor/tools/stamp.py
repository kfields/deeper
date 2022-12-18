import glm

import arcade
from arcade import key

from .tool import WorldEditTool

class Hovered:
    def __init__(self, entity, space, position):
        self.entity = entity
        self.space = space
        self.position = position

class Selected:
    def __init__(self, entity, space):
        self.entity = entity
        self.space = space

class StampTool(WorldEditTool):
    def __init__(self, view, edit_state) -> None:
        super().__init__(view, edit_state)
        self.hovered = None
        self.selected = None

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        print("mouse: ", x, y)
        ray = self.camera.mouse_to_ray(x, y)
        result = self.world.cast_ray(ray)
        print(result)
        if result:
            entity, space, contact = result
            print("contact: ", contact)
            self.hovered = Hovered(entity, space, glm.vec3(contact))
        else:
            self.hovered = None

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.hovered:
            self.selected = Selected(self.hovered.entity, self.hovered.space)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == key.DELETE:
            self.world.delete_entity(self.selected.entity)
            if self.hovered.entity == self.selected.entity:
                self.hovered = None
            self.selected = None

    def draw(self):
        if self.hovered:
            pos = self.camera.project(self.hovered.position).xy
            arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)
            self.draw_aabb(self.hovered.space)

        if self.selected:
            self.draw_aabb(self.selected.space, color=arcade.color.RED)

    def draw_aabb(self, space, color=arcade.color.YELLOW):
        aabb = space.aabb
        bbl = self.camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.minz))
        bbr = self.camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.minz))
        fbl = self.camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.maxz))
        fbr = self.camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.maxz))

        btl = self.camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.minz))
        btr = self.camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.minz))
        ftl = self.camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.maxz))
        ftr = self.camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.maxz))

        #Bottom
        arcade.draw_line(bbl.x, bbl.y, bbr.x, bbr.y, color)
        arcade.draw_line(fbl.x, fbl.y, fbr.x, fbr.y, color)
        arcade.draw_line(bbl.x, bbl.y, fbl.x, fbl.y, color)
        arcade.draw_line(bbr.x, bbr.y, fbr.x, fbr.y, color)
        #Top
        arcade.draw_line(btl.x, btl.y, btr.x, btr.y, color)
        arcade.draw_line(ftl.x, ftl.y, ftr.x, ftr.y, color)
        arcade.draw_line(btl.x, btl.y, ftl.x, ftl.y, color)
        arcade.draw_line(btr.x, btr.y, ftr.x, ftr.y, color)
        #Sides
        arcade.draw_line(bbl.x, bbl.y, btl.x, btl.y, color)
        arcade.draw_line(fbl.x, fbl.y, ftl.x, ftl.y, color)
        arcade.draw_line(bbr.x, bbr.y, btr.x, btr.y, color)
        arcade.draw_line(fbr.x, fbr.y, ftr.x, ftr.y, color)