from loguru import logger
import glm

from crunge import sdl
from crunge.engine import Renderer
from crunge.engine.color import Color

from ..view import View
from ..scene import Scene

from ..scene_camera import SceneCamera

class SceneView(View):
    scene: Scene = None

    def __init__(self, scene, title=''):
        super().__init__(title)
        self.scene = scene
        self.scene_camera: SceneCamera = None
        self.dragging = False

    #def create(self, window):
    def create(self):
        #super().create(window)
        super().create()
        self.scene_camera = SceneCamera(self.camera)
        self.scene_camera = self.scene_camera

    def enable(self):
        super().enable()
        #self.scene_camera = self.scene_camera
        self.scene.enable()
        #super().enable()

    def disable(self):
        super().disable()
        self.scene.disable()

    def on_size(self):
        super().on_size()
        size = self.size
        if self.scene_camera is not None:
            self.scene_camera.resize(size)

    '''
    def resize(self, size: glm.ivec2):
        super().resize(size)
        #self.scene.resize(size)
        self.scene_camera.resize(size)
    '''

    def update(self, delta_time: float):
        self.scene.update(delta_time)
        return super().update(delta_time)

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        down = event.down

        if key == sdl.SDLK_KP_PLUS:
            self.camera.zoom = self.camera.zoom - .1
        elif key == sdl.SDLK_KP_MINUS:
            self.camera.zoom = self.camera.zoom + .1

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        #logger.debug(f"{self.view.title}:{self.title}:on_mouse_press")
        button = event.button

        if button != 3:
            return
        if event.down:
            self.dragging = True
        else:
            self.dragging = False

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        super().on_mouse_motion(event)
        if not self.dragging:
            return
        zoom = self.scene_camera.zoom
        sensitivity = 0.1
        dx = -event.xrel * zoom * sensitivity
        dy = event.yrel * zoom * sensitivity
        self.scene_camera.pan(dx, dy)

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        #logger.debug(f"{self.title}:on_mouse_wheel")
        self.scene_camera.zoom_pct = self.scene_camera.zoom_pct + event.y * 10

    def draw(self, renderer: Renderer):
        self.renderer.viewport = renderer.viewport
        
        with self.renderer:
            self.scene.draw(self.renderer)

        super().draw(renderer)

    def draw_aabb(self, aabb, color=Color.YELLOW):
        bbl = self.scene_camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.minz)).xy
        bbr = self.scene_camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.minz)).xy
        fbl = self.scene_camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.maxz)).xy
        fbr = self.scene_camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.maxz)).xy

        btl = self.scene_camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.minz)).xy
        btr = self.scene_camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.minz)).xy
        ftl = self.scene_camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.maxz)).xy
        ftr = self.scene_camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.maxz)).xy

        #Bottom
        self.scratch.draw_line(bbl, bbr, color)
        self.scratch.draw_line(fbl, fbr, color)
        self.scratch.draw_line(bbl, fbl, color)
        self.scratch.draw_line(bbr, fbr, color)
        #Top
        self.scratch.draw_line(btl, btr, color)
        self.scratch.draw_line(ftl, ftr, color)
        self.scratch.draw_line(btl, ftl, color)
        self.scratch.draw_line(btr, ftr, color)
        #Sides
        self.scratch.draw_line(bbl, btl, color)
        self.scratch.draw_line(fbl, ftl, color)
        self.scratch.draw_line(bbr, btr, color)
        self.scratch.draw_line(fbr, ftr, color)
