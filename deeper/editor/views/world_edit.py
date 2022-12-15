import math
import glm
import arcade
#from arcade.resources import resolve_resource_path
import imgui

from deeper.view import View
from deeper import Space, Cuboid
from deeper.constants import *
from deeper.camera import WorldCamera
from deeper.vu.sprite_vu import SpriteVu
from deeper.processor.rendering import RenderingProcessor
from deeper.catalog import Catalog
from deeper.dimgui import Gui
from deeper.editor.widgets import MainMenu, CatalogWidget
#from deeper.resources.icons.icons_material_design import IconsMaterialDesign


class Hover:
    def __init__(self, space, position):
        self.space = space
        self.position = position

class WorldEditView(View):
    def __init__(self, window, world):
        super().__init__(window)
        self.world = world
        #self.gui = Gui(self.window)
        self.gui = window.gui
        self.gui.add_child(MainMenu())
        #TODO:Need glyph range which pyimgui does not support. :(
        #self.gui.load_font(resolve_resource_path(f':deeper:icons/{IconsMaterialDesign.FONT_ICON_FILE_NAME_MD}'))

        self.catalog = Catalog(self.window)
        self.gui.add_child(CatalogWidget(self.catalog))

        self.camera = WorldCamera(self, glm.vec3(), 1)
        #self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*4, 0, CELL_DEPTH*4), 1)
        #self.camera = WorldCamera(self, glm.vec3(CELL_WIDTH*8, 0, CELL_DEPTH*8), 1)
        self.tile_vu_list = []
        self.tile_list = arcade.SpriteList()
        self.space = Space()
        self.hover = None

        self.create_blocks()

        self.world.add_processor(RenderingProcessor(self))


    def create_blocks(self):
        rotation = glm.vec3()
        shape = Cuboid(CELL_WIDTH, CELL_HEIGHT, CELL_DEPTH)
        for ty in range(0, 8):
            y_distance = CELL_DEPTH * ty
            for tx in range(0, 8):
                x_distance = CELL_WIDTH * tx
                position = glm.vec3(x_distance, CELL_HEIGHT, y_distance)
                #print("position: ", position)
                block = Space(position, rotation, shape)
                self.space.add_child(block)
                vu = SpriteVu(arcade.Sprite(
                    ":deeper:tiles/FloorD3.png", scale=1 / self.camera.zoom
                ))
                self.world.create_entity(block, vu)

    def on_draw(self):
        arcade.start_render()
        self.gui.start_render()

        self.camera.use() #TODO: This is messing with ImGui on resize...
        self.tile_list.draw()

        #self.draw_aabbs()

        pos = self.camera.project(self.camera.target).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.TURQUOISE, 3)

        pos = self.camera.project(self.camera.position).xy
        arcade.draw_circle_outline(*pos, 18, arcade.color.WISTERIA, 3)

        if self.hover:
            pos = self.camera.project(self.hover.position).xy
            arcade.draw_circle_outline(*pos, 18, arcade.color.RED, 3)
        
        self.gui.finish_render()
        arcade.finish_render()

    def draw_aabbs(self):
        for space in self.space.children:
            self.draw_aabb(space)

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

        arcade.draw_line(bbl.x, bbl.y, bbr.x, bbr.y, arcade.color.YELLOW)
        #arcade.draw_line(fbl.x, fbl.y, fbr.x, fbr.y, arcade.color.YELLOW)
        arcade.draw_line(bbl.x, bbl.y, fbl.x, fbl.y, arcade.color.YELLOW)

        arcade.draw_line(btl.x, btl.y, btr.x, btr.y, arcade.color.YELLOW)
        #arcade.draw_line(fbl.x, fbl.y, fbr.x, fbr.y, arcade.color.YELLOW)
        arcade.draw_line(btl.x, btl.y, ftl.x, ftl.y, arcade.color.YELLOW)

    def on_mouse_motion(self, mouse_x, mouse_y, mouse_dx, mouse_dy):
        print("mouse: ", mouse_x, mouse_y)
        ray = self.camera.mouse_to_ray(mouse_x, mouse_y)
        result = self.space.cast_ray(ray)
        print(result)
        if result:
            space, contact = result
            print("contact: ", contact)
            self.hover = Hover(space, glm.vec3(contact))
        else:
            self.hover = None
