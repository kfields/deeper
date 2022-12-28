import glm

import arcade
from arcade import key

from deeper.architect import Architect
from .tool import WorldEditTool

class Hovered:
    def __init__(self, entity, block, position):
        self.entity = entity
        self.block = block
        self.position = position

class Selected:
    def __init__(self, entity, block):
        self.entity = entity
        self.block = block

class StampTool(WorldEditTool):
    def __init__(self, view, edit_state) -> None:
        super().__init__(view, edit_state)
        self.hovered = None
        self.selected = None

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        #print("mouse: ", x, y)
        ray = self.camera.mouse_to_ray(x, y)
        result = self.world.cast_ray(ray)
        #print(result)
        if result:
            entity, block, contact = result
            #print("contact: ", contact)
            self.hovered = Hovered(entity, block, glm.vec3(contact))
        else:
            self.hovered = None

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.hovered and self.edit_state.current_blueprint:
            Architect.instance.build(self.edit_state.current_blueprint, self.world, self.hovered.entity)

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
            self.view.draw_aabb(self.hovered.block.aabb)

        if self.selected:
            self.view.draw_aabb(self.selected.block.aabb, color=arcade.color.RED)