import glm

import arcade

from deeper.tool import WorldTool

class Hovered:
    def __init__(self, space, position):
        self.space = space
        self.position = position

class PickTool(WorldTool):
    def __init__(self, view) -> None:
        super().__init__(view)
        self.hovered = None

    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        print("mouse: ", mouse_x, mouse_y)
        ray = self.camera.mouse_to_ray(mouse_x, mouse_y)
        result = self.world.cast_ray(ray)
        print(result)
        if result:
            space, contact = result
            print("contact: ", contact)
            self.hovered = Hovered(space, glm.vec3(contact))
        else:
            self.hovered = None

    def draw(self):
        if self.hovered:
            pos = self.camera.project(self.hovered.position).xy
            arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)
            self.draw_aabb(self.hovered.space)

    def draw_aabb(self, space):
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
        arcade.draw_line(bbl.x, bbl.y, bbr.x, bbr.y, arcade.color.YELLOW)
        arcade.draw_line(fbl.x, fbl.y, fbr.x, fbr.y, arcade.color.YELLOW)
        arcade.draw_line(bbl.x, bbl.y, fbl.x, fbl.y, arcade.color.YELLOW)
        arcade.draw_line(bbr.x, bbr.y, fbr.x, fbr.y, arcade.color.YELLOW)
        #Top
        arcade.draw_line(btl.x, btl.y, btr.x, btr.y, arcade.color.YELLOW)
        arcade.draw_line(ftl.x, ftl.y, ftr.x, ftr.y, arcade.color.YELLOW)
        arcade.draw_line(btl.x, btl.y, ftl.x, ftl.y, arcade.color.YELLOW)
        arcade.draw_line(btr.x, btr.y, ftr.x, ftr.y, arcade.color.YELLOW)
        #Sides
        arcade.draw_line(bbl.x, bbl.y, btl.x, btl.y, arcade.color.YELLOW)
        arcade.draw_line(fbl.x, fbl.y, ftl.x, ftl.y, arcade.color.YELLOW)
        arcade.draw_line(bbr.x, bbr.y, btr.x, btr.y, arcade.color.YELLOW)
        arcade.draw_line(fbr.x, fbr.y, ftr.x, ftr.y, arcade.color.YELLOW)