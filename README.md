# RC Constant Calculator

Calculator for determining the best resistor and capacitor combination to get a given RC time constant (Tau) using standard component values.

E192 decade table is used for 0.1%, 0.25%, and 0.5% tolerance resistors.
E96 decade table is used for 1% tolerance resistors.
E24 decade table is used for 2% and 5% tolerance resistors.
E12 decade table is used for 10% tolerance resistors.

E24 decade table is used to calculate most standard 1% capacitors, then the rest of them are tacked on in `buildCapacitorValueList()`
