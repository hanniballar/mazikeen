
For a complete changelog, see:

* https://github.com/hanniballar/mazikeen/commits
1.1.3
-----
* mazikeen can now work also with script.yaml version 1.0.0
* new command line argument `--upgradeScriptFile`. It updgrades script file from 1.0.0 to 1.1.0
1.1.2
-----
* Empty `entries` attribute for `serial` or `parallel` no longer yields an error
* Windows shell commands like `echo` allowed
* Bugfix: SIGINIT (CTRL-C) will trigger failfast immediately

1.1.1
-----
* SIGBREAK will immediately stop execution
* Report file path is being created if it doesn't exist
* Bugfix: some tests cases where executed twice
* Empty script files no longer generate errors
* An error code is being return only if there was an error

1.1.0
-----
* Diff block replaced attributes `leftpath` and `rightpath` with paths. Script version 1.1.0 created
* Run block without defined, or None exitcode will ignore exit code.
* Add the name of every block as verbose output.
* All diff files are now treated as binary files. Binarycompare set to `false` will only ignore OS EOL characters.

1.0.2
-----
* Run block replaces variables for attributes 'outputfile' and 'inputfile'.

1.0.1
-----
* Run block didn't work properly on linux.
* Test case wasn't marked as failed if it failed because of diff block.
* added '--version' command line argument.

1.0.0
-----
* Initial release.
