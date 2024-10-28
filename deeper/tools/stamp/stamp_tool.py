from loguru import logger
import glm

from crunge import sdl

from crunge.engine.imgui.widget import Window
from crunge.engine import Renderer
from crunge.engine.color import Color

from deeper import Isometry, Cuboid, Block
from deeper.constants import *
from deeper.kits import EntityKit
from ..scene_tool import SceneEditTool

from .stamp_widget import StampToolWidget
from deeper.state import SnapOption

class Hovered:
    def __init__(self, block, position):
        self.block = block
        self.position = position


class Selected:
    def __init__(self, block):
        self.block = block


class Stamp:
    def __init__(
        self,
        position=DEFAULT_VEC3,
        size=glm.vec3(CELL_WIDTH, 1, 1),
    ):
        self._position = position
        self.size = size
        self.rotation = DEFAULT_VEC3
        self.isometry = Isometry(*self._position, *self.rotation)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self.isometry = Isometry(*position, *self.rotation)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self.shape = Cuboid(size.x, size.y, size.z)

    @property
    def aabb(self):
        return self.shape.aabb(self.isometry)


class StampTool(SceneEditTool):
    def __init__(self, view, edit_state) -> None:
        super().__init__(view, edit_state, "Stamp")
        self.hovered = None
        self.selected = None
        self.stamp = None
        self.widget = Window('Stamp Tool', [StampToolWidget(self)])
        self.widget.create(self.gui)
    
    def enable(self):
        super().enable()
        self.gui.attach(self.widget)

    def disable(self):
        super().disable()
        #self.view.close_window('Catalog')
        self.gui.detach(self.widget)

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        x, y = event.x, event.y
        self.last_mouse = glm.vec2(x, y)
        #logger.debug(f"mouse: x={x}, y={y}")

        ray = self.camera.mouse_to_ray(x, y)
        result = self.scene.cast_ray(ray)
        # print(result)
        if result:
            block, contact = result
            # print("contact: ", contact)
            self.hovered = Hovered(block, contact)

            blueprint = self.edit_state.current_blueprint
            target = self.hovered.block
            if blueprint:
                position = self.compute_stamp_position(
                    blueprint, self.scene, target, contact
                )
                size = glm.vec3(blueprint.size)
                self.stamp = Stamp(position, size)

        else:
            self.hovered = None
            self.stamp = None

    def compute_stamp_position(self, blueprint, world, target, contact):
        option = self.edit_state.snap_option
        if option == SnapOption.NONE:
            return self.snap_none(blueprint, world, target, contact)
        elif option == SnapOption.CENTER:
            return self.snap_center(blueprint, world, target, contact)
        elif option == SnapOption.SIZE:
            return self.snap_size(blueprint, world, target, contact)
        elif option == SnapOption.HALF_CELL:
            return self.snap_half(blueprint, world, target, contact)
        elif option == SnapOption.QUARTER_CELL:
            return self.snap_quarter(blueprint, world, target, contact)

    def snap_none(self, blueprint, world, target, contact):
        target_space = world.component_for_entity(target, Block)
        target_pos = target_space.position
        target_aabb = target_space.aabb

        size = blueprint.size
        return glm.vec3(contact.x, target_aabb.maxy + size[1]/2, contact.z)

    def snap_center(self, blueprint, world, target, contact):
        target_space = world.component_for_entity(target, Block)
        target_pos = target_space.position
        target_aabb = target_space.aabb

        size = blueprint.size
        return glm.vec3(target_pos.x, target_aabb.maxy + size[1]/2, target_pos.z)


    def snap_size(self, blueprint, world, target, contact):
        target_space = world.component_for_entity(target, Block)
        target_pos = target_space.position
        target_aabb = target_space.aabb

        size = blueprint.size

        snap_width = size[0]
        snap_height = size[1]
        snap_depth = size[2]

        cx = round(contact[0] / snap_width) * snap_width
        cy = round(contact[1] / snap_height) * snap_height
        cz = round(contact[2] / snap_depth) * snap_depth

        return glm.vec3(cx, target_aabb.maxy + size[1] / 2, cz)

    def snap_half(self, blueprint, world, target, contact):
        target_space = world.component_for_entity(target, Block)
        target_pos = target_space.position
        target_aabb = target_space.aabb

        size = blueprint.size

        snap_width = CELL_HALF_WIDTH
        snap_height = CELL_HALF_HEIGHT
        snap_depth = CELL_HALF_DEPTH

        cx = round(contact[0] / snap_width) * snap_width
        cy = round(contact[1] / snap_height) * snap_height
        cz = round(contact[2] / snap_depth) * snap_depth

        return glm.vec3(cx, target_aabb.maxy + size[1] / 2, cz)

    def snap_quarter(self, blueprint, world, target, contact):
        target_space = world.component_for_entity(target, Block)
        target_pos = target_space.position
        target_aabb = target_space.aabb

        size = blueprint.size

        snap_width = CELL_QUARTER_WIDTH
        snap_height = CELL_QUARTER_HEIGHT
        snap_depth = CELL_QUARTER_DEPTH

        cx = round(contact[0] / snap_width) * snap_width
        cy = round(contact[1] / snap_height) * snap_height
        cz = round(contact[2] / snap_depth) * snap_depth

        return glm.vec3(cx, target_aabb.maxy + size[1] / 2, cz)

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        button = event.button
        if button == 1 and event.down and self.stamp:
            EntityKit.instance.build(
                self.edit_state.current_blueprint, self.scene, self.edit_state.current_layer, self.stamp.position
            )

    def draw(self, renderer: Renderer):
        if self.hovered:
            pos = self.camera.project(self.hovered.position).xy
            #arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)
            #self.view.draw_aabb(self.hovered.block.aabb)

        if self.stamp:
            pos = self.camera.project(self.stamp.position).xy
            self.view.draw_aabb(self.stamp.aabb)

        if self.selected:
            self.view.draw_aabb(self.selected.block.aabb, color=Color.RED)
