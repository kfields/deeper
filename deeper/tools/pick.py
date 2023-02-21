from loguru import logger

import glm
from pyglet import clock
import pyglet.window.mouse as mouse
import arcade
from arcade import key

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

class PickTool(WorldEditTool):
    def __init__(self, view, edit_state) -> None:
        super().__init__(view, edit_state, 'Pick')
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
            self.hovered = Hovered(entity, block, contact)
        else:
            self.hovered = None

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        #logger.debug(f"{self.view.title}:{self.title}:on_mouse_press")
        if button != mouse.LEFT or not self.hovered:
            return
        
        self.selected = Selected(self.hovered.entity, self.hovered.block)
        if self._click_count == 2:
            #self.push_entity_editor()
            clock.schedule_once(lambda dt, *args, **kwargs : self.push_entity_editor(), 0)
            return


    def push_entity_editor(self):
        from deeper.state import EntityEditState
        from deeper.views.entity_editor import EntityEditor
        self.window.push_view(EntityEditor(self.window, EntityEditState(self.world, self.selected.entity)))

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == key.DELETE and self.selected:
            self.world.delete_entity(self.selected.entity)
            if self.hovered and self.hovered.entity == self.selected.entity:
                self.hovered = None
            self.selected = None
        elif symbol == key.ESCAPE:
            self.selected = None

    def draw(self):
        if self.hovered:
            pos = self.camera.project(self.hovered.position)
            #print("self.hovered.position: ", self.hovered.position)
            #print("pos: ", pos)
            #arcade.draw_circle_outline(*pos.xy, 18, arcade.color.RED, 3)
            self.view.draw_aabb(self.hovered.block.aabb)

        if self.selected:
            self.view.draw_aabb(self.selected.block.aabb, color=arcade.color.RED)
