#  Python Module for import                           Date : 2015-10-05
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  randquantum.py : true random numbers using quantum mechanics. 
                      Repository : https://github.com/rsvp/randomsys

     [For simple USAGE examples, skip to the conclusion at the end.]

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

If the server is somehow inaccessible, this module is written to fallback 
on pseudo simulation of the authentic process (with warnings emitted).


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
2015-10-05  Introduce NINERS variable for float representation.
               Fix in-place .remove() bug in randpick by copy operation.
2015-10-03  Change real() from [0, 1.0] to [0, 1.0) for compatibility.
               Rewrite gaussquantum to use generators.
               Use Python random.randrange as offline fallback.
2015-10-02  Rename intquantum to b16quantum as a precaution.
               Add randint to supplement b16quantum.
               Rename a generator to nine. 
               Rewrite seed to use efficient generator.
               Add randpick and permute [shuffle] for arbitrarily long list.
2015-09-30  Add generator functionality for sipping stream indefinitely.
2015-09-29  First version. 
'''

import urllib2
from math   import log

from random import randrange as pseudorange  #  Only for offline fallback.
from sys    import stderr                    #  Used to warn of fallback.


NINERS = 0.99999999999
#        ^reasonable system-dependent float representation of (1 - epsilon).
#         More nines could set it exactly to 1, resulting in rare errors. 


def warn( message ):
    '''Send warning message via stderr.'''
    #  Portable for both Python 2 and 3.
    stderr.write( ' :!  Warning: ' + message + '\n')


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
    #  print "DEBUG: retrieved json line from server."
    json = page.read()
    #  For length=3, json looks like:
    #      {"type":"uint16","length":3,"data":[7731,40732,1971],"success":true} 
    #  but we ignore the json module, and use brute force:
    json_after = json.split('[')[1]
    strlist = json_after.split(']')[0].split(',')
    #  Above read as string, so of course, convert to integer for our list:
    return [ int(s) for s in strlist ]


def randquantum_authentic( length=1000 ):
    '''Quantum random integers between [0, 65535] inclusive in a list.
    The data is online thus the performance is I/O bound.
    ''' 
    #  length of 1024 will make exactly one call to server.
    #  We must possibly make multiple calls to overcome API length limitation.
    calls = int(( length / 1024.5 ) + 1 )
    biglist = []
    for i in range( calls ):
        biglist += getanu()
    return biglist[:length]


def randquantum_pseudo( length=1000 ): 
    '''Pseudo simulation of randquantum_authentic(), intended as fallback.
    Offline call to the standard Python package random.
    '''
    return [ pseudorange(0, 65536) for i in range(length) ]


def randquantum( length=1000, authentic=True ):
    '''Authentic PRIMARY DEPENDENCY with offline FALLBACK.
    ___ATTN___  "authentic" switch for developer's debugging only.
    '''
    if authentic:
        try:
            return randquantum_authentic( length )
        except:
            warn(    "randquantum_authentic FAIL: now, PSEUDO simulation." )
            return randquantum_pseudo( length )
    else:
        warn( "authentic=False for randquantum implies PSEUDO simulation." )
        return randquantum_pseudo( length )


def boolquantum( length=1000 ):
    '''Convert randquantum to a random list of zeros and ones.
    In Python, 0 is False, anything else True, hence this is boolean.
    '''
    return [ i % 2 for i in randquantum( length ) ]


def realquantum( length=1000, endpoint=1.0 ):
    '''Convert randquantum to random real numbers: [0, endpoint]
    Discrete resolution is 1.52590219e-05 for [0,1].
    '''
    multiplier = float( endpoint ) / 65535 
    return [ i * multiplier for i in randquantum( length ) ]


def b16quantum( length=1000, endinteger=9 ):
    '''Random integers: [0, endinteger] where endinteger < 65536.
    For larger endinterger, consult randint below.
    If your endinteger is 1, we recommend boolquantum() instead.
    '''
    endpoint = endinteger + NINERS
    return [ int(r) for r in realquantum( length, endpoint ) ]



# ======================================================= GENERATORS =========== 
#  Above has focused on lists, but in practice, 
#  generators are more natural within other scripts.
#  The user should not worry about extracting an element from a random list.
#  Also these generators will cache the unused portion of a list in memory, 
#  and stand-by for a yield statement thus conserving calls to the server.
#  The generators below will "fill-up" only when needed (so this means 
#  the quantity of data is not pre-set unlike the lists above).


def sipstream( func_quantum, argtuple=(1024,) ):
     '''Generalized generator for certain randquantum functions. 
     Consider a stream to be lists being downloaded.
     This generator yields an element of a list as it is needed
     iteratively. Usage example:
          import randquantum as rq
          sip = sipstream( rq.gaussquantum, (1024, 0, 1.0) )
          #     where the tuple serves as positional arguments.
          print next( sip )
          print next( sip )
          print next( sip )
     '''
     length = argtuple[0]
     stream = apply( func_quantum, argtuple )
     i = 0
     while True:
          yield stream[i]
          i += 1
          if i == length:
               i = 0
               #   And FRESHEN the stream!
               stream = apply( func_quantum, argtuple )


# _______________ READY-MADE GENERATORS and iterating functions:
#
#  N.B. -  "Functions containing a yield statement are compiled
#           specially as generators -- when called, they return
#           a generator OBJECT that supports the iterator object
#           interface [e.g. next() or .next()]."
#  "next()" is a Python built-in for iterators since v2.6.


sip_boolean = sipstream( boolquantum,  (1024,)        )
sip_trio    = sipstream( b16quantum,   (1024, 2)      )
sip_nine    = sipstream( b16quantum,   (1024, 9)      )
sip_hundred = sipstream( b16quantum,   (1024, 100)    )
sip_real    = sipstream( realquantum,  (1024, NINERS ))
sip_cent    = sipstream( realquantum,  (1024, 100.0)  )


def boolean():  return sip_boolean.next()
def trio():     return sip_trio.next() - 1
def nine():     return sip_nine.next()
def hundred():  return sip_hundred.next()
def real():     return sip_real.next()
def cent():     return sip_cent.next()



def seed( length=19 ):
    '''Create a single random integer within given length.'''
    #  seed() turns out to be VERY useful for random integers, and nine()
    #  as a generator greatly reduces the number of calls to the server.
    s = ''
    for i in range( length):
        s += str( nine() )       
    #  Python can represent any integer up to memory limits!
    return int( s )


def randint( endinteger ):
    '''Random integer: [0, endinteger]; endinteger may be arbitrarily large!
    '''
    ilen = len( str(endinteger) )
    guess = seed( ilen )
    while guess > endinteger:
        guess = seed( ilen )
    return guess


def randpick( listing, count=1, replace=True ):
    '''Randomly pick element(s) from a list.'''
    if replace==False  and  count > len(listing):
        raise IndexError('Please adjust count <= length of listing.')    
    it = listing[:] 
    #            ^need a copy, not reference, due to in-place .remove()
    picks = []
    for k in range( count ):
        size = len( it )
        lucky = randint( size-1 )
        picks.append(  it[lucky] )
        if not replace:
            it.remove( it[lucky] )
    return picks


def shuffle( listing ):
    '''Randomly shuffle an entire list: permutation.'''
    #  Even for small len(x), the total number of permutations of x is 
    #  larger than the period of most PSEUDO random number generators; 
    #  this implies that most permutations of a long sequence can 
    #  never be generated. But this is not true for randquantum_authentic;
    #  though if the listing is huge, this could take a long time to finish.
    #
    return randpick( listing, len(listing), replace=False )


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
    gauss = []
    while len(gauss) < length:
        u1 = real()
        u2 = 1 - real()
        z = NV_MAGICCONST*(u1-0.5)/u2
        #   z is the KEY ratio essentially between
        #     two random reals both from uniform distribution.
        #     It is also the multiplier to standard deviation.
        zz = z*z/4.0
        #  Possible rejection next...
        if zz <= -log(u2):
            gauss.append( mean + (z * sdev))
            #  Approx. acceptance rate: 73% for <= condition.
    return gauss[:length]


# _______________ READY-MADE GENERATOR for standard Gaussian distribution:

sip_gauss   = sipstream( gaussquantum, (1024, 0, 1.0) )
def gauss():    return sip_gauss.next()


#  Interesting discussion regarding generating Gaussian distribution: 
#  http://stackoverflow.com/questions/75677/converting-a-uniform-distribution-to-a-normal-distribution


'''
============================================================ CONCLUSION ====== 

