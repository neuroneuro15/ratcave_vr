""" In this file you will find the shaders for all VPixx devices different modes

You will need to compile them using a normal vertex shader and a shader compiler.

To access a shader, use the ``getShader(my_device)`` functions.

We suggest combining this with PsychoPy and FBO (frame buffer objects), as such:

Example:
    my_monitor = monitors.Monitor('DATAPixx', width=40, distance=60, gamma=2.2)
    my_monitor.setSizePix([800,600])
    win = visual.Window([800,600], useFBO=True, fullscr=True, screen = 1, units='deg', monitor=my_monitor, gamma=1)
    
    my_device  = DATAPixx()
    my_device.setVideoMode('M16')
    my_device.updateRegisterCache()
    
    shaders.setUpShaderAndWindow(my_device, win)


Possible modes:

    - **L48**: DVI RED[7:0] is used as an index into a 256-entry 16-bit RGB colour lookup table.
    - **M16**: DVI RED[7:0] & GREEN[7:0] concatenate into a VGA 16-bit value sent to all three RGB components.
    - **C48**: Even/Odd pixel RED/GREEN/BLUE[7:0] concatenate to generate 16-bit RGB components at half the horizontal resolution.
    - **L48D**: DVI RED[7:4] & GREEN[7:4] concatenate to form an 8-bit index into a 256-entry 16-bit RGB colour lookup table.
    - **M16D**: DVI RED[7:3] & GREEN[7:3] & BLUE[7:2] concatenate into a VGA 16-bit value sent to all three RGB components.
    - **C36D**: Even/Odd pixel RED/GREEN/BLUE[7:2] concatenate to generate 12-bit RGB components at half the horizontal resolution.
    - **C24**: Straight passthrough from DVI 8-bit (or HDMI "deep" 10/12-bit) RGB to VGA 8/10/12-bit RGB.    
"""


def setUpShaderAndWindow(device, window):
    """Sets up the appropriate shader and functions for the window to work
    
    Args:
        device (pypixxlib object): The current object handle for your device
        window (PsychoPy.Window object): A PsychoPy Window object
        
    Returns:
        int: The OpenGL program number for the generated shader.
    """
    shader_dict = {'L48': no_mode_Shader,
                   'C24': no_mode_Shader,
                   'M16': M16_mode_Shader,
                   'M16O': M16O_mode_Shader,
                   'C48': C48_mode_Shader,
                   'L48D': L48D_mode_Shader,
                   'M16D': M16D_mode_Shader,
                   'C36D': C36D_mode_Shader,
                   }

    vid_mode = device.getVideoMode()
    shader = shader_dict[vid_mode]
    if not hasattr(window, '_prepareFBOrender'):
        raise "Window does not have FBO."
    # Compile the shader
    from psychopy._shadersPyglet import compileProgram, vertSimple
    from OpenGL.GL import glUseProgram

    compiled_shader = compileProgram(vertSimple, shader)
    def _prepareFBOrender():
        glUseProgram(compiled_shader)
    def _finishFBOrender():
        glUseProgram(0)
    def _afterFBOrender():
        pass
    window._prepareFBOrender = _prepareFBOrender
    window._finishFBOrender = _finishFBOrender
    window._afterFBOrender = _afterFBOrender
    window._DPShaderProg = compiled_shader
    return compiled_shader

def setUpGammaCorrection(device, window, monitor, gamma_information=None):
    """Sets up the gamma correction for the appropriate video mode
    
    Args:
        device (pypixxlib object): The current object handle for your device
        window (PsychoPy.Window object): A PsychoPy Window object
        monitor (PsychoPy.Monitor object): The current monitor being used
        gamma_information (list, optional): The gamma information if it is not contained in the monitor.
    """
    vid_mode = device.getVideoMode()
    if vid_mode is 'M16':
        setUpM16gammaCorrection(window, monitor, gamma_information)
        return
    if vid_mode is 'C48':
        setUpC48gammaCorrection(window, monitor, gamma_information)
        return
    print "Gamma correction only supported for M16 and C48 video modes."
        
    
