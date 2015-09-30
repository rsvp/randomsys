#  Python Module for import                           Date : 2015-09-29
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  randquantum.py : true random numbers using quantum mechanics. 

Reliable and unbiased random numbers are needed for a range of applications
spanning from numerical modeling to cryptographic communications. While there
are algorithms that can generate pseudo random numbers, they can never be
perfectly random nor indeterministic.

ANU researchers are generating true random numbers from a physical quantum
source by splitting a beam of light into two beams and then measuring the
power in each beam.  Because light is quantised, the light intensity in each
beam fluctuates about the mean.  Those fluctuations, due ultimately to the
quantum vacuum, can be converted into a source of random numbers. 

In classical physics, a vacuum is considered as a space that is empty of
matter or photons. In quantum mechanics, however, that same space resembles a
sea of virtual particles appearing and disappearing all the time. This result
is due to the fact that the vacuum still possesses a zero-point energy.
Consequently, the electromagnetic field of the vacuum exhibits random
fluctuations in phase and amplitude at all frequencies. By measuring these
fluctuations, one can generate ultra-high bandwidth random numbers.

The raw output of a quantum random-number generator is usually tainted by
classical technical noise. The integrity of the device can be compromised if
this noise is tampered with or even controlled by some malicious party. To
safeguard against this, our method produces side-information-independent
randomness that is quantified by min-entropy conditioned on this classical
noise. It maximizes the conditional min entropy of the number sequence
generated from a given quantum-to-classical-noise ratio. The detected
photocurrent in the experiment has a real-time random-number generation rate
of 14 (Mbit/s)/MHz. The spectral response of the detection system shows the
potential to deliver more than 70 Gbit/s of random numbers.

The 2015 hardware is constantly generating random bits at a rate of 5.7
Gbits/s.  The rate at which the live bits are streamed is limited by the
bandwidth of the internet connection.  Every number is randomly generated in
real time and cannot be predicted beforehand. 

Most pseudo random numbers have a finite period. Good pseudo random number
generators (e.g. the Mersenne Twister) have humoungous periods. But
eventually, if we wait long enough, the sequence will repeat itself. All
pseudo generators are indeed deterministic.  In contrast, for our true random
number generator, even if two exactly identical generators were placed in
identical environments with identical initial conditions, the two streams of
number generated will still be totally uncorrelated.

In development, one can use pseudo random numbers for simulations (since their
performance is not I/O bound) -- but as a final double-check on the results, 
use random numbers which are truly random.


Statistical TEST RESULTS daily:  http://qrng.anu.edu.au/NIST.php

References:

- Real time demonstration of high bitrate quantum random number generation
  with coherent laser light T. Symul, S. M. Assad, and P. K. Lam:  
  Appl. Phys.  Lett. 98, 231103 (2011)

- Maximization of Extractable Randomness in a Quantum Random-Number Generator
  J. Y. Haw, S. M. Assad, A. M. Lance, N. H. Y. Ng, V. Sharma, P. K. Lam, and
  T. Symul: Phys. Rev. Applied 3, 054004 (2015)

- Australia National University, ANU:
  http://photonics.anu.edu.au/qoptics/Research/qrng.php

- General resources and papers on randomness, including statistical testing:
  http://qrng.anu.edu.au/Links.php#statistical_tests


