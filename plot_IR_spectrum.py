#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re, os, time


pathin = input("\nPlease Enter the Directory Contained Your File:\n")
inputf = input("\nPlease Enter the Result File: (*.log)\n")
method = input("\nPlease Enter the Method (e.g. harmonic or anharmonic):\n")


def read_file(filename, method):
    '''
    '''
    data = None
    frequency = []
    intensity = []
    fundamental = []
    overtone = []
    combination = []
    
    with open(filename, 'r') as fo:
        if method.lower() == "harmonic":
            for line in fo:
                if line.startswith(" Frequencies"):
                    val1 = line.strip().split()[2:]
                    frequency.append(val1)
                elif line.startswith(" IR Inten"):
                    val2 = line.strip().split()[3:]
                    intensity.append(val2)
                if line.startswith(" - Thermochemistry"):
                    break
            frequency = np.array(frequency, dtype=np.float).flatten()
            intensity = np.array(intensity, dtype=np.float).flatten()
            if frequency.shape == intensity.shape:
                data = pd.DataFrame(intensity,
                                    columns=['IR_Intensity'],
                                    index=frequency)
                data.index.name = 'Frequency'
                return data
            
        elif method.lower() == "anharmonic":
            anhar = r"(\s+|\n\s+)Anharmonic Infrared Spectroscopy"
            freqs = r"(\s+|\n\s+)[1-9]"
            for line in fo:
                if re.search(anhar, line):
                    break

            while fo:
                line = next(fo)
                if line.startswith(" Fundamental Bands"):
                    for i in range(2):
                        line = next(fo)
                    col = line.strip().split()[1:]
                    while line not in ['\n', '\r\n']:
                        line = next(fo)
                        if re.search(freqs, line):
                            fundamental.append(line.strip().split()[1:])
                    fundamental = pd.DataFrame(np.array(fundamental).reshape(-1,4),
                                               columns=col)
                    fundamental.replace('***************', np.nan, inplace=True)
                    fundamental.rename(columns={'E(anharm)':'Frequency',
                                                'I(anharm)':'IR_Intensity'},
                                       inplace=True)
                    #print("fundamental\n{}\n".format(fundamental))
                    
                elif line.startswith(" Overtones"):
                    for i in range(2):
                        line = next(fo)
                    col = line.strip().split()[1:]
                    while line not in ['\n', '\r\n']:
                        line = next(fo)
                        if re.search(freqs, line):
                            overtone.append(line.strip().split()[1:])
                    overtone = pd.DataFrame(np.array(overtone).reshape(-1,3),
                                            columns=col)
                    overtone.rename(columns={'E(anharm)':'Frequency',
                                             'I(anharm)':'IR_Intensity'},
                                    inplace=True)
                    #print("overtone\n{}\n".format(overtone))

                elif line.startswith(" Combination Bands"):
                    for i in range(2):
                        line = next(fo)
                    col = line.strip().split()[1:]
                    while line not in ['\n', '\r\n']:
                        line = next(fo)
                        if re.search(freqs, line):
                            combination.append(line.strip().split()[2:])
                    combination = pd.DataFrame(np.array(combination).reshape(-1,3),
                                               columns=col)
                    combination.rename(columns={'E(anharm)':'Frequency',
                                                'I(anharm)':'IR_Intensity'},
                                       inplace=True)
                    #print("Combination\n{}\n".format(combination))
                    
                elif line.startswith(" Grad"):
                    break
            #data = pd.concat([fundamental, overtone, combination])[fundamental.columns.tolist()]
            return fundamental, overtone, combination


def plot_harmonic(data):
    '''
    '''
    fig = plt.figure(figsize=(8, 6)) # Creates a new figure, size in unit of inch
    ax = fig.add_subplot(111) # add a subplot to the new figure, 111 means "1x1 grid, first subplot"
    fig.subplots_adjust(top=0.90, bottom=0.25 ,left=0.12, right=0.95) # adjust the placing of subplot, adjust top, bottom, left and right spacing  
    ax.set_title('The IR Spectrum', fontsize=18) 

    ax.tick_params(axis='x', labelsize=12, rotation=45)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='right') # align the xtick to the right location, since rotate 45 move the xtick.
    ax.tick_params(axis='y', labelsize=12)
    
    ax.set_xlim([0.0, 4000.0])
    ax.set_xlabel('Frequency (cm$^{-1}$)', fontsize=18)
    ax.set_ylabel('Intensity (a.u.)', fontsize=18)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='best', fontsize=15)

    #### dras the peak-points
    x_c = data.index.values.astype(np.float64)
    amp = data["IR_Intensity"].values.astype(np.float64)
    #ax.plot(x_c, amp, '.', color='b')

    #### draw the spectrum profile
    x = np.linspace(0, 4000, 40000)
    FWHM = 10.0
    const = FWHM ** 2 / (2 * math.log(4))
    for i, data in enumerate(x_c):
        y = amp[i] * np.exp(-0.5 * (np.square(x - data) / const))
        ax.plot(x, y, '-', color='k')
    #fig.savefig(os.path.join(path, 'The_IR_spectum.png'), dpi=600)
    plt.show()


