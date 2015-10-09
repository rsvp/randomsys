#!/usr/bin/env python2
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263 
#                                                     Date : 2015-10-07
#
# _______________|  test_randquantum.py : statistical testing of module.
#
#           Usage:  Just run this unittest script to test, or run nose.
#
#    Dependencies:  unittest (standard Python module)
#                   numpy    (to compute stats)
#                   randquantum
#
'''
Statistical TEST RESULTS daily:  http://qrng.anu.edu.au/NIST.php
These are rigorous results from the source.

- If the problem is the online connection, stderr should warn:
  "randquantum_authentic FAIL: now, PSEUDO simulation."

- Here we use Pearson's chi-squared test as described in:
  https://en.wikipedia.org/wiki/Pearson's_chi-squared_test
  to test the most important uniform distribution.

- Gaussian parameters for gauss() are indirectly tested.

[ ] - TODO: test boolean() output for serial independence.

Failing of a statistical test does not necessarily imply a fatal 
software bug. Some statistical tests may occassionally fail 
due to the nature of randomness itself. Repeat testing several 
times for further assurance.


___ATTN___ Methods within a unittest class should be named beginning with
           "test" IF a test is intended. Such tests will not necessarily 
           be conducted in the order written.
An ERROR is a test with faulty construct. A FAIL is a failure of a test.
Unittest reference: http://docs.python.org/library/unittest.html


CHANGE LOG
2015-10-07  First version, v1.15.1006, https://git.io/randomsys
'''

import unittest
import numpy as np
import randquantum as rq


class Quantum( unittest.TestCase ):

     def setUp( self ):
          '''Executed before each test in this class.'''
          pass

     def tearDown( self ):
          '''Executed after each test.'''
          pass


     def test_randquantum_getanu_response( self ):
          '''Test server network response via randquantum.getanu().'''
          #  2015-10-08  httpstatus: "Recv failure: Connection reset by peer"
          try:
               dummy = rq.getanu()
          except:
               self.fail('randquantum.getanu() server FAIL: changed API?')


     def test_randquantum_nine_chisq( self ):
          '''Chi-square to test uniformity of randquantum.nine().'''
          N = 2040  # Total number of observations
          obs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          for i in range( N ):
              d = rq.nine()
              obs[d] += 1
          #  print obs 
          E = N / 10.0  # Expectation
          terms = [ ((x-E)**2) / float(E) for x in obs ]
          #  terms are squared deviation over expectation for each bin.
          #  print terms
          chisq = sum( terms )
          #  print chisq
          #
          #  Use upper-tail critical values from chi-square distribution table
          #  for 9 degress of freedom:      (FAIL, worst case first.)
          if chisq > 21.6660:
               self.fail('randquantum.nine() FAIL: chi-square at 99% significance.')
          if chisq > 16.9190:
               self.fail('randquantum.nine() FAIL: chi-square at 95% significance.')
          if chisq > 14.68:
               self.fail('randquantum.nine() WARNING: chi-square at 90% significance.')


     def test_randquantum_gauss_parameters( self ):
          '''Test Gaussian parameters of randquantum.gaussquantum().'''
          #  This test by logic also applies to gauss().
          N = 2040  # Total number of observations
          gauss_output = np.array( rq.gaussquantum( N, mean= 0, sdev=1.0))
          mu    = gauss_output.mean()
          sigma = gauss_output.std()
          #  print mu, sigma
          sqrtN = N ** 0.5
          #  Following tests assume we know the true mean and sdev.
          #  Well, of course, since we specified them by construction. 
          #                              FAIL, worst case first.
          if abs( mu )  >  (2.575 / sqrtN):
               self.fail('gaussquantum() FAIL: dubious mean at 99% significance.')
          if abs( mu )  >  (1.960 / sqrtN):
               self.fail('gaussquantum() FAIL: dubious mean at 95% significance.')
          if abs( sigma - 1 )  >  0.05:
               self.fail('gaussquantum() WARNING: sdev exceeded 5% tolerance.')
          if abs( mu )  >  (1.645 / sqrtN):
               self.fail('gaussquantum() WARNING: dubious mean at 90% significance.')


if __name__ == '__main__':
     unittest.main()


     #  There are other assertBlahs (esp. from v2.7) but this is useful:
     #  self.assertAlmostEqual(a, b), i.e. round(a-b, 7) == 0

