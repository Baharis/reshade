# reshade
Python 3.5+ utility to introduce SHADE restraints on crystallographic .res file

## Introduction
This little python script accepts a MoPro-style list of constrains named
`CONSTRAINS.txt` and introduces ADP constrains into a shelx-style `*.res` file.
Introduced atoms are fixed by placing a leading 1 before respective values
to prevent further refinement.

## Usage
In order to use the script you need Python version 3.5 or newer.
Download the file reshade.py and run it in a directory
containing both `*.res` and `CONSTRAINS.txt` files using

    python3 reshade.py

If the files are in different directory, you can supply them as
optional positional arguments. In this case the constrained `.res` file
will be created in the working directory from which the script was run.

    python3 reshade.py /path/to/sample.res /path/to/CONSTRAINS.txt

On UNIX system you can make `reshade` a global command by:
removing the `.py` extension from the file,
making it executable (`chmod +x reshade`),
and either adding said file to a directory within path (such as `/usr/bin/`)
or adding its directory to the $PATH variable
(`export PATH="/path/to/directory/:$PATH`). 

## Author

This script has been created by Daniel Tchoń and published under MIT license.
If you have any questions, feel free to contact me via e-mail or on ResearchGate. 
