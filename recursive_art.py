""" TODO: Put your header comment here """

import random
import math
from PIL import Image


def bld_func(min_d, max_d):
    """ Builds a random function of depth at least min_d and depth
        at most max_d (see assignment writeup for definition of depth
        in this context)

        min_d: the minimum depth of the random function
        max_d: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """

    opers = ['prod','avg','cos_pi','sin_pi','subtract','add']
    oper = random.choice(opers)

    depth = random.randint(min_d,max_d)

    if depth <= 1:
        return [random.choice(['x','y','t'])]
    elif oper == 'prod':
        return ['prod', bld_func(min_d-1,max_d-1), bld_func(min_d-1,max_d-1)]
    elif oper == 'avg':
        return ['avg', bld_func(min_d-1,max_d-1), bld_func(min_d-1,max_d-1)]
    elif oper == 'cos_pi':
        return ['cos_pi', bld_func(min_d-1,max_d-1)]
    elif oper == 'sin_pi':
        return ['sin_pi', bld_func(min_d-1,max_d-1)]
    elif oper == 'subtract':
        return ['subtract', bld_func(min_d-1,max_d-1), bld_func(min_d-1,max_d-1)]
    elif oper == 'add':
        return ['add', bld_func(min_d-1,max_d-1), bld_func(min_d-1,max_d-1)]


def eval_func(f, x, y, t):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> eval_func(["x"],-0.5,0.75,0)
        -0.5
        >>> eval_func(["y"],0.1,0.02,0)
        0.02
    """
    if f[0] == 'x':
        return x
    if f[0] == 'y':
        return y
    if f[0] == 't':
        return y-t
    if f[0] == 'prod':
        return eval_func(f[1],x,y,t)*eval_func(f[2],x,y,t)
    if f[0] == 'avg':
        return (eval_func(f[1],x,y,t)+eval_func(f[2],x,y,t))/2.0
    if f[0] == 'cos_pi':
        return math.cos(math.pi*eval_func(f[1],x,y,t))
    if f[0] == 'sin_pi':
        return math.sin(math.pi*eval_func(f[1],x,y,t))
    if f[0] == 'subtract':
        return eval_func(f[1],x,y,t)-eval_func(f[2],x,y,t)
    if f[0] == 'add':
        return eval_func(f[1],x,y,t)+eval_func(f[2],x,y,t)


def remap(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap(0.5, 0, 1, 0, 10)
        5.0
        >>> remap(5, 4, 6, 0, 2)
        1.0
        >>> remap(5, 4, 6, 1, 2)
        1.5
    """
    weight_end = float(val-input_interval_start)/(input_interval_end-input_interval_start)
    weight_start = float(input_interval_end-val)/(input_interval_end-input_interval_start)

    return (weight_end*output_interval_end)+(weight_start*output_interval_start) 


def c_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> c_map(-1.0)
        0
        >>> c_map(1.0)
        255
        >>> c_map(0.0)
        127
        >>> c_map(0.5)
        191
    """
    return int(remap(val, -1, 1, 0, 255))


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap(i, 0, x_size, -1, 1)
            y = remap(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def gen_art(complexity=7, num_frames=1, x_size=350, y_size=350):
    """ Generates computational art and save as an image file.
        **All args optional**

        complexity - base complexity (depth of recursion) for image creation
        num_frames - determines how many frames will be drawn
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!

    red_function = bld_func(complexity, complexity+2)
    green_function = bld_func(complexity, complexity+2)
    blue_function = bld_func(complexity, complexity+2)


    # Create image and loop over all pixels
    for t in range(0, num_frames+1):
        print "Generating frame %d ... Please be patient." % t
        t_val = (t-(num_frames/2.0))/(num_frames/2.0)

        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        for i in range(x_size):
            for j in range(y_size):
                x = remap(i, 0, x_size, -1, 1)
                y = remap(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        c_map(eval_func(red_function, x, y, t_val)),
                        c_map(eval_func(green_function, x, y, t_val)),
                        c_map(eval_func(blue_function, x, y, t_val))
                        )
    
        im.save('frame%d.png' % t)

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    complexity = input("Of what complexity do you desire your art to be? ")
    num_frames = input("How many frames do you desire? ")
    gen_art(complexity, num_frames)

    # Command to create movie from png in terminal:a
    # avconv -i "frame%d.png" -r 25 -c:v libx264 -crf 20  -pix_fmt yuv420p img.mov
