#!/usr/bin/env python
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263 
#        python 2.7.13 under Linux Ubuntu 14.04.5     Date : 2017-10-03
#  [/] - Cross-platform code compatible with python2.7 and python3.
''' 
_______________|  plot_digitangle.py : Plot digits given their assigned angle.

     Definition:  A "digit" is a member of the set {0, 1, ..., 9}.

    Description:  For each digit, this script pushes the turtle (an arrow)
                  directionally at a specific angle for some distance given
                  in pixel units. That push creates a plot where the colors
                  (HEATMAP) are determined by the input digits.

                  Thus this script visualizes any sequence of digits.
                  If circular angles are mapped on a random sequence we 
                  will see a drunkard walk across the screen. 
                  Furthermore, if the sequence comes from a "normal" number, 
                  we can expect recurrent behavior, i.e. the drunk turtle 
                  will return to where it started its journey, though
                  it may take a long time to do so theoretically.

                  The source of digits can be a generator function 
                  (a random generator is furnished), or any text file 
                  (e.g. pi-digits.txt containing 10,000 digits of pi)
                  containing digits.

          Usage:  $ python plot_digitangle.py
                  ___ATTN___ Turtle may travel outside the screen boundary, 
                             esp. for long iterations. The remedy is to use 
                             large pixel values for WIDTH and HEIGHT.

   Dependencies:  turtle (Standard package for Python graphics, 
                          _tkinter module from python3-tk package)

     References:  Turtle documentation:
                  https://docs.python.org/3/library/turtle.html
                  and tutorial, https://git.io/turtle-tutorial

           Data:  pi digits: https://www.angio.net/pi/digits.html 
                  e  digits: https://apod.nasa.gov/htmltest/gifcity/e.1mil

CHANGE LOG  For latest changes, see https://github.com/rsvp/randomsys
2017-10-03  Add origin_circle() marking starting point and color compass.
2017-10-02  First version is a complete revision of:
               https://gist.github.com/cavedave/423d67a583ad10925aa6dc85ab7acab4
               using Python idioms and heatmap for colors.
               Any text file can be used as a source of digits.

Blog post with interesting images by @cavedave, David Curran:
http://liveatthewitchtrials.blogspot.ie/2017/09/random-walks-with-number-digits.html
'''

from __future__ import absolute_import, print_function, division
import turtle
import random

WIDTH = 0.95
HEIGHT = 0.95
#  Window: WIDTH and HEIGHT in integer-valued pixels, or fraction of screen.

DELAY_millisec = 200
SHOWFREQ = 1
#  Otherwise, use tracer in main() to speed-up output.

HEATMAP = ['gray', 'black', 'blue', 'purple', 'cyan', 
           'green', 'yellow', 'orange', 'brown', 'red']


# _______________ SET-UP WINDOW SCREEN and TURTLE

screen = turtle.Turtle()
turtle.clearscreen()
wn = turtle.Screen()  # Create graphics window.
wn.setup(width=WIDTH, height=HEIGHT, startx=None, starty=None)
#        startx and starty position the window, not the turtle.

wn.tracer( SHOWFREQ, delay=DELAY_millisec)
#          ^Use large number to minimize graphics computing time.
turtle.speed(0)   # No animation, else use DELAY_millisec via tracer.
turtle.pensize(2) # Controls line fatness.
turtle.penup()    # Means no drawing when moving.
turtle.goto(0, 0) # (0, 0) is center of the screen.
turtle.pendown()  # Means drawing when moving.
# turtle.hideturtle()
#  =>  TURTLE will be initially oriented towards the east on x-axis.


def push( angle, pixels=50 ):
    '''Push turtle in directional angle for distance in pixels.'''
    turtle.left( angle )
    turtle.forward( pixels )
    #  Regain original orientation:
    turtle.left( -angle )


def d2circle( digit, pixels=50 ):
    '''Digit yields circular angle for distance in pixels.'''
    angle = digit * 36
    push( angle, pixels )


def d2east( digit, pixels=50 ):
    '''Digit yields easterly directional angle for distance in pixels.'''
    #  This may require super large WIDTH for long iterations,
    #  but will produce an image resembling a time-series.
    angle = (digit-5) * 15
    push( angle, pixels )


def read_digits(filename):
    '''Generator function will yield only digits from given text file.'''
    #  More memory-efficient than list, and can handle any arbitrary
    #  text file with letters, spaces, punctuations, etc.
    with open(filename) as file:
        for line in file:
            for char in line:
                if char.isdigit():
                    yield int(char)


def get_randigit():
    '''Generator function to get a random digit.'''
    yield random.randint(0, 9)


def origin_circle( pixels=210 ):
    '''Mark starting point and provide color compass as legend.'''
    for digit in range(0, 10):
        angle = digit * 36
        turtle.left(angle)
        turtle.forward(pixels)
        turtle.pencolor('black')
        turtle.write(str(angle) + '° ' + HEATMAP[digit] + '=' + str(digit))
        turtle.pencolor(HEATMAP[digit])
        turtle.forward(-pixels)
        turtle.left(-angle)


def run_circle( genfun, pixels=5, iterations=43 ):
    '''Use d2circle to visualize drunkard walk.'''
    origin_circle()
    for i in range( iterations ):
        digit = next(genfun())
        turtle.pencolor(HEATMAP[digit])
        d2circle( digit, pixels )


def run_circle_read( filename, pixels=5 ):
    '''Use d2circle to visualize drunkard walk reading a file.'''
    origin_circle()
    for digit in read_digits(filename):
        turtle.pencolor(HEATMAP[digit])
        d2circle( digit, pixels )


def savework():
    '''Save work as Encapsulated Postscript eps format.'''
    #  Convert to image format using e.g. Gimp.
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file="tmp_turtle_plot.eps")
    turtle.bye()


def main(case='randigit', datafile=None, save=False):
    '''Healthy case values are: 'demo', 'randigit', 'pi', or 'read'.'''
    if case == 'demo':
        #  Demo uses CONSTANT variables to SLOW work in progress.
        random.seed(42)  # For reproducibility.
        run_circle(get_randigit, pixels=42, iterations=50)
    elif case == 'randigit':
        wn.tracer( 100, delay=1) # Reasonable speed-up.
        run_circle(get_randigit, pixels=4, iterations=10000)
    elif case == 'pi':
        wn.tracer( 100, delay=1) # Reasonable speed-up.
        run_circle_read('pi-digits.txt', pixels=4)
    elif case == 'read':
        wn.tracer( 100, delay=1) # Reasonable speed-up.
        run_circle_read(datafile, pixels=4)
    else:
        turtle.bye
        raise ValueError("Invalid case argument: review main().")

    if save:
        savework()
    else:
        turtle.exitonclick()


if __name__ == "__main__":
    main('randigit')


