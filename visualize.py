""" TODO: Put your header comment here """

import random
import math
from PIL import Image
import alsaaudio
import audioop
import time
import pygame


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


def gen_art(num_frames=50, max_volume=40000, complexity=7, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels

    red_function = bld_func(complexity, complexity+3)
    green_function = bld_func(complexity, complexity+3)
    blue_function = bld_func(complexity, complexity+3)


    # Create image and loop over all pixels
    for t in range(0, max_volume, max_volume/num_frames):
        print "Generating frame %d ... Please be patient." % t
        t_val = remap(t, 0, max_volume, -1.0, 1.0)

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

def roundint(val, max_volume, num_frames):
    """ Takes in current volume level, and given the max volume level
    and the total number of frames, returns the closest volume level 
    that corresponds to an existent frame"""

    return int((max_volume/num_frames) * round(float(val)/(max_volume/num_frames)))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    num_frames = 100
    max_volume = 30000

    bool_gen_art = raw_input("Do you need to generate new frames? Y or N: ")
    if bool_gen_art.upper() == "Y":
        gen_art(num_frames, max_volume)


    pygame.init()
    w = 800   
    h = 537
    size = (w,h)
    screen = pygame.display.set_mode(size)

    imgs = [pygame.image.load('frame-%d.jpg' % i) for i in range(num_frames)]
    # imgs = [pygame.transform.scale(img,(1440,1080)) for img in imgs]

    for img in imgs:
        screen.blit(img,(0,0))
        pygame.display.flip()


    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(160)
    time.sleep(.5)
            
    while True:
        l,data = inp.read()
        if l:
            # print roundint(audioop.rms(data,2), max_volume, num_frames)/(max_volume/num_frames)
            print 'frame%d.png' % ((roundint(audioop.rms(data,2), max_volume, num_frames))/(max_volume/num_frames))
            index = ((roundint(audioop.rms(data,2), max_volume, num_frames))/(max_volume/num_frames))
            if index > num_frames-1:
                index = num_frames-1
            screen.blit(imgs[index],(0,0))
            pygame.display.flip()