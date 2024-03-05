#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 14:09:36 2024

@author: matthewdobre
"""

import numpy as np
import matplotlib.pyplot as plt 
import scipy.interpolate as interp
import csv
import statsmodels.api as sm 
import subprocess
import os
from scipy.signal import argrelextrema






def snm(file, T, tq1, tq2, tq_1, tq_2, outdir): 
    file = open(file, 'r')
    FILE = csv.reader(file)
    
    data = parse_monte_margins(FILE)
    info = data[0]
    num_it = data[1]

    t = info[0]
    q = info[1]
    q_ = info[2]
    
    
    snm_list = plot_and_calculate(t, q, q_, T, tq1, tq2, tq_1, tq_2, num_it, outdir)

    std_snm = np.std(snm_list)
    mean_snm = np.average(snm_list)
    min_snm = np.min(snm_list)
    max_snm = np.max(snm_list)
    

        #os.mkdir("simulation_results")
    

    fig, ax = plt.subplots()
    ax.hist(snm_list, bins=15)
    ax.set_xlabel("SNM")
    ax.set_title("Distribution of SNM Across Process Variations")
    plt.savefig("./{}/snm_histogram.png".format(outdir), bbox_inches='tight')

    fig1, ax1 = plt.subplots()
    ax1.plot(snm_list)
    ax1.set_xlabel("ith Iteration")
    ax1.set_title("SNM Over Iterations")
    plt.savefig("./{}/snm_iteration.png".format(outdir), bbox_inches='tight')

    z = (snm_list - mean_snm*np.ones(len(snm_list))) / std_snm
    sm.qqplot(z, line='45')
    plt.title("Quartile Quartile Plot")
    plt.savefig("./{}/qq_plot.png".format(outdir), bbox_inches='tight')


    data = open("./{}/snm_data.txt".format(outdir), "w")
    data.write("Relevant SNM Statistics \n")
    data.write(f"Mean SNM: {mean_snm} \n")
    data.write(f"Standard Deviation: {std_snm} \n")
    data.write(f"Min SNM: {min_snm} \n")
    data.write(f"Max SNM: {max_snm} \n")
    data.close()
    
    return snm_list


def parse_monte_margins(file):
    
    
    monte = 0
    data = []
    t = []
    q = []
    q_ = []
    
    for line in file: 
        line = line[0]
        
        if(line.find("TITLE") > 0): 
            continue
        
        if(line.find("time") > 0): # . does weird things
            monte+=1
            continue
        if(line.find(":") > 0): # this line will contain the different iterations
            print
            continue
            
        
            
        arr = line.split()
        t.append(float(arr[0]))
        q.append(float(arr[1]))
        q_.append(float(arr[2]))
        
        
        
        
    t = np.split(np.array(t), monte)
    q = np.split(np.array(q), monte)
    q_ = np.split(np.array(q_), monte)
    
    
    data.append(t)
    data.append(q)
    data.append(q_)
    
    
        
        
        
        
    return [data, monte]

    



def calculate_snm(q1, q2, q_1, q_2): 
    # perform rotations
    qrot1 = 1/np.sqrt(2)*(q1 - q_1)
    q_rot1 = 1/np.sqrt(2)*(q1 + q_1)
    
    qrot2 = 1/np.sqrt(2)*(q2 - q_2)
    q_rot2 = 1/np.sqrt(2)*(q2 + q_2)
    
    # take the difference between the two curves
    # snm smaller square that can fit in either lobe
    
    h = diff_between_func(qrot2, qrot1, q_rot2, q_rot1)
    #h= diff_between_func(q1, q2, q_1, q_2)
    #plt.plot(h)
        
    
    
    #plt.plot(qrot1, q_rot1)
    #plt.plot(qrot2, q_rot2)



     #checking meta stable point, for now assume its between the middle quartiles
    h = np.array(h)
    #  the relevant difference is the local minima
    local_minima_indices = argrelextrema(np.array(h), np.less)
    min_h = h[local_minima_indices]
    abs_min = np.min(min_h)
    
    if(abs_min > 1/len(h)):
        h_snm = abs_min
    else: 
        idx_min = local_minima_indices[np.argmin(min_h)]
        m = idx_min[0]
        h_max_1 = max(h[0:m])
        h_max_2 = max(h[m:])
        h_snm = min(h_max_1, h_max_2)
    

    #plt.plot(h[0:idx_intersect])
    
    snm = h_snm / np.sqrt(2)
    
    return snm



def diff_between_func(x1, x2, y1, y2):
    # set x and y as a key value pair, sort in order of x
    # then take differences of the x values that are the same 

    
    # finding the largest subsets that are containable within the list
    x_min = max(min(x1), min(x2))
    x_max = min(max(x1), max(x2))


    
    # Create an interpolation function based on arr2
    interp_func2 = interp.interp1d(x2, y2, fill_value="extrapolate")
    interp_func1 = interp.interp1d(x1, y1, fill_value="extrapolate")


    # Generate new x values for interpolation (same length as arr1)
    
    new_x = np.linspace(x_min, x_max, len(y2))

    # Interpolate arr2 to match arr1's shape
    interp_y2 = interp_func2(new_x)
    interp_y1 = interp_func1(new_x)
    
    

    x_ = [x for x in new_x if x >= x_min and x <= x_max]
    y_1 = [interp_y1[i] for i in range(len(interp_y1)) if new_x[i] >= x_min and new_x[i] <= x_max]
    y_2 = [interp_y2[i] for i in range(len(interp_y2)) if new_x[i] >= x_min and new_x[i] <= x_max]
    
    #plt.plot(x_, y_1)
    #plt.plot(x_, y_2)
       



    h = abs(np.array(y_1)-np.array(y_2))




    return h

def plot_and_calculate(t, q, q_, T, tq1, tq2, tq_1, tq_2, num_it, outdir): 
    
    snm_list = []
    for i in range(num_it):
        
        t_ = t[i]
        q1 = q[i]
        q_1 = q_[i]
        num_points = len(t_)
        sub = num_points//T
        
        
            
            
        #assume equal subdivisions: 
                
        # q varying, q_ response value
        qsweep = q1[tq1*sub:tq2*sub]
        qout = q_1[tq1*sub:tq2*sub]
            
        # q_varying, q response
        q_sweep = q_1[tq_1*sub:tq_2*sub]
        q_out = q1[tq_1*sub:tq_2*sub]

        
        snm = calculate_snm(qsweep, q_out, qout, q_sweep)
        snm_list.append(snm)

        
        #print(min(q_sweep), max(q_sweep))
        if not os.path.isdir(outdir): 

            subprocess.call("mkdir {}".format(outdir), shell=True)
        plt.plot(q_out, q_sweep, color = "skyblue")
        plt.plot(qsweep, qout, color = "blue")
        plt.title("Butterfly Curves Over Process Variations")
        plt.xlabel("V(Q)")
        plt.ylabel("V(Q_)")
        plt.savefig("./{}/butterfly_plot.png".format(outdir), bbox_inches='tight')
        
    return snm_list








        
        





