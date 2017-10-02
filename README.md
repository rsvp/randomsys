# randomsys

[![Join the chat at https://gitter.im/rsvp/randomsys](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/rsvp/randomsys?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

We study the behavior of random systems algorithmically.

## Generating truly random numbers: randquantum

[This notebook gives a DEMONSTRATION](https://github.com/rsvp/randomsys/blob/master/quantum/randquantum-demo.ipynb) 
of the useful functions which yield true random numbers produced live from an
experiment in quantum mechanics. They are contained in the `randquantum` Python
module under the `quantum` directory.

Reliable and unbiased random numbers are needed for a range of applications
from numerical modeling to cryptographic communications. While there are
algorithms that can generate pseudo random numbers, they can never be
perfectly random nor indeterministic. ANU researchers are generating true
random numbers from a physical quantum source by splitting a beam of light
into two beams and then measuring the power in each beam. Because light is
quantised, the light intensity in each beam fluctuates about the mean. Those
fluctuations, due ultimately to the quantum vacuum, can be converted into a
source of random numbers.

The rate at which the live bits are streamed is limited by the bandwidth of
your internet connection. Every number is randomly generated in real time and
cannot be predicted beforehand. Most pseudo-random numbers have a finite
period after which the sequence repeats. The output herein will not have such
periodicity.

We develop a faster stochastic hybrid method which integrates authentic and 
pseudo generators to induce independence and eliminate predictable periodicity. 
This has *PASSED Marsaglia Diehard, NIST STS, and RGB Dieharder tests.* 


## Visualization of digits

For each digit,
[plot/plot_digitangle.py](https://github.com/rsvp/randomsys/blob/master/plot/plot_digitangle.py)
pushes the turtle (an arrow) directionally at a specific angle for a fixed distance.
That push creates a plot where the colors are determined by the input digits.
Thus the script visualizes any sequence of digits.

If circular angles are mapped on a random sequence of digits we will see a
drunkard walk across the screen. Furthermore, if the sequence comes from a
"normal" number, we can expect recurrent behavior, i.e. the drunk turtle
will return to where it started its journey, though it may take a long time
to do so theoretically.

Here is a plot of the first 10,000 digits of pi using
[pi-digits.txt](https://github.com/rsvp/randomsys/blob/master/plot/pi-digits.txt):


![pi-digits.jpg](https://git.io/pi-digits.jpg)


---

Revision date : 2017-10-02

