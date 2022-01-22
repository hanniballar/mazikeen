`mazikeen` is a test framework for command line applications.
`mazikeen` was created to facilitae testing of CLI application that have a predictable output. It facilitates testing on different operating systems by provideing a diff method that is agnostic to newline and make / remove directory. For `mazikeen` every test has it's own directory helping debugging and organizing tests.
|`mazikeen` empathise parralel testing.

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

Arguments
---------

.. code-block:: text

	mazikeen --help
	usage: mazikeen [-h] [-p PATTERN] [-f] [--upgradeScriptFile] [-s START] [-v] [-j [JOBS]]
					[-r REPORTFILE]
	
	Mazikeen test enviroment
	
	optional arguments:
	-h, --help            show this help message and exit
	-p PATTERN, --pattern PATTERN
							Only run tests which match pattern. Does support also
							negative patterns "-PATTERN"
	-f, --failfast        stop on first faild test as quickly as possible
	--upgradeScriptFile   save upgraded script file. Script files are upgraded if their version is lower that latest
                          version
	--scriptName NAME     Mazikeen script name (`script.yaml` default)
	-s DIR, --start-directory DIR
							Directory to start discovering tests ('.' default)
	-v, --verbose         Verbose output
	-j [JOBS], --jobs [JOBS]
							Specifies the number of jobs to run simultaneously
	-r REPORTFILE, --report REPORTFILE
							Create junit test report
							
script.yaml
-----------
For full documentation, please see https://github.com/hanniballar/mazikeen/blob/master/Documentation/script.yaml.rst.