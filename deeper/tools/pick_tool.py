from loguru import logger

import glm

from crunge import sdl
from crunge.engine import Renderer, Scheduler
from crunge.engine.color import Color
from .scene_tool import SceneEditTool


class Hovered:
    def __init__(self, block, position):
        self.block = block
        self.position = position

class Selected:
    def __init__(self, block):
        self.block = block

class PickTool(SceneEditTool):
    def __init__(self, view, edit_state) -> None:
        super().__init__(view, edit_state, 'Pick')
        self.hovered = None
        self.selected = None

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        super().on_mouse_motion(event)
        x, y = event.x, event.y
        self.last_mouse = glm.vec2(x, y)
        #logger.debug(f"mouse: x={x}, y={y}")

        ray = self.camera.mouse_to_ray(x, y)
        result = self.scene.cast_ray(ray)
        #print(result)
        if result:
            block, contact = result
            #print("contact: ", contact)
            self.hovered = Hovered(block, contact)
        else:
            self.hovered = None

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        #logger.debug(f"{self.view.title}:{self.title}:on_mouse_press")
        button = event.button
        action = event.state == 1

        if button != 1 or not self.hovered:
            return
        
        self.selected = Selected(self.hovered.block)

        if event.clicks == 2:
            Scheduler().schedule_once(lambda dt : self.push_entity_editor(), 0)
            return


    def push_entity_editor(self):
        from deeper.state import EntityEditState
        from deeper.views.entity_editor import EntityEditor
        self.window.push_view(EntityEditor(EntityEditState(self.scene, self.selected.block)).create(self.window))

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        state = event.state

        if key == sdl.SDLK_DELETE and self.selected:
            self.scene.delete_entity(self.selected.block)
            if self.hovered and self.hovered.block == self.selected.block:
                self.hovered = None
            self.selected = None
        elif key == sdl.SDLK_ESCAPE:
            self.selected = None

    def draw(self, renderer: Renderer):
        if self.hovered:
            pos = self.camera.project(self.hovered.position)
            #print("self.hovered.position: ", self.hovered.position)
            #print("pos: ", pos)
            #arcade.draw_circle_outline(*pos.xy, 18, arcade.color.RED, 3)
            self.view.draw_aabb(self.hovered.block.aabb)

        if self.selected:
            self.view.draw_aabb(self.selected.block.aabb, color=Color.RED)
