## CHANGE LOG

###  2015-10-21  v1.15.1021

- Add rigorous statistical testing: quantum/dieharder-randquantum

Results show randquantum has *PASSED Marsaglia Diehard, NIST STS, 
and RGB Dieharder tests* by successfully simulating 32-bit 
unsigned integers.


###  2015-10-10  v1.15.1010

We induce independence by creating a hybrid between authentic
and pseudo. Since the sources are clearly independent, this method also
stochastically disrupts the deterministic periodicity of pseudo generation.
Also by incorporating pseudo, we fetch fewer times from the server, 
increasing speed.

- Add unittest quantum/test_randquantum.py


###  2015-10-06  v1.15.1006

- Add randquantum.py Python module in `quantum` directory.
- Add randquantum-demo.ipynb IPython notebook for demonstration.


###  2015-09-29  Birthday for randomsys! 

- Initialize at GitHub. Register https://git.io/randomsys 