def plot_anharmonic(fundamental, overtone, combination):
    '''
    '''
    fig = plt.figure(figsize=(8, 6)) # Creates a new figure, size in unit of inch
    ax = fig.add_subplot(111) # add a subplot to the new figure, 111 means "1x1 grid, first subplot"
    fig.subplots_adjust(top=0.90, bottom=0.25 ,left=0.12, right=0.95) # adjust the placing of subplot, adjust top, bottom, left and right spacing  
    ax.set_title('The Anharmonic IR Spectrum', fontsize=18) 

    ax.tick_params(axis='x', labelsize=12, rotation=45)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='right') # align the xtick to the right location, since rotate 45 move the xtick.
    ax.tick_params(axis='y', labelsize=12)
    
    ax.set_xlim([0.0, 4000.0])
    #ax.set_ylim([0.0, max()])
    ax.set_xlabel('Frequency (cm$^{-1}$)', fontsize=18)
    ax.set_ylabel('Intensity (a.u.)', fontsize=18)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='best', fontsize=15)
    
    fdm_x_c = fundamental["Frequency"].values.astype(np.float64)
    fdm_amp = fundamental["IR_Intensity"].values.astype(np.float64)
    ovt_x_c = overtone["Frequency"].values.astype(np.float64)
    ovt_amp = overtone["IR_Intensity"].values.astype(np.float64)
    cmb_x_c = combination["Frequency"].values.astype(np.float64)
    cmb_amp = combination["IR_Intensity"].values.astype(np.float64)

    #ax.plot(fdm_x_c, dfm_amp, '.', color='b')
    #ax.plot(ovt_x_c, vot_amp, 'o', color='g')
    #ax.plot(cmb_x_c, cmb_amp, '^', color='r')

    x = np.linspace(0, 4000, 40000)
    FWHM = 10.0
    const = FWHM ** 2 / (2 * math.log(4))
    for i, fdm_data in enumerate(fdm_x_c):
        fdm = fdm_amp[i] * np.exp(-0.5 * (np.square(x - fdm_data) / const))
        ax.plot(x, fdm, '-', color='b')

    for j, ovt_data in enumerate(ovt_x_c):
        ovt = ovt_amp[j] * np.exp(-0.5 * (np.square(x - ovt_data) / const))
        ax.plot(x, ovt, '-', color='g')

    for k, cmb_data in enumerate(cmb_x_c):
        cmb = cmb_amp[k] * np.exp(-0.5 * (np.square(x - cmb_data) / const))
        ax.plot(x, cmb, '-', color='r')
    #fig.savefig(os.path.join(path, 'The_IR_spectum.png'), dpi=600)
    plt.show()


def main(path, filename, method):
    ''' Workflow:
    (1) read the file line by line;
    (2) extract the frequency and the IR intensity as a table;
    (3) plot the (harmonic or anharmonic) IR spectrum.
    '''
    initial_time = time.time()
    inputfile = os.path.join(path, filename)
    IR_df = read_file(inputfile, method)

    if method.lower() == "harmonic":
        fmt = "\nThe table is:\n{:}\n"
        print(fmt.format(IR_df))
        fmt_time = "\nWork Complete! Used Time: {:.3f} Seconds."
        print(fmt_time.format(time.time() - initial_time))
        plot_harmonic(IR_df)
        
    elif method.lower() == "anharmonic":
        fmt = ''.join(("\nThe table is:\n", "{:}\n\n" * len(IR_df)))
        print(fmt.format(*IR_df))
        fmt_time = "\nWork Complete! Used Time: {:.3f} Seconds."
        print(fmt_time.format(time.time() - initial_time))
        plot_anharmonic(IR_df[0].dropna(),
                        IR_df[1].dropna(),
                        IR_df[2].dropna())
        
    return IR_df
    

if __name__ == "__main__":
    IR_df = main(pathin, inputf, method)
