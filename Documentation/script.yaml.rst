`script.yaml` is the script file mazikeen is looking after. Every directory that contains this file is considered a testcase.

Blocks
--------
`script.yaml` consists of blocks that are interpreted by mazikeen.
`script.yaml` should start with a version indicator. Afterwards it's considerted as inside a serial block

version
----------
Indicates the version of script.yaml.
For a summarized script.yaml change log please see: https://github.com/hanniballar/mazikeen/blob/master/Documentation/changelog_script.yaml.rst.



Example:

.. code-block:: yaml

version: 1.2.0

serial
----------
All block inside `steps` are executed one after the other.

It has following attributes:

steps
  List of block that will be executed. All block are being exectued one time for every entrie in the `entries` block. An entrie is replaced when the string `${entriename}` is encontered.

entries
  Entries for the `steps` block.
  Entries should be inside a `product` or `zip` block

- product::
  
    product:
      shape:
      - circle
      - square
    color:
      - red
      - yellow

  will result in::
  
    (shape: circle, color: red), (shape: circle, color: yellow), (shape: square, color: red), (shape: square, color: yellow)
- zip::
  
    product:
      shape:
      - circle
      - square
    color:
      - red
      - yellow

  will result in::
  
    (shape: circle, color: red), (shape: square, color: yellow)

failfast [ `True` | `False` ]
  Will exit the block if a step fails. Default `True`

serial block example:

.. code-block:: yaml

  ---
  version: 1.2.0
  entries:
    product:
      shape:
        - circle
        - square
        - triangle
      color:
        - red
        - yellow
  steps:
    - run:
        cmd: echo shape = ${shape}; color = ${color}
        outputfile: out.txt

parallel
----------
All blocks inside `steps` are executed in parallel. 
It's exacly the same as the serial block with the aditional attribute `max_workers`.

parallel block example:

.. code-block:: yaml

  ---
  version: 1.2.0
  steps:
    - rmdir: Output
    - makedirs: Output
    - parallel:
        entries:
          product:
            idx:
              - 1
              - 2
              - 3
              - 4
        max_workers: 4
        steps:
          - serial:
              steps:
                - run:
                    cmd: echo Parallel${idx}
                    outputfile: Output/parallel${idx}
                - diff: Output/parallel${idx} Expected/parallel${idx}

diff
----------
Will compare files and directories.

It has following attributes:

- paths [`leftpath` `rightpath`]
    left path and right path required for diff command
- binarycompare [ `True` | `False` ]
   Perform binary compare. Default `False`
- strategy [ `IgnoreLeftOrphans` | `IgnoreRightOrphans` | `IgnoreOrphans` | `All` ]
- ignorelines [`regex pattern`]
   Lines that match this patterns are ignored

diff block example:

.. code-block:: yaml

  ---
  version: 1.2.0
  steps:
    - diff: 
        paths: output/leftpath output/rightpath
        binarycompare: True
        strategy: IgnoreLeftOrphans
        ignorelines: 
          - 'Time:'

diff block short version:

.. code-block:: yaml

  ---
  version: 1.2.0
  steps:
    - diff: output/leftpath output/rightpath

run
----------
Will execute shell commands.
It has following attributes:

- cmd [`shell command`]
   Shell command that will be executed
- inputFile [`path`]
   The content of the `inputFile` will be sent to shell commands `stdin`
- outputFile [`path`]
   Shell commands stdout will the saved in outputFile
- exitcode [`exitcode`]
   Checks that shell commands exitcode matches this exitcode. If not defined or `null` exitcode will be ignored
- shell [`[cmd | sh | powershell]`]
   Execute command in selected shell

run block example:

.. code-block:: yaml

  ---
  steps:
    - run: 
        cmd: echo $shapes $color
        inputFile: input/inp.txt
        outputFile: output/out.txt
        exitCode: 0

run block short version:

.. code-block:: yaml

  ---
  steps:
    - run: echo $shapes $color

makedirs
----------
Created directories recursive

makedirs block example:

.. code-block:: yaml

  ---
  steps:
    - makedirs: Output/TestDir

rmdir
----------
Delete an entire directory tree

rmdir block example:

.. code-block:: yaml

  ---
  steps:
    - rmdir: Output/TestDir