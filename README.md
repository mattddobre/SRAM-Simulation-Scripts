The following scripts plot the read, write and hold margins of an sram bitcell after running a spice simulation. 
The simulation performed is a slow transient solution to calculate the DC operating point at various voltages. 
Voltage controlled resistors act as switches that allow each node to be swept in one simulation. An example simulation setup for the bitcell is given. 
The simulator used is finesim. The script uses the following libraries which should be installed: 
- matplotlib
- numpy
- scipy
- statsmodels

To run the script, use the following command:
python3 sim_bench_monte.py -s (spicefile) -T (total simulation time, no unit) -tq0 (start of sweep of node 1) -tqf (end of sweep of node 1) -tq_0 (start of sweep of node 2) -tq_f (end of sweep of node 2) -o output directory

Note, only integer values are supported. Also, field in the spice file directory should not contain the file extension. Only .sp or .spice extensions are supported 

The command would look like the following for the given example: 
python3 sim_bench_monte.py -s bitcell_sim -T 6 -tq0 1 -tqf 2 -tq_0 4 -tq_f 5 -o example_out

The output directory will contain a plot of the butterfly curves, a file containings the statistics of the simulation, a Q-Q plot and histogram to display non-gaussian characteristics, and a plot with the snm value at each iteration of the simulation. 

Tip: 
The spice file must include a .print V(Q1) V(Q2) statement, where Q1 and Q2 are the nodes that contain the stored value. 
It would be best to ommit the .option post so fsdb files are not generated for each monte carlo simulation. 
Set strobeperiod=.001 in the .tran statement. This will ensure that finesim plots enough datapoints to obtain an accurate simulation. 

Additionally, if you're using the skywater130 technology, the spice files must be modified to use the correct directives for monte carlo simulation, since by default they are commented out. The MC_SWITCH parameter enables this. Plese refer to https://www.youtube.com/watch?v=fGxs2TnDgrU for how to do this, and https://github.com/ThomasJagielski/ic_tools_install/tree/main/july-2023-scripts for the script. 






