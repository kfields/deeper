import glm
import arcade

from . import Block
from .layer import Layer


class Scene:
    def __init__(self, world, camera):
        self.world = world
        self.camera = camera
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
        self.world.swap_layers(i, j)

    def mark(self):
        for layer in self.layers:
            layer.mark()

    def enable(self):
        self.mark()
        for processor in self.processors:
            processor.enable()
        for layer in self.layers:
            layer.enable()

    def disable(self):
        for processor in self.processors:
            processor.disable()
        for layer in self.layers:
            layer.disable()

    def resize(self, width: int, height: int):
        self.camera.resize(width, height)

    def update(self, delta_time: float):
        self.world.process(delta_time)
        self.camera.update()

    def cast_ray(self, ray):
        results = []
        for layer in self.layers:
            if not layer.visible:
                continue
            for entity, (_, block) in self.world.get_components(layer.group.__class__, Block):
                result = block.cast_ray(ray)
                if result:
                    results.append(result)
        if len(results) == 0:
            return None
        if len(results) == 1:
            return results[0]

        origin = ray.origin
        sorted_results = sorted(
            results, key=lambda result: glm.distance(result[0].position, origin)
        )
        return sorted_results[0]

    def draw(self):
        self.camera.use()
        for layer in self.layers:
            layer.draw()

        """
        pos = self.camera.project(self.camera.target).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)
        """

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