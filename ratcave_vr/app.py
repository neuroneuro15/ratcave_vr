from __future__ import print_function

import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['debug_gl_trace'] = False

import ratcave as rc
from natnetclient import NatClient


motive = NatClient(read_rate=2000, )
if not motive.rigid_bodies:
    raise IOError("Not Detecting Rigid Bodies.  Turn RigidBody Streaming On in the Motive Streaming Pane.")

if not motive.rigid_bodies['Arena'].position:
    raise IOError("Not Detecting Arena Position.  Turn RigidBody Streaming on in the Motive Streaming Pane.")



class RatcaveApp(pyglet.window.Window):

    def __init__(self, arena_objfile, projector_file, fullscreen=True, screen=1, antialiasing=True, vsync=False, fps_mode=False, *args, **kwargs):
        """
        A Pyglet Window that sets up the arena, beamer, and virtual scenes, along with motive update and draw functions
        for updating and rendering a virtual reality environment in a ratCAVE setup.
        """
        self.__display = pyglet.window.get_platform().get_default_display()
        self.__screen = self.__display.get_screens()[screen]
        super(self.__class__, self).__init__(fullscreen=fullscreen, screen=self.__screen, vsync=vsync, *args, **kwargs)

        self.cube_fbo = rc.FBO(texture=rc.TextureCube(width=4096, height=4096))

        self.active_scene, self.arena,  self.arena_rb = utils.load_projected_scene(arena_file=arena_objfile,
                                                    projector_file=projector_file,
                                                    motive_client=motive)

        self.orig_texture = None

        self.shader = rc.Shader.from_file(*rc.resources.genShader)
        self._vr_scenes = set()
        self.current_vr_scene = None

        self.rat_rb = motive.rigid_bodies['Rat']

        self.antialiasing = antialiasing
        self.fbo_aa = rc.FBO(rc.Texture(width=4096, height=4096, mipmap=True))
        self.aa_quad = rc.gen_fullscreen_quad()
        self.aa_quad.texture = self.fbo_aa.texture
        self.shader_deferred = rc.Shader.from_file(*rc.resources.deferredShader)
        if fps_mode:
            pass
            # raise NotImplementedError("Haven't gotten fps_mode to work properly yet.")
        self.fps_mode = fps_mode

        pyglet.clock.schedule(self.update)

    def on_draw(self):
        """Render the virtual environment."""
        if self.fps_mode:
            with self.shader:
                if self.current_vr_scene:
                    self.current_vr_scene.draw()
                else:
                    self.active_scene.draw()
        else:
            with self.shader:
                if self.current_vr_scene:
                    with self.cube_fbo as fbo:
                        self.current_vr_scene.draw360_to_texture(fbo.texture)
                if self.antialiasing:
                    with self.fbo_aa:
                        self.active_scene.draw()
                else:
                    self.active_scene.draw()

            if self.antialiasing:
                with self.shader_deferred:
                    self.aa_quad.draw()

    def update(self, dt):
        """Update arena position and vr_scene's camera to match motive's Arena and Rat rigid bodies."""
        self.arena.position.xyz = self.arena_rb.position
        self.arena.rotation.xyzw = self.arena_rb.quaternion

        if self.current_vr_scene:
            if sum(self.rat_rb.position) != 0:
                self.current_vr_scene.camera.position.xyz = self.rat_rb.position
                self.current_vr_scene.camera.rotation.xyzw = self.rat_rb.quaternion
                self.current_vr_scene.camera.uniforms['playerPos'] = self.current_vr_scene.camera.position.xyz

    @property
    def vr_scenes(self):
        return tuple(self._vr_scenes)

    @vr_scenes.setter
    def vr_scenes(self, value):
        raise AttributeError("RatcaveApp.vr_scenes can not be directly assigned.  Instead, use the RatcaveApp.add_vr_scene() method.")

    def register_vr_scene(self, scene, parent_to_arena=True, match_light_to_beamer=True, make_cube_camera=True, face_culling=False):
        """appends a virtual scene to the app, making any changes to the arena needed to display it correctly.
        Will also make it the current vr_scene automatically.
        """
        if not isinstance(scene, rc.Scene):
            raise TypeError("scene must be a ratcave Scene instance.")

        if not self.vr_scenes:
            if self.arena.texture:
                self.orig_texture = self.arena.texture
            self.arena.texture = self.cube_fbo.texture

        if parent_to_arena:
            for mesh in scene.meshes:
                mesh.parent = self.arena

        if match_light_to_beamer:
            scene.light.position.xyz = self.active_scene.light.position.xyz

        if make_cube_camera:
            scene.camera.rotation = scene.camera.rotation.to_quaternion()
            scene.camera.projection.aspect = 1.
            scene.camera.projection.fov_y = 90.
            scene.camera.projection.z_near = .004
            scene.camera.projection.z_far = 2.

        if not face_culling:
            scene.gl_states = scene.gl_states[:-1]

        if self.fps_mode:
            scene.camera.projection.fov_y = 120

        self._vr_scenes.add(scene)
        self.current_vr_scene = scene

    @property
    def current_vr_scene(self):
        return self._current_vr_scene

    @current_vr_scene.setter
    def current_vr_scene(self, scene):
        if not isinstance(scene, (rc.Scene, type(None))):
            raise TypeError("current_vr_scene must be a ratcave.Scene or None")
        if isinstance(scene, type(None)):
            self._current_vr_scene = None
            if self.orig_texture:
                self.arena.texture = self.orig_texture
            return
        if scene not in self.vr_scenes:
            raise ValueError("scene not in vr_scenes.  Use RatcaveApp.register_vr_scene() to register the scene first.")
        self._current_vr_scene = scene
        self.arena.texture = self.cube_fbo.texture

    def run(self):
        """Runs the application's event loop."""
        pyglet.app.run()
