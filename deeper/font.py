import pyglet
from pyglet.gl import *
from pyglet.gl.gl_compat import *
from ctypes import byref

def render_text_to_image(text, font_name='Material Icons', font_size=32):
    # Ensure you have a GL context to do the rendering
    config = pyglet.gl.Config(double_buffer=False)
    window = pyglet.window.Window(1, 1, config=config, visible=False)
    
    # Create a label
    label = pyglet.text.Label(text, font_name=font_name, font_size=font_size)

    # Get the width and height of the label
    width, height = label.content_width, label.content_height

    # Create a framebuffer to render to
    #image   = pyglet.image.create(width, height)
    #texture = image.get_texture()
    texture = pyglet.image.Texture.create(width, height)

    fbo_id = GLuint(0)
    glGenFramebuffers(1, byref(fbo_id))
    glBindFramebuffer(GL_FRAMEBUFFER, fbo_id)

    glBindTexture(GL_TEXTURE_2D, texture.id)

    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture.id, 0)

    res = glCheckFramebufferStatus(GL_FRAMEBUFFER)
    if res != GL_FRAMEBUFFER_COMPLETE:
        raise RuntimeError('Framebuffer not completed')

    # Clear and draw the label to the buffer
    '''
    glPushAttrib(GL_ENABLE_BIT)
    glDisable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(1, 1, 1, 0)  # Clear with transparent white
    glClear(GL_COLOR_BUFFER_BIT)
    '''
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3f(1.0, 1.0, 1.0)

    label.draw()

    # Clean up and close the window
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    window.close()

    return texture

'''
def render_text_to_image(text, font_name='Arial', font_size=36, output_file='output.png'):
    # Ensure you have a GL context to do the rendering
    config = pyglet.gl.Config(double_buffer=False)
    window = pyglet.window.Window(1, 1, config=config, visible=False)
    
    # Load the desired font and size
    font = pyglet.font.load(font_name, font_size)

    # Create a label
    label = pyglet.text.Label(text, font_name=font_name, font_size=font_size)

    # Get the width and height of the label
    width, height = label.content_width, label.content_height

    # Create a framebuffer to render to
    buffer = pyglet.image.Texture.create_for_size(GL_TEXTURE_2D, width, height, GL_RGBA)
    glBindFramebuffer(GL_FRAMEBUFFER, buffer.id)

    # Clear and draw the label to the buffer
    glPushAttrib(GL_ENABLE_BIT)
    glDisable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(1, 1, 1, 0)  # Clear with transparent white
    glClear(GL_COLOR_BUFFER_BIT)
    label.draw()

    # Save the buffer to an image file
    buffer.save(output_file)

    # Clean up and close the window
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    window.close()
'''