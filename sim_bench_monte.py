import monte_carlo as monte
import argparse 
import subprocess
from os import path
import sys

# defining command line parser 

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--spiceFile1', type=str, metavar='', required=True, help="Spice File")
parser.add_argument('-T', '--T', type=int, metavar='', required=True, help="Total units of time for simulation, ex: 6ms => T = 6")
parser.add_argument('-tq0', '--tq0', type=int, metavar='', required=True, help="Ex: if Q starts sweep at 1ms, then tq0 = 1")
parser.add_argument('-tqf', '--tqf', type=int, metavar='', required=True, help="Ex: if Q ends sweep at 2ms, then tqf = 2")
parser.add_argument('-tq_0', '--tq_0', type=int, metavar='', required=True, help="Ex: if Q_ starts sweep at 4ms, then tq_0 = 4")
parser.add_argument('-tq_f', '--tq_f', type=int, metavar='', required=True, help="Ex: if Q_ ends sweep at 5ms, then tq_f = 5")
parser.add_argument('-o', '--outdir', type=str, metavar='', required=True, help="Directory to store results")
cli_args = parser.parse_args()


# checking arguments


if(path.isfile("{}.sp".format(cli_args.spiceFile1)) == True or path.isfile("{}.spice".format(cli_args.spiceFile1)) == True): 
    subprocess.call("finesim {}.sp".format(cli_args.spiceFile1), shell=True)
else:
    print("File Nonexistant")
    sys.exit()
    



#assume you have written data in form spiceFile.pd0 
if(path.isfile("{}.pt0".format(cli_args.spiceFile1)) == True):
    snm = monte.snm("{}.pt0".format(cli_args.spiceFile1), cli_args.T, cli_args.tq0, cli_args.tqf, cli_args.tq_0, cli_args.tq_f, cli_args.outdir)
    

