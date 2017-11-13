#!/usr/bin/env python3

import numpy as np
import os, re, time

path  = input("\nPlease Enter the Directory Contains the Output File:\n")
fname = input("\nPlease Enter the Output (*.log) File Name:\n")



def extract_energy(path, fname):
    with open(os.path.join(path, fname)) as fo:
        for line in fo:
            if line.startswith(" Zero-point correction="):
                ZPE = re.search(r'\d+\.\d+', line).group()
            if line.startswith(" Sum of electronic and zero-point Energies="):
                energy_with_ZPE = re.search(r'[+-]\d+\.\d+', line).group()
    return ZPE, energy_with_ZPE


if __name__ == "__main__":
    ZPE, energy_with_ZPE = extract_energy(path, fname)
    print("ZPE is: {:}".format(ZPE))
    print("E + ZPE is: {:}".format(energy_with_ZPE))
