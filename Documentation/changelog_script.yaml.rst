
For a complete changelog, see:

* https://github.com/hanniballar/mazikeen/commits

1.2.0
-----
* Diff block attribute `ignoreLine` changed to `ignore`
* Run block attribute 'exitcode' no longer accepts value `None`. It is now written `null` as this is the standart
* Run block now suppors attribute `shell`. It allwos to run a command in a selected shell. Supported shells are: `cmd`, `sh` and `powershell`

1.1.0
-----
* Diff block replaced attributes `leftpath` and `rightpath` with paths
* Run block `exitCode` accepts value `None`

1.0.0
-----
* Initial release.
