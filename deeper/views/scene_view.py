from loguru import logger
import glm

from crunge import sdl
from crunge.engine import Renderer
from crunge.engine.d2.renderer_2d import Renderer2D
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

    def _create(self, window):
        super()._create(window)
        self.scene_camera = SceneCamera(self.camera)
        self.scene.camera = self.scene_camera

    def enable(self):
        super().enable()
        self.scene.camera = self.scene_camera
        self.scene.enable()
        #super().enable()

    def disable(self):
        super().disable()
        self.scene.disable()

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.scene.resize(size)

    def update(self, delta_time: float):
        self.scene.update(delta_time)
        return super().update(delta_time)

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        state = event.state

        if key == sdl.SDLK_KP_PLUS:
            self.camera.zoom = self.camera.zoom + .1
        elif key == sdl.SDLK_KP_MINUS:
            self.camera.zoom = self.camera.zoom - .1

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        #logger.debug(f"{self.view.title}:{self.title}:on_mouse_press")
        button = event.button
        action = event.state == 1

        if button != 3:
            return
        if action:
            self.dragging = True
        else:
            self.dragging = False

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        super().on_mouse_motion(event)
        if not self.dragging:
            return
        zoom = self.scene.camera.zoom
        sensitivity = 0.1
        dx = -event.xrel * zoom * sensitivity
        dy = event.yrel * zoom * sensitivity
        self.scene.camera.pan(dx, dy)

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        #logger.debug(f"{self.title}:on_mouse_wheel")
        self.scene.camera.zoom_pct = self.scene.camera.zoom_pct + event.y * 10

    def draw(self, renderer: Renderer2D):
        # logger.debug("DemoView.draw()")
        self.renderer.texture_view = renderer.texture_view
        
        with self.renderer:
            self.scene.draw(self.renderer)

        super().draw(renderer)

    def draw_aabb(self, aabb, color=Color.YELLOW):
        bbl = self.scene.camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.minz)).xy
        bbr = self.scene.camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.minz)).xy
        fbl = self.scene.camera.project(glm.vec3(aabb.minx, aabb.miny, aabb.maxz)).xy
        fbr = self.scene.camera.project(glm.vec3(aabb.maxx, aabb.miny, aabb.maxz)).xy

        btl = self.scene.camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.minz)).xy
        btr = self.scene.camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.minz)).xy
        ftl = self.scene.camera.project(glm.vec3(aabb.minx, aabb.maxy, aabb.maxz)).xy
        ftr = self.scene.camera.project(glm.vec3(aabb.maxx, aabb.maxy, aabb.maxz)).xy

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
