# Explanation

This directory contains a couple of useful scripts to simulate the difference between Infrastructure and Civilian Factories in Hearts of Iron 4.

## infra_csv_converter.py

This script provides you with a way to convert the output from infra.py into a csv, so that you can use it for the infra_plot.py.

## infra.py

This script can simulate the difference between Civilian Industry and Infrastructure - for a proper explanation, refer to my video on the matter.

In order to store the output in a file you should run this command:

> py .\infra.py >results/results.txt 2>results/stderr.txt

### Modes of this script:

When using the script, you should comment things out that you don't desire. For example, when you are only interested in calculating one instance, you should comment out/delete the "run_all_simulations()" function, and instead insert the simulate_build() function.

It does make sense to uncomment the print functions in this case to get a better understanding what happens in your specific instance, but it's not required.

### Known flaws of the script:

1. We simply calculate the IC. This script assumes you can use 30 factories to build 1 factory (it does account that infrastructure will only benefit 15 factories, however, the output of the factories is still combined, which means the higher we go, the quicker we get factories).

## infra_plot.py

Creates a plot for the values provided in a csv.

# How to run the script

1. Install Python.
2. Some scripts will require additional dependencies. If running the script fails, do the following:
   1. Install Pip.
   2. cd into this directory
   3. Run `pip install -r requirements.txt`

And then simply run the scripts via:

> py infra.py

or any of the other script names.

# Analyzing results

To compare results, you can use one of these commands on your results files, if you have a tool that can search via regex:

> Infra: 3->4, Con: ([^,]+), Econ: No Economy, CGF=0.2, Mils=0, Fac=10

The above command will search for all instances with ANY Construction modifiers, but the rest being set statically.

Similarly, you can apply this to any other search:

> Infra: ([^,]+), Con: ([^,]+), Econ: ([^,]+), CGF=([^,]+), Mils=([^,]+), Fac=([^,]+) => Days: ([^,]+), Infra Fac: ([^,]+)
