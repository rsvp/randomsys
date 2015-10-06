# randomsys

[![Join the chat at https://gitter.im/rsvp/randomsys](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/rsvp/randomsys?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

We study the behavior of random systems algorithmically.

## Generating truly random numbers: randquantum

This notebook gives a DEMONSTRATION 
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

