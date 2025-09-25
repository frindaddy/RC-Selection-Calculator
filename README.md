# RC Constant Calculator

Calculator for determining the best resistor and capacitor combination to get a given RC time constant (Tau) using standard component values.

E192 decade table is used for 0.1%, 0.25%, and 0.5% tolerance resistors.
E96 decade table is used for 1% tolerance resistors.
E24 decade table is used for 2% and 5% tolerance resistors.
E12 decade table is used for 10% tolerance resistors.

E24 decade table is used to calculate most standard value capacitors, then the rest of them are tacked on in `buildCapacitorValueList()`

# Usage

Call `calculateRC.py` via the command line.

`calculateRC.py [-h] [-r {0.1,0.25,0.5,1,2,5,10}] [-n NUM_RESULTS] tau`

### Positional arguments:
`tau` Target RC time constant (e.g., 10ms, 0.5s)

### Options:
`-h, --help` show this help message and exit

`-r, --resistor-tolerance` {0.1,0.25,0.5,1,2,5,10} Resistor tolerance in percent (default: 1%)

`-n, --num-results` NUM_RESULTS Number of top results to display (default: 5)