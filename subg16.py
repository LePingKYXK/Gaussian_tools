# -*- coding: utf-8 -*-
"""
Created on Sunday, May 9, 20:47, 2021
Modified on Thursday, Jan 13, 22:05, 2022
@author: Dr. Huan Wang
"""

import argparse as ap
import subprocess
from pathlib import Path



parser = ap.ArgumentParser(add_help=True,
                    formatter_class=ap.ArgumentDefaultsHelpFormatter,
                    description="""
                    Author:  Dr. Huan Wang, 
                    Email:   huan.wang@whut.edu.cn,
                    Version: v2,
                    Date:    Jan. 13, 2022""")
parser.add_argument("-q",
                    metavar="<queue>",
                    type=str,
                    help="queue",
                    default="v4",
                    )
parser.add_argument("-m",
                    metavar="<memory>",
                    type=str,
                    help="memory",
                    default="18",
                    )
parser.add_argument("-i",
                    metavar="<Gaussian_input_file>",
                    type=Path,
                    nargs="+",
                    help="input file name",
                    default=(Path.cwd() / "h2o.g16"),
                    )
args = parser.parse_args()


def checkinput(inp):
    warn = """\nInvalid Extension of Your Input File! 
            (.g16 or .gjf or .com) are acceptable.\n"""
    inputlist = [".g16", ".com", ".gjf"]
    if inp.suffix in inputlist:
        return inp
    else:
        raise SystemExit(warn)


def prepare_pbs(inp, q, m):
    """
    This function replaces the keywords in the PBS templet file and returns
    a new PBS file with the name of the submission job.

    Parameters
    ----------
    inp : string or Path
        The input file name.
    q   : string
        The quere will be used.
    m   : string    
        The memory will be used.

    Returns
    -------
    pbs_dst : Path / string
        The directory of PBS (file name).
    """
    pbs_src = Path("/public1/apps/gs/subg16_templet.pbs").expanduser()
    pbs_dst = Path.cwd() / ''.join(("subg16_", inp.stem, pbs_src.suffix))

    with open(pbs_dst, "w") as fw, open(pbs_src, "r") as fo:
        for line in fo:
            if line.startswith("#PBS -N"):
                fw.write(line.replace("INPUT", "_".join(("g16", inp.stem))))
                
            elif line.startswith("#PBS -l nodes"):
                if q == "v4":
                    fw.write(line.replace("NP", "44"))
                elif q == "v5":
                    fw.write(line.replace("NP", "40"))
                    
            elif line.startswith("#PBS -l mem="):
                if not m:
                    if q == "v4":
                        fw.write(line.replace("6", "25"))
                    elif q == "v5":
                        fw.write(line.replace("6", "18"))
                elif m:
                    fw.write(line.replace("6", m))
                    
            elif line.startswith(("#PBS -e", "#PBS -o")):
                fw.write(line.replace("INPUT", "_".join(("g16", inp.stem))))
                
            elif line.startswith("#PBS -q"):
                if q == "v4":
                    fw.write(line.replace("default", "v4"))
                elif q == "v5":
                    fw.write(line.replace("default", "v5"))
                    
            elif line.startswith("/public1/apps/gs"):
                line = line.replace("INPUT.g16", str(inp))
                line = line.replace("INPUT.out", "".join((inp.stem, ".out")))
                fw.write(line)
                
            else:
                fw.write(line)
    return pbs_dst


def main():
    """ work flow
    1) grab the input files and number of cores;
    2) check if input file with valid extension;
    3) copy the PBS file with the new name of input file;
    4) submit the new PBS;
    5) repeat the loop (1 to 3) until all *.inp jobs submitted.
    """

    q, m, inps = args.q, args.m, args.i
    
    fmt = "Queue: {:} \t Memory: {:}0000 MB\nInput File(s): {:}"
    print(fmt.format(q, m, inps))

    for inp in inps:
        checkinput(inp)
        pbs = prepare_pbs(inp, q, m)
        subprocess.run(["qsub", pbs])


if __name__ == "__main__":
    main()
