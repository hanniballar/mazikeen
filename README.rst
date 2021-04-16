`mazikeen` test framework is designed for Command Line Applications. It's main feature is that every test has it's own directory.
`mazikeen` empathise parralel testing.

The test structure looks like:
::

    Testsuit1
    ├── Testcase1
    │   └── script.yaml
    ├── . . .
    └──TestcaseN
        └── script.yaml
    Testsuit2
    ├── Testcase1
    │   └── script.yaml
    ├── ...
    └──TestcaseN
        └── script.yaml
		
An example of a simple test:

.. code-block:: yaml

    # content of script.yaml
  ---
  steps:
    - rmdir: Output
    - makedirs: Output
    - run: echo "Hello World" > Output/hello.txt
    - diff: Output/hello.txt Expected/hello.txt

To execute it::

    $ mazikeen
    [RUN       ] --- simple
    [    PASSED] --- simple
    ----------------------------------------------------------------
    Total test cases: 1 passed: 1 skipped: 0 error: 0 failed: 0
    ----------------------------------------------------------------
    process time: 0.02 execution time: 0.01

Features
--------

- Every test case is a directory. Making it very to debug a failing test as all relevant data is stored in one place.
- Parallel execution support. Testscases can be executed in parallel. A testcase can call multiple CLI applications in parallel.


Documentation
-------------

For full documentation, please see https://github.com/hanniballar/mazikeen/blob/master/Documentation/Mazikeen.rst .


Bugs/Requests
-------------

Please use the `GitHub issue tracker <https://github.com/hanniballar/mazikeen/issues>`_ to submit bugs or request features.