def setUpM16gammaCorrection(window, monitor, gamma_information=None):
    """Sets up the gamma correction for M16
    
    Args:
        window (PsychoPy.Window object): A PsychoPy Window object
        monitor (PsychoPy.Monitor object): The current monitor being used
        gamma_information (list, optional): The gamma information if it is not contained in the monitor. (gamma, b, k)
    """
    if not hasattr(window, '_DPShaderProg'):
        raise Warning("Shader not set up! make sure you call setUpShaderAndWindow before setting up gamma correction.")
        return
    
    from OpenGL.GL import glUseProgram, glUniform3f, glGetUniformLocation, glUniform1i
    glUseProgram(window._DPShaderProg)
    
    loc = glGetUniformLocation(window._DPShaderProg, "gamma_information")
    if loc == -1:
        raise Warning("The current shader is not the right shader, are you sure you are in M16 mode?")
        return
    
    if gamma_information is None:
        grid = monitor.getGammaGrid()
        if grid is None:
            raise Warning("You did not provide gamma information and your monitor does not have any.")
            return
        gamma_information = [grid[1][2], grid[1][4], grid[1][5]] # gamma, b, k
    
    glUniform3f(glGetUniformLocation(window._DPShaderProg, "gamma_information"), gamma_information[0], gamma_information[1] , gamma_information[2])
    glUniform1i(glGetUniformLocation(window._DPShaderProg, "gamma_correction_flag"), 1);
    
def setUpC48gammaCorrection(window, monitor, gamma_grid=None):
    """Sets up the gamma correction for C48
    
    Args:
        window (PsychoPy.Window object): A PsychoPy Window object
        monitor (PsychoPy.Monitor object): The current monitor being used
        gamma_grid (list, optional): The gamma information if it is not contained in the monitor. (gamma_rgb; b_rgb, k_rgb)
    """
    if not hasattr(window, '_DPShaderProg'):
        raise Warning("Shader not set up! make sure you call setUpShaderAndWindow before setting up gamma correction.")
        return
    
    from OpenGL.GL import glUseProgram, glUniform3f, glGetUniformLocation, glUniform1i
    glUseProgram(window._DPShaderProg)
    
    loc = glGetUniformLocation(window._DPShaderProg, "gamma_rgb")
    if loc == -1:
        raise Warning("The current shader is not the right shader, are you sure you are in M16 mode?")
        return
    
    if gamma_grid is None:
        gamma_grid = monitor.getGammaGrid()
        if gamma_grid is None:
            raise Warning("You did not provide gamma information and your monitor does not have any.")
            return
        gamma_rgb = [gamma_grid[1][2], gamma_grid[2][2], gamma_grid[3][2]] # gamma
        b_rgb = [gamma_grid[1][4], gamma_grid[2][4], gamma_grid[3][4]] # b
        k_rgb = [gamma_grid[1][5], gamma_grid[2][5], gamma_grid[3][5]] # k
    else:
        gamma_rgb = [gamma_grid[0][0], gamma_grid[0][1], gamma_grid[0][2]] # gamma
        b_rgb = [gamma_grid[1][0], gamma_grid[1][1], gamma_grid[1][2]] # b
        k_rgb = [gamma_grid[2][0], gamma_grid[2][1], gamma_grid[2][2]] # k
    
    glUniform3f(glGetUniformLocation(window._DPShaderProg, "b_rgb"), b_rgb[0], b_rgb[1] , b_rgb[2])
    glUniform3f(glGetUniformLocation(window._DPShaderProg, "k_rgb"), k_rgb[0], k_rgb[1] , k_rgb[2])
    glUniform3f(glGetUniformLocation(window._DPShaderProg, "gamma_rgb"), gamma_rgb[0], gamma_rgb[1] , gamma_rgb[2])
    glUniform1i(glGetUniformLocation(window._DPShaderProg, "gamma_correction_flag"), 1);

def disableGammaCorrection(window):
    """Disables M16 or C48 shader gamma correction"""
    from OpenGL.GL import glUseProgram, glUniform3f, glGetUniformLocation, glUniform1i
    if not hasattr(window, '_DPShaderProg'):
        raise Warning("Shader not set up! make sure you call setUpShaderAndWindow before setting up gamma correction.")
        return
    glUseProgram(window._DPShaderProg)
    glUniform1i(glGetUniformLocation(window._DPShaderProg, "gamma_correction_flag"), 0);
    
    
def enableGammaCorrection(window):
    """Enables M16 or C48 shader gamma correction"""
    from OpenGL.GL import glUseProgram, glUniform3f, glGetUniformLocation, glUniform1i
    if not hasattr(window, '_DPShaderProg'):
        raise Warning("Shader not set up! make sure you call setUpShaderAndWindow before setting up gamma correction.")
        return
    glUseProgram(window._DPShaderProg)
    glUniform1i(glGetUniformLocation(window._DPShaderProg, "gamma_correction_flag"), 1);
    


