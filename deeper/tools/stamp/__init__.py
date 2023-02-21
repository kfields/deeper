import glm

import pyglet.window.mouse as mouse
import arcade
from arcade import key

from deeper import Isometry, Cuboid, Block
from deeper.constants import *
from deeper.kits import EntityKit
from ..tool import WorldEditTool

from deeper.dimgui import Window
from .stamp_widget import StampToolWidget
from deeper.state import SnapOption

class Hovered:
    def __init__(self, entity, block, position):
        self.entity = entity
        self.block = block
        self.position = position


class Selected:
    def __init__(self, entity, block):
        self.entity = entity
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


class StampTool(WorldEditTool):
    def __init__(self, view, edit_state) -> None:
        super().__init__(view, edit_state, "Stamp")
        self.hovered = None
        self.selected = None
        self.stamp = None
        self.widget = Window('Stamp Tool', [StampToolWidget(self)])
        self.widget.create(self.gui)

    def enable(self):
        super().enable()
        self.gui.add_child(self.widget)

    def disable(self):
        super().disable()
        self.gui.remove_child(self.widget)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        # print("mouse: ", x, y)
        ray = self.camera.mouse_to_ray(x, y)
        result = self.world.cast_ray(ray)
        # print(result)
        if result:
            entity, block, contact = result
            # print("contact: ", contact)
            self.hovered = Hovered(entity, block, contact)

            blueprint = self.edit_state.current_blueprint
            target = self.hovered.entity
            if blueprint:
                position = self.compute_stamp_position(
                    blueprint, self.world, target, contact
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

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        #print("stamp")
        if button == mouse.LEFT and self.stamp:
            EntityKit.instance.build(
                self.edit_state.current_blueprint, self.world, self.edit_state.current_layer, self.stamp.position
            )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == key.DELETE:
            self.world.delete_entity(self.selected.entity)
            if self.hovered.entity == self.selected.entity:
                self.hovered = None
            self.selected = None

    def draw(self):
        if self.hovered:
            pos = self.camera.project(self.hovered.position).xy
            #arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)
            #self.view.draw_aabb(self.hovered.block.aabb)

        if self.stamp:
            pos = self.camera.project(self.stamp.position).xy
            self.view.draw_aabb(self.stamp.aabb)

        if self.selected:
            self.view.draw_aabb(self.selected.block.aabb, color=arcade.color.RED)