CHANGE LOG  Latest version available at https://git.io/randomsys
2015-09-29  First version. 
'''

import urllib2
from math import log


def getanu( url='https://qrng.anu.edu.au/API/jsonI.php?length=1024&type=uint16' ):
    '''Download list of Quantum Random Numbers from Australia National University.
    See API doc: https://qrng.anu.edu.au/API/api-demo.php
    where "uint16" returns integers between 0-65535 INCLUSIVE of endpoints, 
    and maximum length permitted is 1024 (but multiple calls are permitted).

    Each time you download the "live stream" via the functions defined below,
    the server will deliver new and unique random numbers. Moreover, these
    pages are authenticated and encrypted for security.
    '''
    page = urllib2.urlopen( url, timeout=7 )
    json = page.read()
    #  For length=3, json looks like:
    #      {"type":"uint16","length":3,"data":[7731,40732,1971],"success":true} 
    #  but we ignore the json module, and use brute force:
    json_after = json.split('[')[1]
    strlist = json_after.split(']')[0].split(',')
    #  Above read as string, so of course, convert to integer for our list:
    return [ int(s) for s in strlist ]


def randquantum( length=1000 ):
    '''Quantum random integers between [0, 65535] inclusive in a list.
  
    Performance is improved overall if LENGTH is set to what your project
    needs in memory. The data is online thus the performance is I/O bound.
    ''' 
    #  We must possibly make multiple calls to overcome API length limitation.
    calls = int(( length / 1024 ) + 1 )
    #                    ^Python 3 division acceptable also.
    biglist = []
    for i in range( calls ):
        biglist += getanu()
    return biglist[:length]


def truequantum( length=1000 ):
    '''Convert randquantum to a random list of zeros and ones.
    In Python, 0 is False, anything else True.
    '''
    return [ i % 2 for i in randquantum( length ) ]


def realquantum( length=1000, endpoint=1.0 ):
    '''Convert randquantum to random real numbers: [0, endpoint]
    Discrete resolution is 1.52590219e-05 for [0,1].
    '''
    multiplier = float( endpoint ) / 65535 
    return [ i * multiplier for i in randquantum( length ) ]


def intquantum( length=1000, endinteger=9 ):
    '''Convert randquantum to random integers: [0, endinteger]
    Not recommended for endinteger > 65535, but see seed() below.
    If your endinteger is 1, we recommend truequantum() instead.
    '''
    endpoint = endinteger + 0.9999999999999999
    return [ int(r) for r in realquantum( length, endpoint ) ]


def seed( length=19 ):
    '''Create a single random integer of any length.'''
    digits = intquantum( length, endinteger=9 )
    strd = ''.join([ str(d) for d in digits ])    
    #   Python can represent any integer up to memory limits!
    return int( strd )


def gaussquantum( length=1000, mean=0, sdev=1.0 ):
    '''Transform random uniform to normal Gaussian distribution.

    Modified from Python random module, normalvariate function.
    Reference: Albert J. Kinderman and J.F. Monahan,
    "Computer generation of random variables using the ratio of 
    uniform deviates", ACM Trans Math Software 1977, v3:3:257-260.

    (Python's faster random.gauss() uses trig functions so we 
    guess that is the Box-Muller algorithm which we are avoiding
    since it appears to constrain abs(z) to under 7.)

    Ref: https://en.wikipedia.org/wiki/Normal_distribution
    see "Generating values" section.
    '''
    NV_MAGICCONST = 1.71552776992141
    #             = 4*exp(-0.5)/sqrt(2.0)
    safelength = int( length * 1.47 )
    #            Expecting about 32% rejection rate below.
    gauss = []
    while len(gauss) < length:
        unx = realquantum( safelength, endpoint=0.999999999 )
        uny = realquantum( safelength, endpoint=0.999999999 )
        for i in range( safelength ):
            u1 = unx[i]
            u2 = 1 - uny[i]
            z = NV_MAGICCONST*(u1-0.5)/u2
            #   z is the KEY ratio essentially between
            #     two random reals both from uniform distribution.
            #     It is also the multiplier to standard deviation.
            zz = z*z/4.0
            #  Possible rejection next...
            if zz <= -log(u2):
                gauss.append( mean + (z * sdev))
    return gauss[:length]


#  Interesting discussion regarding generating Gaussian distribution: 
#  http://stackoverflow.com/questions/75677/converting-a-uniform-distribution-to-a-normal-distribution



if __name__ == "__main__":
     print "\n ::  THIS IS A MODULE for import -- not for direct execution! \n"
     raw_input('Enter something to get out: ')