no_mode_Shader="""
/* 
 *
 *
 */
    uniform sampler2D fbo;
    void main() {
        vec4 fboFrag = texture2D(fbo, gl_TexCoord[0].st);
        gl_FragColor.rgb = fboFrag.rgb;
        gl_FragColor.r = gl_FragColor.r;
        gl_FragColor.g = gl_FragColor.g;
        gl_FragColor.b = gl_FragColor.b;
    }
"""

M16_mode_Shader="""
/* M16++ output formatter
 *
 * Converts from a 16bit framebuffer object into a 8bit per channel frame
 * for use in VPixx Device.
 *
 */
    uniform sampler2D fbo;
    uniform vec3 gamma_information; // (gamma, b, k)
    uniform int gamma_correction_flag;
    float index;
    float index_gamma_corrected;
    float k;
    float b;
    float gamma;

    void main() {
        vec4 fboFrag = texture2D(fbo, gl_TexCoord[0].st);
        gl_FragColor.rgb = fboFrag.rgb;
        if (gamma_correction_flag)
        {
            gamma = gamma_information.x;
            b = gamma_information.y;
            k = gamma_information.z;
            index_gamma_corrected = ( pow(( (1-gl_FragColor.r)*pow(b, gamma) + gl_FragColor.r*pow(b+k, gamma)), 1/gamma) - b ) / k;
            index = index_gamma_corrected * 65535.0 + 0.01;
        }
        else
        {
            index = gl_FragColor.r * 65535.0 + 0.01;
        }
        gl_FragColor.r = floor(index / 256.0) / 255.0;
        gl_FragColor.g = mod(index, 256.0) / 255.0;
        gl_FragColor.b = 0;
    }
"""
M16O_mode_Shader="""
/*
    M16 Mode with overlay. To use the overlay simply set the blue
    value to the index in the CLUT you want to use. Make sure that the
    red component is set to something different, otherwise, the index
    will be set to zero.
*/
    uniform sampler2D fbo;
    float index;

    void main() {
        vec4 fboFrag = texture2D(fbo, gl_TexCoord[0].st);
        gl_FragColor.rgb = fboFrag.rgb;
        index = gl_FragColor.r * 65535.0 + 0.01;
        if (gl_FragColor.b != gl_FragColor.r) // We have an overlay color
        {
            gl_FragColor.b = gl_FragColor.b;
            // Don't set other colors to zero in case of
            // Transparency color!
        }
        else
        {
            gl_FragColor.b = 0;
        }
        gl_FragColor.r = floor(index / 256.0) / 255.0;
        gl_FragColor.g = mod(index, 256.0) / 255.0; 
    }
"""

C48_mode_Shader="""
/* C48 output formatter
 *
 * Converts from a 16bit framebuffer object into a 8bit per channel frame
 * for use in C48 mode VPixx Device.
 *
 */
    #extension GL_ARB_texture_rectangle : enable
    uniform sampler2D fbo;
    uniform int gamma_correction_flag;
    uniform vec3 b_rgb;
    uniform vec3 k_rgb;
    uniform vec3 gamma_rgb;
    vec3 index_gamma_corrected;
    vec3 index;

    void main() {
        vec2 scrPos = gl_TexCoord[0].st;
        scrPos.s = (scrPos.s - floor(mod(scrPos.s, 2.0)));
        vec4 fboFrag = texture2D(fbo, scrPos);
        
        if (gamma_correction_flag)
        {
            index_gamma_corrected.r = ( pow(( (1-fboFrag.r)*pow(b_rgb.r, gamma_rgb.r) + fboFrag.r*pow(b_rgb.r+k_rgb.r, gamma_rgb.r)), 1/gamma_rgb.r) - b_rgb.r ) / k_rgb.r;
            index_gamma_corrected.g = ( pow(( (1-fboFrag.g)*pow(b_rgb.g, gamma_rgb.g) + fboFrag.g*pow(b_rgb.g+k_rgb.g, gamma_rgb.g)), 1/gamma_rgb.b) - b_rgb.g ) / k_rgb.g;
            index_gamma_corrected.b = ( pow(( (1-fboFrag.b)*pow(b_rgb.b, gamma_rgb.b) + fboFrag.b*pow(b_rgb.b+k_rgb.b, gamma_rgb.b)), 1/gamma_rgb.g) - b_rgb.b ) / k_rgb.b;
            //index_gamma_corrected = ( pow(( (1-fboFrag.rgb)*pow(b_rgb, gamma_rgb) + fboFrag.rgb*pow(b_rgb+k_rgb, gamma_rgb)), 1/gamma_rgb) - b_rgb ) / k_rgb;
            index = index_gamma_corrected * 65535.0 + 0.01;
        }
        else
        {
            index = fboFrag.rgb * 65535.0 + 0.01;
        }
        if (mod(gl_FragCoord.x, 2.0) < 1.0) {
            /* Even output pixel: high byte */
            gl_FragColor.rgb = floor(index / 256.0) / 255.0;
        }
        else {
            /* Odd output pixel: low byte */
            gl_FragColor.rgb = mod(index, 256.0) / 255.0;
        }
    }
"""
M16D_mode_Shader="""
/* M16++ output formatter
 *
 * Converts from a 16bit framebuffer object into a 8bit per channel frame
 * for use in VPixx Device.
 *
 * Red[7:3] takes the first 5 bits.
 * Green[7:3] takes the next 5 bits.
 * Blue[7:2] takes the last 6 bits.
 */

    uniform sampler2D fbo;
    float index;
    float index_gamma_corrected;
    float b,k,gamma;
    void main() {
        vec4 fboFrag = texture2D(fbo, gl_TexCoord[0].st);
        gl_FragColor.rgb = fboFrag.rgb;
        
        // GAMMA CORRECT!!!!
        b = 0.4502;
        k = 2.5970;
        gamma = 2.5272;
        //index_gamma_corrected = ( pow(( (1-gl_FragColor.r)*pow(b, gamma) + gl_FragColor.r*pow(b+k, gamma)), 1/gamma) - b ) / k;
        index = gl_FragColor.r * 65535.0 + 0.01;
        //index = index_gamma_corrected * 65535.0 + 0.01;
        gl_FragColor.r = floor(index / 2048.0) * 8.0 / 255.0;
        gl_FragColor.g = floor(mod(index, 2048.0) / 64.0) * 8.0 / 255.0;
        gl_FragColor.b = floor(mod(index, 64.0)) * 4.0 / 255.0;
    }
"""

