import glm
import pyglet.window.mouse as mouse
import arcade
from arcade import key

from ..view import View
from ..layer import Layer


class SceneView(View):
    def __init__(self, window, world, title=''):
        super().__init__(window, title)
        self.camera = None
        self.world = world
        self.processors = []
        self.layers = []

        for group in world.layers:
            self.create_layer(group)

    def add_processors(self, processors):
        for processor in processors:
            self.add_processor(processor)

    def remove_processors(self, processors):
        for processor in processors:
            self.remove_processor(processor)

    def add_processor(self, processor):
        self.processors.append(processor)

    def remove_processor(self, processor):
        self.processors.remove(processor)

    def new_layer(self):
        group = self.world.create_layer('Unnamed')
        layer = self.create_layer(group)
        layer.enable()
        return layer

    def create_layer(self, group):
        layer = Layer(self, group.name, group)
        self.add_layer(layer)
        return layer

    def add_layer(self, layer):
        self.layers.append(layer)

    def remove_layer(self, layer):
        self.layers.remove(layer)
        self.world.remove_layer(layer.group)

    def swap_layers(self, i, j):
        self.layers[i].mark()
        self.layers[j].mark()
        self.layers[i], self.layers[j] = self.layers[j], self.layers[i]

    def mark(self):
        for layer in self.layers:
            layer.mark()

    def on_show_view(self):
        super().on_show_view()
        self.mark()
        for processor in self.processors:
            #self.world.add_processor(processor)
            processor.enable()
        for layer in self.layers:
            layer.enable()

    def on_hide_view(self):
        super().on_hide_view()
        for processor in self.processors:
            #self.world.remove_processor(processor.__class__) #TODO: Weird, why doesn't esper remove by instance?
            processor.disable()
        for layer in self.layers:
            layer.disable()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.camera.resize(width, height)

    def on_update(self, delta_time: float):
        self.world.process(delta_time)
        self.camera.update()
        return super().on_update(delta_time)

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        if symbol == key.NUM_ADD:
            self.camera.zoom = self.camera.zoom + .1
        elif symbol == key.NUM_SUBTRACT:
            self.camera.zoom = self.camera.zoom - .1

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == mouse.RIGHT:
            self.camera.pan(-dx, -dy)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.camera.zoom_pct = self.camera.zoom_pct + scroll_y * 10

    def draw(self):
        for layer in self.layers:
            layer.draw()
        super().draw()

    def draw_aabb(self, aabb, color=arcade.color.YELLOW):
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