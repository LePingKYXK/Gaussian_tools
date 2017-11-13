#!/usr/bin/env python3


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re, os, time


pathin = input("\nPlease Enter the Directory Contained Your File:\n")
inputf = input("\nPlease Enter the SCAN Result File: (*.log)\n")
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
                    print("The current line BEFORE BREAK is:\n{:}\n".format(line))
                    break
            print("The current line JUST BREAK is:\n{:}\n".format(line))

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
                    #fundamental.rename(columns={'Mode(Quanta)':'Fundamental'}, inplace=True)
                    print("fundamental\n{}\n".format(fundamental))
                    
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
                    #overtone.rename(columns={'Mode(Quanta)':'Overtones'}, inplace=True)
                    print("overtone\n{}\n".format(overtone))

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
                    #combination.rename(columns={'Mode(Quanta)':'Combinations'}, inplace=True)
                    print("Combination\n{}\n".format(combination))
                    
                elif line.startswith(" Grad"):
                    break
            #data = pd.concat([fundamental, overtone, combination])[fundamental.columns.tolist()]
            

    return data


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
    ax.set_xlabel('Frequency (cm$^{-1}$)', fontsize=18)
    ax.set_ylabel('Intensity (a.u.)', fontsize=18)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='best', fontsize=15)

    x = grouped.Date
    y = grouped.n_fra

    ax.plot(x, y, '-')
    fig.savefig(os.path.join(path, 'The_IR_spectum.png'), dpi=600)
    plt.show()


def plot_anharmonic(data):
    '''
    '''
    fig = plt.figure(figsize=(8, 6)) # Creates a new figure, size in unit of inch
    ax = fig.add_subplot(111) # add a subplot to the new figure, 111 means "1x1 grid, first subplot"
    fig.subplots_adjust(top=0.90, bottom=0.25 ,left=0.12, right=0.95) # adjust the placing of subplot, adjust top, bottom, left and right spacing  
    ax.set_title('The IR Spectrum', fontsize=18) 

    ax.tick_params(axis='x', labelsize=12, rotation=45)
    plt.setp(ax.xaxis.get_majorticklabels(), ha='right') # align the xtick to the right location, since rotate 45 move the xtick.
    ax.tick_params(axis='y', labelsize=12)
    ax.set_xlabel('Frequency (cm$^{-1}$)', fontsize=18)
    ax.set_ylabel('Intensity (a.u.)', fontsize=18)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='best', fontsize=15)

    x = grouped.Date
    y = grouped.n_fra

    ax.plot(x, y, '-')
    fig.savefig(os.path.join(path, 'The_IR_spectum.png'), dpi=600)
    plt.show()


def main(path, filename, method):
    ''' Workflow:
    (1) read the file line by line;
    (2) extract the frequency and the IR intensity as a table;
    (3) plot the IR spectrum.
    '''
    initial_time = time.time()
    inputfile = os.path.join(path, filename)
    IR_data = read_file(inputfile, method)
    print("\nThe table is\n{:}\n".format(IR_data))
    
    #fmt_time = "\nWork Complete! Used Time: {:.3f} Seconds."
    #print(fmt_time.format(time.time() - initial_time))
    #IR_data.plot(kind='bar')
    #plt.show()
    #plot_anharmonic(IR_data)


if __name__ == "__main__":
    main(pathin, inputf, method)