USAGE of these generators is very simple, for example:

     import randquantum as rq
     x = rq.gauss()
     y = rq.gauss()

So x and y are independently drawn from a standard 
Gaussian distribution, i.e. the normal N(0,1), 
and of course, they will be uncorrelated.

Illustrating random 0 or 1:

     if rq.boolean():
          print "yes, it's true."
     else:
          print "nothingness."

Such generator based functions can be invoked anywhere 
in your program without worrying about exhausting 
its list of origin. Our generators are designed to 
refresh automatically, and iterate indefinitely 
without blowing up memory space.


FOUR UNUSUAL GENERATORS:
rq.trio()    yields one of three equally possible: -1, 0, 1.
rq.nine()    yields a single integer 0 through 9    inclusive.
rq.cent()    will be real-valued between [0, 100.0] inclusive.
rq.hundred() will be an integer between  [0, 100]   inclusive.

THREE TRADITIONAL GENERATORS:
rq.boolean() yields binary-valued: 0 or 1.
rq.real() is real-valued [0,1] where both endpoints are included.
rq.gauss() is drawn from the standard normal distribution N(0,1).


FAQ:     What is the hit on performance versus pseudo random?
Answer:  Just as fast, except those milliseconds when a tiny json file
         is downloading. This is where the speed of your internet
         connection matters. You could cache in the background.


FAQ:     Why do these generators not output continuous values?
Answer:  Well, these true random numbers originate from 
         the **quantum** world where fundamentally everything
         is discrete.

Enjoy!
'''


# _______________ ALTERNATE SOURCES of randomness
#
#  - Humboldt University, Berlin: http://qrng.physik.hu-berlin.de 
#       Uses photon arrival times. Site requires registration.
#
#  - http://www.random.org was cool, but now has turned commercial.
#       Uses atmospheric noise, so it's empirical rather than 
#       theoretical in nature.


# _______________ TESTING randomness
#
#  - Start at the NIST, U.S. National Institute for Standards and Technology,
#          Computer Security Division: http://csrc.nist.gov/groups/ST/toolkit/rng
#
#  - Check for UPDATES at https://git.io/randomsys



if __name__ == "__main__":
     print "\n ::  THIS IS A MODULE for import -- not for direct execution! \n"
     raw_input('Enter something to get out: ')
