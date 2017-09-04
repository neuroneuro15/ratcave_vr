import pyglet
import ratcave as rc
from collections import namedtuple
from pypixxlib import propixx
import json
import logging
import cfg

RenderCollection = namedtuple("RenderCollection", "shader fbo quad")


def load_projected_scene(arena_file, projector_file, motive_client):
    """Scene-building convenience function. Returns (scene, arena, arena_rb) from filenames and motive."""
    arena = rc.WavefrontReader(arena_file).get_mesh('Arena')
    arena.uniforms['diffuse'] = 1., 1, 1
    arena.uniforms['flat_shading'] = False
    arena.rotation = arena.rotation.to_quaternion()

    arena_rb = motive_client.rigid_bodies['Arena']
    arena.position.xyz = arena_rb.position
    arena.rotation.wxyz = arena_rb.quaternion

    scene = rc.Scene(meshes=[arena], bgColor=(.6, 0, 0))
    scene.gl_states = scene.gl_states[:-1]

    beamer = rc.Camera.from_pickle(projector_file)
    scene.camera.position.xyz = beamer.position.xyz
    scene.camera.rotation.xyz = beamer.rotation.xyz
    scene.camera.projection.fov_y = 41.5
    scene.camera.projection.aspect = 1.7778

    scene.light.position.xyz = scene.camera.position.xyz
    return scene, arena, arena_rb


def setup_deferred_rendering():
    """Return (Shader, FBO, QuadMesh) for deferred rendering."""
    fbo = rc.FBO(rc.Texture(width=4096, height=4096, mipmap=True))
    quad = rc.gen_fullscreen_quad("DeferredQuad")
    quad.texture = fbo.texture
    shader = rc.Shader.from_file(*rc.resources.deferredShader)
    return RenderCollection(shader=shader, fbo=fbo, quad=quad)


def setup_grey3x_rendering(update_projector=False):
    """
    Return (Shader, FBO, QuadMesh) for rendering in Propixx's 'GREY3X' mode. If desired, can
    also apply the settings to the beamer to set it to this mode (caution: won't change back afterward).
    """

    if update_projector:
        beamer = propixx.PROPixx()
        beamer.setDlpSequencerProgram('GREY3X')

    vert_shader = open(rc.resources.deferredShader.vert).read()
    frag_shader = """
    #version 400
    #extension GL_ARB_texture_rectangle : enable

    uniform sampler2D TextureMap;

    in vec2 texCoord;
    out vec3 color;

    void main( void ) {

        if (gl_FragCoord.x * 3 + 1 < 1920){
            color = vec3(texture2D(TextureMap, vec2(floor(gl_FragCoord.x * 3. + 0.0) / 1920.0, gl_FragCoord.y / 1080.0)).r,
                         texture2D(TextureMap, vec2(floor(gl_FragCoord.x * 3. + 1.0) / 1920.0, gl_FragCoord.y / 1080.0)).r,
                         texture2D(TextureMap, vec2(floor(gl_FragCoord.x * 3. + 2.0) / 1920.0, gl_FragCoord.y / 1080.0)).r
                         );

        } else {
            color = vec3(.2, 0., 0.);
        }
        return;
    }
    """

    shader = rc.Shader(vert=vert_shader, frag=frag_shader)
    quad = rc.gen_fullscreen_quad('Grey3xQuad')
    return RenderCollection(shader=shader, fbo=None, quad=quad)


def create_and_configure_experiment_logs(filename, motive_client, exclude_subnames=[]):
    """
    Sets the csv logging config and writes the json sesssion config log from cfg.py, excluding all variables that contain
    any of the substrings in 'exclude_subnames'.
    """
    filename_settings = 'logs/settings_logs/' + filename + '.json'
    with open(filename_settings, 'w') as f:
        json.dump({var: cfg.__dict__[var] for var in dir(cfg) if not '_' in var[0] and not any(substring in var for substring in exclude_subnames)}, f, sort_keys=True, indent=4)

    filename_log = 'logs/event_logs/' + filename + '.csv'
    with open(filename_log, 'a') as f:
        f.write('DateTime; MotiveExpTimeSecs; Event; EventArguments\n')

    logging.basicConfig(filename=filename_log,
                        level=logging.INFO, format='%(asctime)s; %(message)s')

    motive_client.set_take_file_name(file_name=filename)
