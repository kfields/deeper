import glm
import arcade
from arcade.gui import UIManager

from .dimgui import ViewGui
from .tool import Tool

class View(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        self.ui_manager = UIManager(window)
        self.gui = ViewGui(self, auto_enable=False)
        self.current_tool: Tool = None
        
    def use_tool(self, tool: Tool):
        if tool == self.current_tool:
            return
        if self.current_tool:
            self.current_tool.disable()
                        
        self.current_tool = tool
        self.gui.disable()
        tool.enable()
        self.gui.enable()

    def draw(self):
        pass

    def on_draw(self):
        super().on_draw()
        arcade.start_render()
        self.gui.start_render()

        self.ui_manager.draw()

        self.draw()

        if self.current_tool:
            self.current_tool.draw()

        self.gui.finish_render()
        arcade.finish_render()


    def on_show_view(self):
        super().on_show_view()
        self.ui_manager.enable()
        self.gui.enable()

    def on_hide_view(self):
        super().on_hide_view()
        self.ui_manager.disable()
        self.gui.disable()

class WorldView(View):
    def on_update(self, delta_time: float):
        self.world.process(delta_time)
        return super().on_update(delta_time)

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