L48D_mode_Shader="""
/*
 * Takes the Red value and send it such that it does not get dithered
 *
 *
 */
    uniform sampler2D fbo;
    float index;

    void main() {
        vec4 fboFrag = texture2D(fbo, gl_TexCoord[0].st);
        gl_FragColor.rgb = fboFrag.rgb;
        index = gl_FragColor.r * 65535.0 + 0.01;
        gl_FragColor.r = floor(index /  4096.0) * 16.0 / 255.0;
        gl_FragColor.g = mod(floor(index / 256.0), 16.0) * 16.0 / 255.0;
        gl_FragColor.b = 0;
    }
"""

C36D_mode_Shader="""
/* C36 output formatter
 *
 * Converts from a 16bit framebuffer object into a 8bit per channel frame
 * for use in C48 mode VPixx Device.
 *
 */
    #extension GL_ARB_texture_rectangle : enable
    uniform sampler2D fbo;
    vec3 index;

    void main() {
        vec2 scrPos = gl_TexCoord[0].st;
        scrPos.s = (scrPos.s - floor(mod(scrPos.s, 2.0)));
        vec4 fboFrag = texture2D(fbo, scrPos);

        index = fboFrag.rgb * 65535.0 + 0.01;

        if (mod(gl_FragCoord.x, 2.0) < 1.0) {
            /* Even output pixel: high byte */
            gl_FragColor.rgb = floor(index / 1024.0) * 4.0 / 255.0;
        }
        else {
            /* Odd output pixel: low byte */
            gl_FragColor.rgb = mod(floor(index / 16.0), 64.0) * 4.0 / 255.0;
        }
    }
"""
RB24_mode_Shader="""
/*
 * RB24, DVI RED[7:0] & GREEN[7:4] concatenate to form 12-bit RED value,
 * DVI BLUE[7:0] & GREEN[3:0] concatenate to form 12-bit BLUE value,
 * GREEN is forced to 0
 *
 *
 */
    uniform sampler2D fbo;
    float index_r, index_b;

    void main() {
        vec4 fboFrag = texture2D(fbo, gl_TexCoord[0].st);
        gl_FragColor.rgb = fboFrag.rgb;
        index_r = gl_FragColor.r * 65535.0 + 0.01;
        index_b = gl_FragColor.b * 65535.0 + 0.01;
        gl_FragColor.r = floor(index_r / 256.0) / 255.0;
        gl_FragColor.g = (mod(floor(index_r / 16.0), 16.0) * 16.0 + mod(floor(index_b / 16.0), 16.0)) / 255.0;
        gl_FragColor.b = floor(index_b / 256.0) / 255.0;
    }
"""