#!/usr/local/bin/python3

import sys
import getopt
import math
import time

def timestamp(s):
  print (s + time.strftime("%Y/%m/%d %X"))
  
# ASCII FONTS from: http://patorjk.com/software/taag/
# Font = "Big"
def ProgramHeader():
  print ("###################################################################")
  print ("Wellington Fast Assessment of Reactions using Force Fields")
  print (" __          __  _ _ ______      _____      ______ ______ ")
  print (" \ \        / / | | |  ____/\   |  __ \    |  ____|  ____|")
  print ("  \ \  /\  / /__| | | |__ /  \  | |__) |___| |__  | |__   ")
  print ("   \ \/  \/ / _ \ | |  __/ /\ \ |  _  // _ \  __| |  __|  ")
  print ("    \  /\  /  __/ | | | / ____ \| | \ \  __/ |    | |     ")
  print ("     \/  \/ \___|_|_|_|/_/    \_\_|  \_\___|_|    |_|     ")
  print ("                                              Version 0.01")
  print ("      WellFAReFF Copyright (C) 2015 Matthias Lein         ")
  print ("    This program comes with ABSOLUTELY NO WARRANTY        ")
  print ("     This is free software, and you are welcome to        ")
  print ("       redistribute it under certain conditions.          ")
  timestamp('Program started at: ')
  print ("###################################################################\n")

def ProgramFooter():
  print ("\n###################################################################")
  print ("  _____                                                      _     ")
  print (" |  __ \                                                    | |    ")
  print (" | |__) | __ ___   __ _ _ __ __ _ _ __ ___     ___ _ __   __| |___ ")
  print (" |  ___/ '__/ _ \ / _` | '__/ _` | '_ ` _ \   / _ \ '_ \ / _` / __|")
  print (" | |   | | | (_) | (_| | | | (_| | | | | | | |  __/ | | | (_| \__ \ ")
  print (" |_|   |_|  \___/ \__, |_|  \__,_|_| |_| |_|  \___|_| |_|\__,_|___/")
  print ("                   __/ |                                           ")
  print ("                  |___/                                            ")
  timestamp('Program terminated at: ')
  print ("###################################################################")

def ProgramAbort():
  print ("\n###################################################################")
  print ("  _____                     _                _           _ ")
  print (" |  __ \                   | |              | |         | |")
  print (" | |__) |   _ _ __     __ _| |__   ___  _ __| |_ ___  __| |")
  print (" |  _  / | | | '_ \   / _` | '_ \ / _ \| '__| __/ _ \/ _` |")
  print (" | | \ \ |_| | | | | | (_| | |_) | (_) | |  | ||  __/ (_| |")
  print (" |_|  \_\__,_|_| |_|  \__,_|_.__/ \___/|_|   \__\___|\__,_|")
  timestamp('Program aborted at: ')
  print ("###################################################################")
  sys.exit()
  return

def ProgramWarning():
  print ("\n###################################################################")
  print (" __          __              _             ")
  print (" \ \        / /             (_)            ")
  print ("  \ \  /\  / /_ _ _ __ _ __  _ _ __   __ _ ")
  print ("   \ \/  \/ / _` | '__| '_ \| | '_ \ / _` |")
  print ("    \  /\  / (_| | |  | | | | | | | | (_| |")
  print ("     \/  \/ \__,_|_|  |_| |_|_|_| |_|\__, |")
  print ("                                      __/ |")
  print ("                                     |___/ ")
  timestamp('Warning time/date: ')
  print ("###################################################################")
  return

def ProgramError():
  print ("\n###################################################################")
  print ("  ______                     ")
  print (" |  ____|                    ")
  print (" | |__   _ __ _ __ ___  _ __ ")
  print (" |  __| | '__| '__/ _ \| '__|")
  print (" | |____| |  | | | (_) | |   ")
  print (" |______|_|  |_|  \___/|_|   ")
  timestamp('Error time/date: ')
  print ("###################################################################")
  return

# Check for numpy, exit immediately if not available
import imp
try:
    imp.find_module('numpy')
    foundnp = True
except ImportError:
    foundnp = False
if not foundnp:
    print("Numpy is required. Exiting")
    ProgramAbort()
import numpy

# Check for scipy, exit immediately if not available
import imp
try:
    imp.find_module('scipy')
    foundnp = True
except ImportError:
    foundnp = False
if not foundnp:
    print("SciPy is required. Exiting")
    ProgramAbort()
import scipy.optimize

def iofiles(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('./wellfareFF.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('./wellfareFF.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   if inputfile == '':
      inputfile="orca-ethane.log"
   return (inputfile)

#############################################################################################################
# This section is for the definition of *all* constants and conversion factors
#############################################################################################################

# Conversion of mass in atomic mass units (AMU) to
# atomic units (electron masses)
def AMU2au(amu):
  return amu*1822.88839

# Same in reverse
def au2AMU(au):
  return au/1822.88839

# Conversion of length in Angstroms to  to
# atomic units (Bohrs)
def Ang2Bohr(ang):
    return ang*1.889725989

# Same in reverse
def Bohr2Ang(bohr):
    return bohr/1.889725989

SymbolToNumber = {
"H" :1, "He" :2, "Li" :3, "Be" :4, "B" :5, "C" :6, "N" :7, "O" :8, "F" :9,
"Ne" :10, "Na" :11, "Mg" :12, "Al" :13, "Si" :14, "P" :15, "S"  :16, "Cl" :17,
"Ar" :18, "K"  :19, "Ca" :20, "Sc" :21, "Ti" :22, "V"  :23, "Cr" :24,
"Mn" :25, "Fe" :26, "Co" :27, "Ni" :28, "Cu" :29, "Zn" :30, "Ga" :31,
"Ge" :32, "As" :33, "Se" :34, "Br" :35, "Kr" :36, "Rb" :37, "Sr" :38,
"Y"  :39, "Zr" :40, "Nb" :41, "Mo" :42, "Tc" :43, "Ru" :44, "Rh" :45,
"Pd" :46, "Ag" :47, "Cd" :48, "In" :49, "Sn" :50, "Sb" :51, "Te" :52,
"I"  :53, "Xe" :54, "Cs" :55, "Ba" :56, "La" :57, "Ce" :58, "Pr" :59,
"Nd" :60, "Pm" :61, "Sm" :62, "Eu" :63, "Gd" :64, "Tb" :65, "Dy" :66,
"Ho" :67, "Er" :68, "Tm" :69, "Yb" :70, "Lu" :71, "Hf" :72, "Ta" :73,
"W"  :74, "Re" :75, "Os" :76, "Ir" :77, "Pt" :78, "Au" :79, "Hg" :80,
"Tl" :81, "Pb" :82, "Bi" :83, "Po" :84, "At" :85, "Rn" :86, "Fr" :87,
"Ra" :88, "Ac" :89, "Th" :90, "Pa" :91, "U"  :92, "Np" :93, "Pu" :94,
"Am" :95, "Cm" :96, "Bk" :97, "Cf" :98, "Es" :99, "Fm" :100, "Md" :101,
"No" :102, "Lr" :103, "Rf" :104, "Db" :105, "Sg" :106, "Bh" :107,
"Hs" :108, "Mt" :109, "Ds" :110, "Rg" :111, "Cn" :112, "Uut":113,
"Fl" :114, "Uup":115, "Lv" :116, "Uus":117, "Uuo":118}

# Invert the above: atomic numbers to atomic symbols
NumberToSymbol = {v: k for k, v in SymbolToNumber.items()}

SymbolToMass = {
"H" : 1.00794, "He": 4.002602, "Li": 6.941, "Be": 9.012182, "B": 10.811,
"C": 12.0107, "N": 14.0067, "O": 15.9994, "F": 18.9984032, "Ne": 20.1797,
"Na": 22.98976928, "Mg": 24.3050, "Al": 26.9815386, "Si": 28.0855,
"P": 30.973762, "S": 32.065, "Cl": 35.453, "Ar": 39.948, "K": 39.0983,
"Ca": 40.078, "Sc": 44.955912, "Ti": 47.867, "V": 50.9415, "Cr": 51.9961,
"Mn": 54.938045, "Fe": 55.845, "Co": 58.933195, "Ni": 58.6934, "Cu": 63.546,
"Zn": 65.38, "Ga": 69.723, "Ge": 72.64, "As": 74.92160, "Se": 78.96,
"Br": 79.904, "Kr": 83.798, "Rb": 85.4678, "Sr": 87.62, "Y": 88.90585,
"Zr": 91.224, "Nb": 92.90638, "Mo": 95.96, "Tc": 98.0, "Ru": 101.07,
"Rh": 102.90550, "Pd": 106.42, "Ag": 107.8682, "Cd": 112.411, "In": 114.818,
"Sn": 118.710, "Sb": 121.760, "Te": 127.60, "I": 126.90447, "Xe": 131.293,
"Cs": 132.9054519, "Ba": 137.327, "La": 138.90547, "Ce": 140.116,
"Pr": 140.90765, "Nd": 144.242, "Pm": 145.0, "Sm": 150.36, "Eu": 151.964,
"Gd": 157.25, "Tb": 158.92535, "Dy": 162.500, "Ho": 164.93032, "Er": 167.259,
"Tm": 168.93421, "Yb": 173.054, "Lu": 174.9668, "Hf": 178.49, "Ta": 180.94788,
"W": 183.84, "Re": 186.207, "Os": 190.23, "Ir": 192.217, "Pt": 195.084,
"Au": 196.966569, "Hg": 200.59, "Tl": 204.3833, "Pb": 207.2, "Bi": 208.98040,
"Po": 209.0, "At": 210.0, "Rn": 222.0, "Fr": 223.0, "Ra": 226.0, "Ac": 227.0,
"Th": 232.03806, "Pa": 231.03588, "U": 238.02891, "Np": 237.0, "Pu": 244.0,
"Am": 243.0, "Cm": 247.0, "Bk": 247.0, "Cf": 251.0, "Es": 252.0, "Fm": 257.0,
"Md": 258.0, "No": 259.0, "Lr": 262.0, "Rf": 267.0, "Db": 268.0, "Sg": 271.0,
"Bh": 272.0, "Hs": 270.0, "Mt": 276.0, "Ds": 281.0, "Rg": 280.0, "Cn": 285.0,
"Uut": 284.0, "Uuq": 289.0, "Uup": 288.0, "Uuh": 293.0, "Uuo": 294.0}

# Define dictionary to convert atomic symbols to covalent radii (in Angstrom)
SymbolToRadius = {
"H"  : 0.37, "He" : 0.32, "Li" : 1.34, "Be" : 0.90, "B"  : 0.82, "C"  : 0.77,
"N"  : 0.75, "O"  : 0.73, "F"  : 0.71, "Ne" : 0.69, "Na" : 1.54, "Mg" : 1.30,
"Al" : 1.18, "Si" : 1.11, "P"  : 1.06, "S"  : 1.02, "Cl" : 0.99, "Ar" : 0.97,
"K"  : 1.96, "Ca" : 1.74, "Sc" : 1.44, "Ti" : 1.36, "V"  : 1.25, "Cr" : 1.27,
"Mn" : 1.39, "Fe" : 1.25, "Co" : 1.26, "Ni" : 1.21, "Cu" : 1.38, "Zn" : 1.31,
"Ga" : 1.26, "Ge" : 1.22, "As" : 1.19, "Se" : 1.16, "Br" : 1.14, "Kr" : 1.10,
"Rb" : 2.11, "Sr" : 1.92, "Y"  : 1.62, "Zr" : 1.48, "Nb" : 1.37, "Mo" : 1.45,
"Tc" : 1.56, "Ru" : 1.26, "Rh" : 1.35, "Pd" : 1.31, "Ag" : 1.53, "Cd" : 1.48,
"In" : 1.44, "Sn" : 1.41, "Sb" : 1.38, "Te" : 1.35, "I"  : 1.33, "Xe" : 1.30,
"Cs" : 2.25, "Ba" : 1.98, "La" : 1.69, "Ce" : 1.70, "Pr" : 1.70, "Nd" : 1.70,
"Pm" : 1.70, "Sm" : 1.70, "Eu" : 1.70, "Gd" : 1.70, "Tb" : 1.70, "Dy" : 1.70,
"Ho" : 1.70, "Er" : 1.70, "Tm" : 1.70, "Yb" : 1.70, "Lu" : 1.60, "Hf" : 1.50,
"Ta" : 1.38, "W"  : 1.46, "Re" : 1.59, "Os" : 1.28, "Ir" : 1.37, "Pt" : 1.28,
"Au" : 1.44, "Hg" : 1.49, "Tl" : 1.48, "Pb" : 1.47, "Bi" : 1.46, "Po" : 1.50,
"At" : 1.50, "Rn" : 1.45, "Fr" : 1.50, "Ra" : 1.50, "Ac" : 1.50, "Th" : 1.50,
"Pa" : 1.50, "U"  : 1.50, "Np" : 1.50, "Pu" : 1.50, "Am" : 1.50, "Cm" : 1.50,
"Bk" : 1.50, "Cf" : 1.50, "Es" : 1.50, "Fm" : 1.50, "Md" : 1.50, "No" : 1.50,
"Lr" : 1.50, "Rf" : 1.50, "Db" : 1.50, "Sg" : 1.50, "Bh" : 1.50, "Hs" : 1.50,
"Mt" : 1.50, "Ds" : 1.50, "Rg" : 1.50, "Cn" : 1.50, "Uut" : 1.50,"Uuq" : 1.50,
"Uup" : 1.50, "Uuh" : 1.50, "Uus" : 1.50, "Uuo" : 1.50}

# Define dictionary to convert atomic symbols to (Pauling) electronegativity
SymbolToEN = {
"H"  : 2.20, "He" : 0.00, "Li" : 0.98, "Be" : 1.57, "B"  : 2.04, "C"  : 2.55,
"N"  : 3.04, "O"  : 3.44, "F"  : 3.98, "Ne" : 0.00, "Na" : 0.93, "Mg" : 1.31,
"Al" : 1.61, "Si" : 1.90, "P"  : 2.19, "S"  : 2.58, "Cl" : 3.16, "Ar" : 0.00,
"K"  : 0.82, "Ca" : 1.00, "Sc" : 1.36, "Ti" : 1.54, "V"  : 1.63, "Cr" : 1.66,
"Mn" : 1.55, "Fe" : 1.83, "Co" : 1.88, "Ni" : 1.91, "Cu" : 1.90, "Zn" : 1.65,
"Ga" : 1.81, "Ge" : 2.01, "As" : 2.18, "Se" : 2.55, "Br" : 2.96, "Kr" : 3.00,
"Rb" : 0.82, "Sr" : 0.95, "Y"  : 1.22, "Zr" : 1.33, "Nb" : 1.60, "Mo" : 2.16,
"Tc" : 1.90, "Ru" : 2.00, "Rh" : 2.28, "Pd" : 2.20, "Ag" : 1.93, "Cd" : 1.69,
"In" : 1.78, "Sn" : 1.96, "Sb" : 2.05, "Te" : 2.10, "I"  : 2.66, "Xe" : 2.60,
"Cs" : 0.79, "Ba" : 0.89, "La" : 1.10, "Ce" : 1.12, "Pr" : 1.13, "Nd" : 1.14,
"Pm" : 1.13, "Sm" : 1.17, "Eu" : 1.20, "Gd" : 1.20, "Tb" : 1.10, "Dy" : 1.22,
"Ho" : 1.23, "Er" : 1.24, "Tm" : 1.25, "Yb" : 1.10, "Lu" : 1.27, "Hf" : 1.30,
"Ta" : 1.50, "W"  : 2.36, "Re" : 1.90, "Os" : 2.20, "Ir" : 2.20, "Pt" : 2.28,
"Au" : 2.54, "Hg" : 2.00, "Tl" : 1.62, "Pb" : 1.87, "Bi" : 2.02, "Po" : 2.00,
"At" : 2.20, "Rn" : 2.20, "Fr" : 0.70, "Ra" : 0.90, "Ac" : 1.10, "Th" : 1.30,
"Pa" : 1.50, "U"  : 1.38, "Np" : 1.36, "Pu" : 1.28, "Am" : 1.13, "Cm" : 1.28,
"Bk" : 1.30, "Cf" : 1.30, "Es" : 1.30, "Fm" : 1.30, "Md" : 1.30, "No" : 1.30,
"Lr" : 1.30, "Rf" : 1.30, "Db" : 1.30, "Sg" : 1.30, "Bh" : 1.30, "Hs" : 1.30,
"Mt" : 1.30, "Ds" : 1.30, "Rg" : 1.30, "Cn" : 1.30, "Uut" : 1.30,"Uuq" : 1.30,
"Uup" : 1.30, "Uuh" : 1.30, "Uus" : 1.30, "Uuo" : 1.30}


# ---------------------------------------------------
# Define global empirical parameters for force field
# ---------------------------------------------------

# Define a dictionary for the element specific parameter k_a
k_a = {
 "H"  : 1.755, "He" : 1.755, "B"  : 2.287, "C"  : 2.463, "N"  : 2.559, "O"  : 2.579,
 "F"  : 2.465, "Ne" : 2.465, "Al" : 2.508, "Si" : 2.684, "P"  : 2.780, "S"  : 2.800,
 "Cl" : 2.686, "Li" : 2.20, "Na" : 2.20, "K"  : 2.20, "Rb" : 2.20, "Cs" : 2.20,
 "Fr" : 2.20, "Be" : 2.80, "Mg" : 2.80, "Ca" : 2.80, "Sr" : 2.80, "Ba" : 2.80,
 "Ra" : 2.80, "Ar" : 2.75, "Sc" : 2.95, "Ti" : 2.95, "V"  : 2.95, "Cr" : 2.95,
 "Mn" : 2.95, "Fe" : 2.95, "Co" : 2.95, "Ni" : 2.95, "Cu" : 2.95, "Zn" : 2.95,
 "Ga" : 2.95, "Ge" : 2.95, "As" : 2.95, "Se" : 2.95, "Br" : 2.95, "Kr" : 2.95,
 "Y"  : 3.15, "Zr" : 3.15, "Nb" : 3.15, "Mo" : 3.15, "Tc" : 3.15, "Ru" : 3.15,
 "Rh" : 3.15, "Pd" : 3.15, "Ag" : 3.15, "Cd" : 3.15, "In" : 3.15, "Sn" : 3.15,
 "Sb" : 3.15, "Te" : 3.15, "I"  : 3.15, "Xe" : 3.15, "La" : 3.80, "Ce" : 3.80,
 "Pr" : 3.80, "Nd" : 3.80, "Pm" : 3.80, "Sm" : 3.80, "Eu" : 3.80, "Gd" : 3.80,
 "Tb" : 3.80, "Dy" : 3.80, "Ho" : 3.80, "Er" : 3.80, "Tm" : 3.80, "Yb" : 3.80,
 "Lu" : 3.80, "Hf" : 3.80, "Ta" : 3.80, "W"  : 3.80, "Re" : 3.80, "Os" : 3.80,
 "Ir" : 3.80, "Pt" : 3.80, "Au" : 3.80, "Hg" : 3.80, "Tl" : 3.80, "Pb" : 3.80,
 "Bi" : 3.80, "Po" : 3.80, "At" : 3.80, "Rn" : 3.80}

# Define dictionary for the element specific parameter k_z
k_z = {
 "H"  : 3.00, "He" : 2.35, "Li" : 1.70, "Be" : 5.50, "B"  : 0.95, "C"  : 0.95,
 "N"  : 0.95, "O"  : 0.95, "F"  : 0.95, "Ne" : 0.95, "Na" : 2.50, "Mg" : 3.00,
 "Al" : 0.75, "Si" : 0.75, "P"  : 0.75, "S"  : 0.75, "Cl" : 0.75, "Ar" : 0.75,
 "K"  : 3.00, "Ca" : 3.00, "Sc" : 0.65, "Ti" : 0.65, "V"  : 0.65, "Cr" : 0.65,
 "Mn" : 0.65, "Fe" : 0.65, "Co" : 0.65, "Ni" : 0.65, "Cu" : 0.65, "Zn" : 0.65,
 "Ga" : 0.65, "Ge" : 0.65, "As" : 0.65, "Se" : 0.65, "Br" : 0.65, "Kr" : 0.65,
 "Rb" : 3.00, "Sr" : 3.00, "Cs" : 0.60, "Ba" : 0.60, "La" : 0.60, "Ce" : 0.60,
 "Pr" : 0.60, "Nd" : 0.60, "Pm" : 0.60, "Sm" : 0.60, "Eu" : 0.60, "Gd" : 0.60,
 "Tb" : 0.60, "Dy" : 0.60, "Ho" : 0.60, "Er" : 0.60, "Tm" : 0.60, "Yb" : 0.60,
 "Lu" : 0.60, "Hf" : 0.60, "Ta" : 0.60, "W"  : 0.60, "Re" : 0.60, "Os" : 0.60,
 "Ir" : 0.60, "Pt" : 0.60, "Au" : 0.60, "Hg" : 0.60, "Tl" : 0.60, "Pb" : 0.60,
 "Bi" : 0.60, "Po" : 0.60, "At" : 0.60, "Rn" : 0.60, "Fr" : 0.60, "Ra" : 0.60,
 "Ac" : 0.60, "Th" : 0.60, "Pa" : 0.60, "U"  : 0.60, "Np" : 0.60, "Pu" : 0.60,
 "Am" : 0.60, "Cm" : 0.60, "Bk" : 0.60, "Cf" : 0.60, "Es" : 0.60, "Fm" : 0.60,
 "Md" : 0.60, "No" : 0.60, "Lr" : 0.60, "Rf" : 0.60, "Db" : 0.60, "Sg" : 0.60,
 "Bh" : 0.60, "Hs" : 0.60, "Mt" : 0.60, "Ds" : 0.60, "Rg" : 0.60, "Cn" : 0.60,
 "Uut" : 0.60,"Uuq" : 0.60, "Uup": 0.60, "Uuh" : 0.60, "Uus" : 0.60, "Uuo" : 0.60}
# Note no values specified for row 5 elements outside s block - Grimme gives rows 1, 2, 3 and 4, then Z>54

# Define individual global parameters
k_EN = -0.164
k_a2 = 0.221
k_a13 = 2.81
k_b13 = 0.53
k_13r = 0.7
k_damping = 0.11
k_overlap = 0.5
a1 = 0.45
a2 = 4.0
s8 = 2.7
E_ES_14 = 0.85
E_disp_rep = 0.5
beta_rep = 16.5
k_q = 1.15

# Define dictionary for the element specific hydrogen bonding parameter
k_hbnd = {"N": 0.8,
           "O": 0.3,
           "F": 0.1,
           "P": 2.0,
           "S": 2.0,
           "Cl": 2.0,
           "Se": 2.0,
           "Br": 2.0}

# Define dictionary for the element specific parameter k_X
k_X = {"Cl": 0.3,
       "Br": 0.6,
       "I": 0.8,
       "At": 1.0}

# Define dictionaries for the hydrogen and halogen bonding parameters k_q1 and k_q2
k_q1 = {"hbond": 10,
        "xbond": -6.5}
k_q2 = {"hbond": 5,
        "xbond": 1}

#############################################################################################################
# Do *not* define constants or conversion factors below here
#############################################################################################################

# Test if the argument is (can be converted to)
# an integer number
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#############################################################################################################
# Potential Fuctions are to be defined below here
#############################################################################################################

def potMorse(r, r0, D, b):
    """
    Morse oscillator potential
    """
    
    u = D * (1 - math.exp(-b*(r-r0))) ** 2

    return u

def potHarmonic(a, a0, k):
    """"
    Harmonic potential (for stretches and bends)
    """
    
    u = 0.5 * k * (a-a0) ** 2
    
    return u

def potSimpleCosine(theta, theta0, k):
    """"
    Extremely simplified cosine potential for torsions
    """
    
    u = k * (1 + numpy.cos(math.radians(180)+theta-theta0))
    
    return u

def bond_exp(a, b):
    """
    Exponent a used in the Generalised Lennard-Jones potential for bond stretches
    """
    # Currently assuming that a and b are instances of the class Atom. If not, will need to modify slightly here or in the FFstretch class
    delta_EN = SymbolToEN[a.symbol] - SymbolToEN[b.symbol]
    bond_exp = (k_a[a.symbol] * k_a[b.symbol]) + (k_EN * (delta_EN ** 2))

    return bond_exp

def exp_1_3(a, b):
    """
    Exponent a used in the Generalised Lennard-Jones potential for 1,3-stretches
    """
    # Currently assuming a and b are instances of the class Atom
    exp_1_3 = k_a13 + (k_b13 * k_a[a.symbol] * k_a[b.symbol])
    # Special case: if both atoms are in a ring, then k_13r is added to exp_1_3. Detection of rings to be implemented later

    return exp_1_3

def potGLJ(r, r0, k_str, a):
    """"
    Generalised Lennard-Jones potential (for bond and 1,3 stretches)
    """
    # k_str to be set equal to force constant for /that/ bond as read from Hessian as an initial guess, fitting implemented later
    u = k_str * (1 + ((r0/r) ** a) - 2 * ((r0/r) ** (a/2)))

    return u

def DampingFunction(a, b, r):
    """
    Distance dependent damping function for atoms with symbols a and b, and separation r
    """
    r_cov = SymbolToRadius[a] + SymbolToRadius[b]
    # Covalent distance defined as sum of covalent radii for the two atoms - will need to check this is correct

    f_dmp = 1 / (1 + k_damping * ((r/r_cov) ** 4))

    return f_dmp

def potBendNearLinear(a, a0, k_bnd, f_dmp):
    """
    Bending potential for equilibrium angles close to linearity
    """

    u = k_bnd * f_dmp * ((a0 - a) ** 2)

    return u

def potAnyBend(a, a0, k_bnd, f_dmp):
    """
    Double minimum bending potential
    """

    u = k_bnd * f_dmp * ((math.cos(a0) - math.cos(a)) ** 2)

    return u

def ChiralityFunction(theta):
    """
    Function used in torsion potential to give correct mirror symmetry
    """

    f_chiral = 0.5 * (1 - math.erf(theta - math.pi))

    return f_chiral

def potTorsion(theta, theta0, f_dmp, k_tors):
    """
    Torsion potential
    """

    f_chiral = ChiralityFunction(theta)

    u = 0.0
    # Sort out where n comes from in the following sum, check if k_tors ** n or k_tors_n
    #for n in # Range to be determined:
    #    inner_sum = (f_chiral * (1 + math.cos(n * (theta - theta0) + math.pi))) + ((1 - f_chiral) * (1 + math.cos(n * (theta + theta0 - (2 * math.pi)) + math.pi)))
    #    u = u + ((k_tors ** n) * inner_sum)
    #u = u * f_dmp

    return u

def AngleDamping(theta):
    """
    Angle dependent damping function for hydrogen bonding interactions
    """

    f_dmp_a = (0.5 * (math.cos(theta)+1)) ** 6

    return f_dmp_a

def HBondDamping(a, b, r):
    """
    Distance dependent damping function for hydrogen bonding with donor/acceptor atoms having symbols a and b, separation r
    """
    r_cov = SymbolToRadius[a] + SymbolToRadius[b]
    # Covalent distance defined as sum of covalent radii for the two atoms - will need to check this is correct

    f_dmp_hbnd = 1 / (1 + k_damping * ((r/r_cov) ** 12))

    return f_dmp_hbnd

def AtomicHBondFactor(sym, chg):
    """
    Atomic factor c_hbnd for an atom with symbol sym and atomic charge chg, used in hydrogen bond interaction strength
    """

    c_hbnd = k_hbnd[sym] * (math.exp(-k_q1 * chg) / (math.exp(-k_q1 * chg) + k_q2))

    return c_hbnd

def HBondStrengthFactor(sym_a, chg_a, r_ah, sym_b, chg_b, r_bh):
    """
    Modifier for the strength of a hydrogen bonding interaction where donor/acceptor atoms a and b are at distances r_ah and r_bh from hydrogen
    """

    c_hbnd_a = AtomicHBondFactor(sym_a, chg_a)
    c_hbnd_b = AtomicHBondFactor(sym_b, chg_b)
    c_hbnd = (c_hbnd_a * (r_ah ** 2) + c_hbnd_b * (r_bh ** 2)) / (r_ah ** 2 + r_bh ** 2)

    return c_hbnd

#############################################################################################################
# Classes for Force Field Terms defined below
#############################################################################################################

>>>>>>> master
class FFStretch:
  """ A stretching potential"""
  
  def __init__(self, a, b, r0, typ, arg):
    """ (FFStretch, int, int, number, int, [number]) -> NoneType
    
    A stretch potential between atoms number a and b with equilibrium
    distance r0, of type typ with arguments [arg]
    """
    
    self.atom1 = molecule.atoms[a]
    self.atom2 = molecule.atoms[b]
    self.r0 = r0
    if typ == 1:
      self.typ = typ
      self.k = arg[0]
    elif typ == 2:
      self.D = arg[0]
      self.b = arg[1]
    elif typ == 3:
        self.exp_a = bond_exp(self.atom1,self.atom2)
    #check whether an Atom can be passed to a function this way
        self.k_str == arg[0]
    elif typ == 4:
        self.exp_a = exp_1_3(self.atom1,self.atom2)
        self.k_str = arg[0]
    else:
      self.typ = 1
      self.k = arg[0]

  
  def __str__(self):
    """ (FFStretch) -> str
    
    Return a string representation of the stretching potential in this format:
    
    (atom1, atom2, r0, type, arguments)
    
    """
    
    s = '({0}, {1}, {2}, {3}, '.format(self.atom1, self.atom2, self.r0, self.typ)
    r = ''

    if self.typ == 1:
      r = '{0})'.format(self.k)
    elif self.typ == 2:
      r = '{0}, {1})'.format(self.D, self.b)
    
    return s+r
  
  def __repr__(self):
    """ (FFStretch) -> str
    
    Return a string representation of the stretching potential in this format:
    
    (atom1, atom2, r0, type, arguments)
    
    """
    
    s = '({0}, {1}, {2}, {3}, '.format(self.atom1, self.atom2, self.r0, self.typ)
    r = ''

    if self.typ == 1:
      r = '{0})'.format(self.k)
    elif self.typ == 2:
      r = '{0}, {1})'.format(self.D, self.b)
    
    return s+r
  
  def energy(self, r):
    """ Returns the energy of this stretching potential at distance r"""
    
    energy = 0.0
    if self.typ == 1:
      energy = potHarmonic(r, self.r0, self.k)
    elif self.typ == 2:
      energy = potMorse(r, self.r0, D, b)
    elif self.typ == 3 or self.typ == 4:
        energy = potGLJ(r, self.r0, self.k_str, self.exp_a)
    return energy

class FFBend:
  """ A bending potential"""
  
  def __init__(self, a, b, c, a0, typ, arg):
    """ (FFStretch, int, int, int, number, int, [number]) -> NoneType
    
    A bending potential between atoms number a, b and c with equilibrium
    angle a0, of type typ with arguments [arg]
    """
    
    self.atom1 = a
    self.atom2 = b
    self.atom3 = c
    self.a0 = a0
    if typ == 1:
      self.typ = typ
      self.k = arg[0]
    elif typ == 2:
        self.typ = 2
        self.k_bnd = arg[0]
        r_12 = molecule.atmatmdist(self.atom1, self.atom2)
        r_23 = molecule.atmatmdist(self.atom2, self.atom3)
        f_dmp_12 = DampingFunction(molecule.atoms[self.atom1].symbol, molecule.atoms[self.atom2].symbol, r_12)
        f_dmp_23 = DampingFunction(molecule.atoms[self.atom2].symbol, molecule.atoms[self.atom3].symbol, r_23)
        self.f_dmp = f_dmp_12 * f_dmp_23
    else:
      self.typ = 1
      self.k = arg[0]
  
  def __str__(self):
    """ (FFStretch) -> str
    
    Return a string representation of the bending potential in this format:
    
    (atom1, atom2, atom3, a0, type, arguments)
    
    """
    
    s = '({0}, {1}, {2}, {3}, '.format(self.atom1, self.atom2, self.atom3, self.a0, self.typ)
    
    if self.typ == 1:
      r = '{0})'.format(self.k)
    
    return s+r
  
  def __repr__(self):
    """ (FFStretch) -> str
    
    Return a string representation of the bending potential in this format:
    
    (atom1, atom2, atom3, a0, type, arguments)
    
    """
    
    s = '({0}, {1}, {2}, {3}, '.format(self.atom1, self.atom2, self.atom3, self.a0, self.typ)
    
    if self.typ == 1:
      r = '{0})'.format(self.k)
    
    return s+r
  
  def energy(self, a):
    """ Returns the energy of this bending potential at angle a"""
    
    energy = 0.0
    if self.typ == 1:
      energy = potHarmonic(a, self.a0, self.k)
    elif self.typ == 2:
        if (math.pi - 0.01) <= self.a0 <= (math.pi + 0.01):
        # Tolerance used here is essentially a placeholder, may need changing in either direction
            energy = potBendNearLinear(a, self.a0, self.k_bnd, self.f_dmp)
        else:
            energy = potAnyBend(a, self.a0, self.k_bnd, self.f_dmp)
    
    return energy

class FFTorsion:
  """ A torsion potential"""
  
  def __init__(self, a, b, c, d, theta0, typ, arg):
    """ (FFTorsion, int, int, int, int, number, int, [number]) -> NoneType
    
    A torsion potential between atoms number a, b, c and d with equilibrium
    angle theta0, of type typ with arguments [arg]
    """
    
    self.atom1 = a
    self.atom2 = b
    self.atom3 = c
    self.atom4 = d
    self.theta0 = theta0
    if typ == 1:
      self.typ = typ
      self.k = arg[0]
    elif typ == 2:
        self.typ = typ
        r_12 = molecule.atmatmdist(self.atom1, self.atom2)
        r_23 = molecule.atmatmdist(self.atom2, self.atom3)
        r_34 = molecule.atmatmdist(self.atom3, self.atom4)
    # Calculation of damping functions needs atom symbols and distance - check that molecule.atoms[a].symbol does return the symbol of the atom at index a in the atoms list
        f_dmp_12 = DampingFunction(molecule.atoms[self.atom1].symbol, molecule.atoms[self.atom2].symbol, r_12)
        f_dmp_23 = DampingFunction(molecule.atoms[self.atom2].symbol, molecule.atoms[self.atom3].symbol, r_23)
        f_dmp_34 = DampingFunction(molecule.atoms[self.atom3].symbol, molecule.atoms[self.atom4].symbol, r_34)
        self.f_dmp = f_dmp_12 * f_dmp_23 * f_dmp_34
        self.k = arg[0]
    else:
      self.typ = 1
      self.k = arg[0]
  
  def __str__(self):
    """ (FFTorsion) -> str
    
    Return a string representation of the torsion potential in this format:
    
    (atom1, atom2, atom3, atom4, theta0, type, arguments)
    
    """
    
    s = '({0}, {1}, {2}, {3}, {4}, '.format(self.atom1, self.atom2, self.atom3, self.atom4, self.theta0, self.typ)
    
    if self.typ == 1:
      r = '{0})'.format(self.k)
    
    return s+r
  
  def __repr__(self):
    """ (FFTorsion) -> str
    
    Return a string representation of the torsion potential in this format:
    
    (atom1, atom2, atom3, atom4, theta0, type, arguments)
    
    """
    
    s = '({0}, {1}, {2}, {3}, {4}, '.format(self.atom1, self.atom2, self.atom3, self.atom4, self.theta0, self.typ)
    
    if self.typ == 1:
      r = '{0})'.format(self.k)
    
    return s+r
  
  def energy(self, theta):
    """ Returns the energy of this torsion potential at angle theta"""
    
    energy = 0.0
    if self.typ == 1:
      energy = potSimpleCosine(theta, self.theta0, self.k)
    elif typ == 2:
        energy = potTorsion(theta, self.theta0, self.f_dmp, self.k)
    # Will need two cases, one for non-rotatable bonds, the other for rotatable bonds.
    # Probably best to implement via types
    return energy

#############################################################################################################
# Atom class and class methods to be defined below
#############################################################################################################

class Atom:
  """ An atom with an atomic symbol and cartesian coordinates"""
  
  def __init__(self, sym, x, y, z):
    """ (Atom, int, str, number, number, number) -> NoneType
    
    Create an Atom with (string) symbol sym,
    and (float) cartesian coordinates (x, y, z).
    (int) charge charge and (float) mass mass are set
    automatically according to symbol.
    """
    
    self.symbol = sym
    self.charge = SymbolToNumber[sym]
    self.mass = SymbolToMass[sym]
    self.coord = [x, y, z]
  
  def __str__(self):
    """ (Atom) -> str
    
    Return a string representation of this Atom in this format:
    
      (SYMBOL, X, Y, Z)
    """
    
    return '({0}, {1}, {2}, {3})'.format(self.symbol, self.coord[0], self.coord[1], self.coord[2])
  
  def __repr__(self):
    """ (Atom) -> str
    
    Return a string representation of this Atom in this format:"
    
      Atom("SYMBOL", charge, mass, X, Y, Z)
    """
    
    return '("{0}", {1}, {2}, {3}, {4}, {5})'.format(self.symbol, self.charge, self.mass, self.coord[0], self.coord[1], self.coord[2])
  
  def x(self, x):
    """ (Atom) -> NoneType
    
    Set x coordinate to x
    """
    self.coord[0]=x
    
  def y(self, y):
    """ (Atom) -> NoneType
    
    Set y coordinate to y
    """
    self.coord[1]=y

  def z(self, z):
    """ (Atom) -> NoneType
    
    Set z coordinate to z
    """
    self.coord[2]=z

#############################################################################################################
# Molecule class and class methods to be defined below
#############################################################################################################

class Molecule:
  """A molecule with a name, charge and a list of atoms"""
  
  def __init__(self, name, charge):
    """ (Molecule, str, int) -> NoneType
    
    Create a Molecule named name with charge charge and no atoms
    (int) Multiplicity mult is automatically set to the lowest
    possible value (1 or 2) and the lists of bonds, angles and
    dihedrals are empty.
    """
    
    self.name = name
    self.charge = charge
    self.mult = 1
    self.atoms = []
    self.bonds = []
    self.angles = []
    self.dihedrals = []
    self.stretch = []
    self.str13 = []
    self.bend = []
    self.tors = []
    self.inv = []
    
  
  def addAtom(self, a):
    """ (Molecule, Atom) -> NoneType
    
    Add a to my list of Atoms.
    """
    
    self.atoms.append(a)
    nucchg = 0
    for i in self.atoms:
      nucchg = nucchg + i.charge
    if (nucchg - self.charge) % 2 != 0:
      self.mult = 2
    else:
      self.mult = 1
  
  def __str__(self):
    """ (Molecule) -> str
    
    Return a string representation of this Molecule in this format:
    (NAME, CHARGE, MULT, (ATOM1, ATOM2, ...))
    """
    
    res = ''
    for atom in self.atoms:
      res = res + str(atom) + ', '
    res = res[:-2]
    return '({0}, {1}, {2}, ({3}))'.format(self.name, self.charge, self.mult, res)
  
  def __repr__(self):
    """ (Molecule) -> str
    
    Return a string representation of this Molecule in this format:
    (NAME, CHARGE, MULT, (ATOM1, ATOM2, ...))
    """
    
    res = ''
    for atom in self.atoms:
      res = res + str(atom) + ', '
    res = res[:-2]
    return '({0}, {1}, {2}, ({3}))'.format(self.name, self.charge, self.mult, res)
  
  def mass(self):
    """ (Molecule) -> number
    
    Return the molar mass as sum of atomic masses
    """
    
    mass = 0.0
    for atom in self.atoms:
      mass = mass + atom.mass
      
    return mass
  
  def numatoms(self):
    """ (Molecule) -> int
    
    Return the number of atoms in the molecule
    """
    
    return int(len(self.atoms))
  
  def chatom(self, n, at):
    """ (Molecule) -> NoneType
    
    Change the nth atom of the Molecule
    """
    
    self.atoms[n]=at
  
  def movatom(self, n, x, y, z):
    """ (Molecule) -> NoneType
    
    Move the nth atom to position x, y, z
    """
    
    self.atoms[n].x(x)
    self.atoms[n].y(y)
    self.atoms[n].z(z)
  
  def atmmass(self, n, m):
    """ (Molecule) -> NoneType
    
    Change the mass of the nth atom to m
    """
    
    self.atoms[n].mass=m
  
  def atmatmdist(self, i,j):
    """ (Molecule) -> number
    
    Report the distance between atoms i and j
    """
    
    distance=(self.atoms[i].coord[0]-self.atoms[j].coord[0])*(self.atoms[i].coord[0]-self.atoms[j].coord[0])
    distance=distance+(self.atoms[i].coord[1]-self.atoms[j].coord[1])*(self.atoms[i].coord[1]-self.atoms[j].coord[1])
    distance=distance+(self.atoms[i].coord[2]-self.atoms[j].coord[2])*(self.atoms[i].coord[2]-self.atoms[j].coord[2])
    
    return math.sqrt(distance)

  def bondangle(self, i):
    """ (Molecule) -> number (in radians)

    Report the angle described by three atoms in the bonds list
    """
    
    # Calculate the distance between each pair of atoms
    angle = self.angles[i]
    d_bond_1 = self.atmatmdist(angle[0], angle[1])
    d_bond_2 = self.atmatmdist(angle[1], angle[2])
    d_non_bond = self.atmatmdist(angle[0], angle[2])

    # Use those distances and the cosine rule to calculate bond angle theta
    numerator = d_bond_1**2 + d_bond_2**2 - d_non_bond**2
    denominator = 2*d_bond_1*d_bond_2
    argument = numerator/denominator
    theta = numpy.arccos(argument)

    return theta

  def anybondangle(self, i, j, k):
    """ (Molecule) -> number (in radians)

    Report the angle described by three atoms i, j and k
    """

    # Calculate the distance between each pair of atoms
    d_bond_1 = self.atmatmdist(i, j)
    d_bond_2 = self.atmatmdist(j, k)
    d_non_bond = self.atmatmdist(i, k)

    # Use those distances and the cosine rule to calculate bond angle theta
    numerator = d_bond_1**2 + d_bond_2**2 - d_non_bond**2
    denominator = 2*d_bond_1*d_bond_2
    argument = numerator/denominator
    theta = numpy.arccos(argument)

    return theta

  def dihedralangle(self, i):
    """ (Molecule) -> number (in radians)

    Report the dihedral angle described by a set of four atoms in the dihedrals list
    """

    # Calculate the vectors lying along bonds, and their cross products
    dihedral = self.dihedrals[i]
    atom_e1 = self.atoms[dihedral[0]]
    atom_b1 = self.atoms[dihedral[1]]
    atom_b2 = self.atoms[dihedral[2]]
    atom_e2 = self.atoms[dihedral[3]]
    end_1 = [atom_e1.coord[i] - atom_b1.coord[i] for i in range(3)]
    bridge = [atom_b1.coord[i] - atom_b2.coord[i] for i in range(3)]
    end_2 = [atom_b2.coord[i] - atom_e2.coord[i] for i in range(3)]
    vnormal_1 = numpy.cross(end_1, bridge)
    vnormal_2 = numpy.cross(bridge, end_2)

    # Construct a set of orthogonal basis vectors to define a frame with vnormal_2 as the x axis
    vcross = numpy.cross(vnormal_2, bridge)
    norm_vn2 = numpy.linalg.norm(vnormal_2)
    norm_b = numpy.linalg.norm(bridge)
    norm_vc = numpy.linalg.norm(vcross)
    basis_vn2 = [vnormal_2[i]/norm_vn2 for i in range(3)]
    basis_b = [bridge[i]/norm_b for i in range(3)]
    basis_cv = [vcross[i]/norm_vc for i in range(3)]

    # Find the signed angle between vnormal_1 and vnormal_2 in the new frame
    vn1_coord_n2 = numpy.dot(vnormal_1, basis_vn2)
    vn1_coord_vc = numpy.dot(vnormal_1, basis_cv)
    psi = math.atan2(vn1_coord_vc, vn1_coord_n2)

    return psi

  def anydihedralangle(self, i, j, k, l):
    """ (Molecule) -> number (in radians)

    Report the dihedral angle described by a set of four atoms i, j, k and l
    """

    # Calculate the vectors lying along bonds, and their cross products
    atom_e1 = self.atoms[i]
    atom_b1 = self.atoms[j]
    atom_b2 = self.atoms[k]
    atom_e2 = self.atoms[l]
    end_1 = [atom_e1.coord[i] - atom_b1.coord[i] for i in range(3)]
    bridge = [atom_b1.coord[i] - atom_b2.coord[i] for i in range(3)]
    end_2 = [atom_b2.coord[i] - atom_e2.coord[i] for i in range(3)]
    vnormal_1 = numpy.cross(end_1, bridge)
    vnormal_2 = numpy.cross(bridge, end_2)

    # Construct a set of orthogonal basis vectors to define a frame with vnormal_2 as the x axis
    vcross = numpy.cross(vnormal_2, bridge)
    norm_vn2 = numpy.linalg.norm(vnormal_2)
    norm_b = numpy.linalg.norm(bridge)
    norm_vc = numpy.linalg.norm(vcross)
    basis_vn2 = [vnormal_2[i]/norm_vn2 for i in range(3)]
    basis_b = [bridge[i]/norm_b for i in range(3)]
    basis_cv = [vcross[i]/norm_vc for i in range(3)]

    # Find the signed angle between vnormal_1 and vnormal_2 in the new frame
    vn1_coord_n2 = numpy.dot(vnormal_1, basis_vn2)
    vn1_coord_vc = numpy.dot(vnormal_1, basis_cv)
    psi = math.atan2(vn1_coord_vc, vn1_coord_n2)

    return psi

  def orient(self):
    """ (Molecule) -> NoneType
    
    Translate centre of mass to coordinate origin and
    (re-)Orient the molecule along the principal axes of inertia.
    """
    
    # The molecular center of mass
    xValue = 0.0
    yValue = 0.0
    zValue = 0.0
    for i in self.atoms:
      xValue = xValue+(i.mass*i.coord[0])
      yValue = yValue+(i.mass*i.coord[1])
      zValue = zValue+(i.mass*i.coord[2])
    xValue = xValue/(self.mass())
    yValue = yValue/(self.mass())
    zValue = zValue/(self.mass())
    
    # Translate whole molecule into the center of mass reference frame
    for i in self.atoms:
      i.coord[0]=i.coord[0]-xValue
      i.coord[1]=i.coord[1]-yValue
      i.coord[2]=i.coord[2]-zValue
    
    # Build inertia tensor
    inertiaTensor = []
    Ixx = 0.0
    Ixy = 0.0
    Ixz = 0.0
    Iyx = 0.0
    Iyy = 0.0
    Iyz = 0.0
    Izx = 0.0
    Izy = 0.0
    Izz = 0.0
    for i in self.atoms:
      Ixx = Ixx + (i.mass*((Ang2Bohr(i.coord[1])*Ang2Bohr(i.coord[1]))+(Ang2Bohr(i.coord[2])*Ang2Bohr(i.coord[2]))))
      Ixy = Ixy - i.mass*Ang2Bohr(i.coord[0])*Ang2Bohr(i.coord[1])
      Ixz = Ixz - i.mass*Ang2Bohr(i.coord[0])*Ang2Bohr(i.coord[2])
      Iyx = Iyx - i.mass*Ang2Bohr(i.coord[1])*Ang2Bohr(i.coord[0])
      Iyy = Iyy + (i.mass*((Ang2Bohr(i.coord[0])*Ang2Bohr(i.coord[0]))+(Ang2Bohr(i.coord[2])*Ang2Bohr(i.coord[2]))))
      Iyz = Iyz - i.mass*Ang2Bohr(i.coord[1])*Ang2Bohr(i.coord[2])
      Izx = Izx - i.mass*Ang2Bohr(i.coord[2])*Ang2Bohr(i.coord[0])
      Izy = Izy - i.mass*Ang2Bohr(i.coord[2])*Ang2Bohr(i.coord[1])
      Izz = Izz + (i.mass*((Ang2Bohr(i.coord[0])*Ang2Bohr(i.coord[0]))+(Ang2Bohr(i.coord[1])*Ang2Bohr(i.coord[1]))))
    inertiaTensor.append([Ixx, Ixy, Ixz])
    inertiaTensor.append([Iyx, Iyy, Iyz])
    inertiaTensor.append([Izx, Izy, Izz])
    inertiaTensor = numpy.matrix(inertiaTensor)
    
    # Diagonalise inertia tensor
    inertiaMoments, inertialAxes = numpy.linalg.eig(inertiaTensor)
    
    # Orthogonalise eigenvectors (only sometimes necessary)...
    inertialAxes, r = numpy.linalg.qr(inertialAxes)
    
    # Sort moments from highest to lowest
    idx = inertiaMoments.argsort()[::-1]
    inertiaMoments = inertiaMoments[idx]
    inertialAxes = inertialAxes[:,idx]
    
    # Transform molecular coordinates into new frame of principal axes of inertia
    for i in self.atoms:
      vector = [i.coord[0],i.coord[1],i.coord[2]]
      vector = numpy.matrix(vector)
      vector = numpy.matrix.transpose(inertialAxes).dot(numpy.matrix.transpose(vector))
      vector = numpy.array(vector).flatten().tolist()
      i.coord[0] = vector[0]
      i.coord[1] = vector[1]
      i.coord[2] = vector[2]
  
  def addBond(self, a, b):
    """ (Molecule) -> NoneType
    
    Adds a bond between atoms a and b to the list of bonds
    """
    # Make sure a < b
    if a < b:
      c = a
      d = b
    else:
      c = b
      d = a
    
    # Check if the bond already exists
    exists = False
    for i in self.bonds:
      if i == [c, d]:
        exists = True
    
    # Append bond to list if doesn't exist and is plausible
    if exists == False and a >= 0 and b >= 0 and a <= len(self.atoms) and b <= len(self.atoms) and c != d:
      self.bonds.append([c, d])

  def addFFStretch(self, a, b, r0, typ, arg):
    """ (Molecule) -> NoneType

    Adds a stretching potential between atoms a and b to the list of stretches
    """
    # Make sure a < b
    if a < b:
      c = a
      d = b
    else:
      c = b
      d = a

    # Note: There's no check if the stretch already exists. Mainly because there's no reason not to have
    # two different functions adding energy to the same "stretch"

    # Append stretch to list if doesn't exist and is plausible
    if a >= 0 and b >= 0 and a <= len(self.atoms) and b <= len(self.atoms) and c != d:
      self.stretch.append(FFStretch(c, d, r0, typ, arg))

  def addFFStr13(self, a, b, r0, typ, arg):
    """ (Molecule) -> NoneType

    Adds a stretching potential between atoms a and b to the list of stretches
    """
    # Make sure a < b
    if a < b:
      c = a
      d = b
    else:
      c = b
      d = a

    # Note: There's no check if the stretch already exists. Mainly because there's no reason not to have
    # two different functions adding energy to the same "stretch"

    # Append stretch to list if doesn't exist and is plausible
    if a >= 0 and b >= 0 and a <= len(self.atoms) and b <= len(self.atoms) and c != d:
      self.str13.append(FFStretch(c, d, r0, typ, arg))

  def delBond(self, a, b):
    """ (Molecule) -> NoneType
    
    Deletes the bond between atoms a and b from the list of bonds
    """
    # Make sure a < b
    if a < b:
      c = a
      d = b
    else:
      c = b
      d = a
    
    # Check if the bond actually exists
    exists = False
    for i in self.bonds:
      if i == [c, d]:
        exists = True
    
    # Remove if it does
    if exists == True:
      self.bonds.remove([c, d])
  
  def addAngle(self, a, b, c):
    """ (Molecule) -> NoneType
    
    Adds an angle between atoms a, b and c to the list of angles
    """
    
    # Check if the angle already exists
    exists = False
    for i in self.angles:
      if i == [a, b, c]:
        exists = True
    
    # Append angle to list if doesn't exist and is plausible
    # (it's a bit unsatisfactory, but I don't think there are
    # better sanity checks)
    if exists == False and a >= 0 and b >= 0 and c >= 0 and a <= len(self.atoms) and b <= len(self.atoms) and c <= len(self.atoms) and a != b and a != c and b != c:
      self.angles.append([a, b, c])

  def addFFBend(self, a, b, c, a0, typ, arg):
    """ (Molecule) -> NoneType

    Adds an angle bend potential between atoms a, b and c to the list of angle bends.
    """

    # Note: There's no check if the bend already exists. Mainly because there's no reason not to have
    # two different functions adding energy to the same "bend"

    # Append bend to list if doesn't exist and is plausible
    # (it's a bit unsatisfactory, but I don't think there are
    # better sanity checks)
    if a >= 0 and b >= 0 and c >= 0 and a <= len(self.atoms) and b <= len(self.atoms) and c <= len(self.atoms) and a != b and a != c and b != c:
      self.bend.append(FFBend(a, b, c, a0, typ, arg))

  def addDihedral(self, a, b, c, d):
    """ (Molecule) -> NoneType
    
    Adds a dihedral between atoms a, b, c and d to the list of dihedrals
    """
    
    # Check if the dihedral already exists
    exists = False
    for i in self.dihedrals:
      if i == [a, b, c, d]:
        exists = True
    
    # Append dihedral to list if doesn't exist and is plausible
    # (it's a bit unsatisfactory, but I don't think there are
    # better sanity checks)
    if exists == False and a >= 0 and b >= 0 and c >= 0 and d >= 0 and a <= len(self.atoms) and b <= len(self.atoms) and c <= len(self.atoms) and d <= len(self.atoms) and a != b and a != c and a != d and b != c and b != d and c != d:
      self.dihedrals.append([a, b, c, d])

  def addFFTorsion(self, a, b, c, d, theta0, typ, arg):
    """ (Molecule) -> NoneType

    Adds a dihedral torsion potential between atoms a, b, c and d to the list of dihedral torsions.
    """

    # Note: There's no check if the bend already exists. Mainly because there's no reason not to have
    # two different functions adding energy to the same "torsion"

    # Append torsion to list if doesn't exist and is plausible
    # (it's a bit unsatisfactory, but I don't think there are
    # better sanity checks)
    if a >= 0 and b >= 0 and c >= 0 and d >= 0 and a <= len(self.atoms) and b <= len(self.atoms) and c <= len(self.atoms) and d <= len(self.atoms) and a != b and a != c and a != d and b != c and b != d and c != d:
      self.tors.append(FFTorsion(a, b, c, d, theta0, typ, arg))

  def cartesianCoordinates(self):
    """ (Molecule) ->

    Returns a list containing the cartesian coordinates.
    """

    coord = []
    for i in self.atoms:
      coord.append(i.coord[0])
      coord.append(i.coord[1])
      coord.append(i.coord[2])

    return coord

  def xyzString(self):
    """ (Molecule) -> str
    
    Returns a string containing an xyz file
    """
    
    s = str(self.numatoms()) + "\n" + self.name + "\n"
    for i in self.atoms:
      t = "{:<3} {: .8f} {: .8f} {: .8f}\n".format(i.symbol, i.coord[0], i.coord[1], i.coord[2])
      s = s + t
    
    return s
  
  def gamessString(self):
    """ (Molecule) -> str
    
      Returns a string containing cartesian coordinates in Gamess format
    """
    
    s = " $DATA\n" + self.name + "\nC1\n"
    for i in self.atoms:
      t = "{:<3} {:<3d} {: .8f} {: .8f} {: .8f}\n".format(i.symbol, i.charge, i.coord[0], i.coord[1], i.coord[2])
      s = s + t
    s =s + " $END\n"
    return s
  
  def gaussString(self):
    """ (Molecule) -> str
    
      Returns a string containing cartesian coordinates in Gaussian format
    """
    
    s = "\n" + self.name + "\n\n" + str(molecule.charge) + " "+ str(molecule.mult) + "\n"
    for i in self.atoms:
      t = "{:<3} {: .8f} {: .8f} {: .8f}\n".format(i.symbol, i.coord[0], i.coord[1], i.coord[2])
      s = s + t
    s =s + "\n"
    return s

  def FFEnergy(self, cartCoordinates, verbosity = 0):
    """ (Molecule) -> number (Force Field energy)

      Returns a number containing the molecular energy according to the current Force Field definition at structure
      specified by the provided cartesian coordinates.
    """

    energy = 0.0
    if verbosity >= 1:
      print("Initial energy for calculation = " + str(energy))
    for i in self.stretch:
      distance=(cartCoordinates[3*i.atom1]-cartCoordinates[3*i.atom2])**2
      distance += (cartCoordinates[3*i.atom1 + 1] - cartCoordinates[3*i.atom2 + 1]) ** 2
      distance += (cartCoordinates[3*i.atom1 + 2] - cartCoordinates[3*i.atom2 + 2]) ** 2
      distance=math.sqrt(distance)
      energy = energy + i.energy(distance)
    if verbosity >= 1:
      print("With bond stretches, energy = " + str(energy))

    for i in self.str13:
      distance=(cartCoordinates[3*i.atom1]-cartCoordinates[3*i.atom2])**2
      distance += (cartCoordinates[3*i.atom1 + 1] - cartCoordinates[3*i.atom2 + 1]) ** 2
      distance += (cartCoordinates[3*i.atom1 + 2] - cartCoordinates[3*i.atom2 + 2]) ** 2
      distance=math.sqrt(distance)
      energy = energy + i.energy(distance)
    if verbosity >= 1:
      print("With 1,3-stretches, energy = " + str(energy))

    for i in self.bend:
      d_bond_1=(cartCoordinates[3*i.atom1]-cartCoordinates[3*i.atom2])**2
      d_bond_1 += (cartCoordinates[3*i.atom1 + 1] - cartCoordinates[3*i.atom2 + 1]) ** 2
      d_bond_1 += (cartCoordinates[3*i.atom1 + 2] - cartCoordinates[3*i.atom2 + 2]) ** 2
      d_bond_1=math.sqrt(d_bond_1)

      d_bond_2=(cartCoordinates[3*i.atom2]-cartCoordinates[3*i.atom3])**2
      d_bond_2 += (cartCoordinates[3*i.atom2 + 1] - cartCoordinates[3*i.atom3 + 1]) ** 2
      d_bond_2 += (cartCoordinates[3*i.atom2 + 2] - cartCoordinates[3*i.atom3 + 2]) ** 2
      d_bond_2=math.sqrt(d_bond_2)

      d_non_bond=(cartCoordinates[3*i.atom1]-cartCoordinates[3*i.atom3])**2
      d_non_bond += (cartCoordinates[3*i.atom1 + 1] - cartCoordinates[3*i.atom3 + 1]) ** 2
      d_non_bond += (cartCoordinates[3*i.atom1 + 2] - cartCoordinates[3*i.atom3 + 2]) ** 2
      d_non_bond=math.sqrt(d_non_bond)

      # Use those distances and the cosine rule to calculate bond angle theta
      numerator = d_bond_1**2 + d_bond_2**2 - d_non_bond**2
      denominator = 2*d_bond_1*d_bond_2
      argument = numerator/denominator
      theta = numpy.arccos(argument)
      energy = energy + i.energy(theta)
    if verbosity >=1:
      print("With bends, energy = " + str(energy))

    for i in self.tors:
      # Calculate the vectors lying along bonds, and their cross products
      atom_e1 = [cartCoordinates[3*i.atom1], cartCoordinates[3*i.atom1+1], cartCoordinates[3*i.atom1+2]]
      atom_b1 = [cartCoordinates[3*i.atom2], cartCoordinates[3*i.atom2+1], cartCoordinates[3*i.atom2+2]]
      atom_b2 = [cartCoordinates[3*i.atom3], cartCoordinates[3*i.atom3+1], cartCoordinates[3*i.atom3+2]]
      atom_e2 = [cartCoordinates[3*i.atom4], cartCoordinates[3*i.atom4+1], cartCoordinates[3*i.atom4+2]]
      end_1 = [atom_e1[i] - atom_b1[i] for i in range(3)]
      bridge = [atom_b1[i] - atom_b2[i] for i in range(3)]
      end_2 = [atom_b2[i] - atom_e2[i] for i in range(3)]
      vnormal_1 = numpy.cross(end_1, bridge)
      vnormal_2 = numpy.cross(bridge, end_2)

      # Construct a set of orthogonal basis vectors to define a frame with vnormal_2 as the x axis
      vcross = numpy.cross(vnormal_2, bridge)
      norm_vn2 = numpy.linalg.norm(vnormal_2)
      norm_b = numpy.linalg.norm(bridge)
      norm_vc = numpy.linalg.norm(vcross)
      basis_vn2 = [vnormal_2[i]/norm_vn2 for i in range(3)]
      basis_b = [bridge[i]/norm_b for i in range(3)]
      basis_cv = [vcross[i]/norm_vc for i in range(3)]

      # Find the signed angle between vnormal_1 and vnormal_2 in the new frame
      vn1_coord_n2 = numpy.dot(vnormal_1, basis_vn2)
      vn1_coord_vc = numpy.dot(vnormal_1, basis_cv)
      psi = math.atan2(vn1_coord_vc, vn1_coord_n2)
      energy = energy + i.energy(psi)
    if verbosity >= 1:
      print("With torsion, energy = " + str(energy))

    for i in self.inv: # Inversion terms aren't implemented yet
      energy += 0.0
    if verbosity >= 1:
      print("With inversion, energy = " + str(energy))
    # Don't forget to add non-bonded interactions here

    if verbosity >=1:
      print("Total energy:")
    return energy


#############################################################################################################
# Most important function so far: Read Quantum Chemistry output file and construct WellFaRe Molecule from it
#############################################################################################################

def extractCoordinates(filename, molecule, verbosity = 0, distfactor = 1.3, bondcutoff = 0.45):
  if verbosity >= 1:
    print("\nSetting up WellFARe molecule: ", molecule.name)
  f = open(filename,'r')
  program = "N/A"
  # Determine which QM program we're dealing with
  for line in f:
    if line.find("Entering Gaussian System, Link 0=g09") != -1:
      if verbosity >= 1:
        print("Reading Gaussian output file: ", filename)
      program = "g09"
      break
    elif line.find("* O   R   C   A *") != -1:
      if verbosity >= 1:
        print("Reading Orca output file: ", filename)
      program = "orca"
      break
  f.close()
  
  # GEOMETRY READING SECTION
  geom = []
  # Read through Gaussian file, read *last* "Input orientation"
  if program == "g09":
    f = open(filename,'r')
    for line in f:
      if line.find("Input orientation:") != -1:
        if verbosity >= 2:
          print("\nInput orientation found, reading coordinates")
        del geom[:]
        for i in range(0,4):
          readBuffer = f.__next__()
        while True:
          readBuffer = f.__next__()
          if readBuffer.find("-----------") == -1:
            geom.append(readBuffer)
            if verbosity >= 3:
              readBuffer=readBuffer.split()
              print(" Found atom: {:<3} {: .8f} {: .8f} {: .8f} in current Input orientation".format(NumberToSymbol[int(readBuffer[1])],float(readBuffer[3]),float(readBuffer[4]),float(readBuffer[5])))
          else:
            break
    if verbosity >= 1:
      print("\nReading of geometry finished.\nAdding atoms to WellFARe molecule: ", molecule.name)
    for i in geom:
      readBuffer=i.split()
      molecule.addAtom(Atom(NumberToSymbol[int(readBuffer[1])],float(readBuffer[3]),float(readBuffer[4]),float(readBuffer[5])))
      if verbosity >= 2:
        print(" {:<3} {: .8f} {: .8f} {: .8f}".format(NumberToSymbol[int(readBuffer[1])],float(readBuffer[3]),float(readBuffer[4]),float(readBuffer[5])))
    f.close()
  # Read through ORCA file, read *last* set of cartesian coordinates
  elif program == "orca":
    f = open(filename,'r')
    for line in f:
      if line.find("CARTESIAN COORDINATES (ANGSTROEM)") != -1:
        if verbosity >= 2:
          print("\nCartesian Coordinates found")
        del geom[:]
        readBuffer = f.__next__()
        while True:
          readBuffer = f.__next__()
          if readBuffer and readBuffer.strip():
            geom.append(readBuffer)
            if verbosity >= 3:
              readBuffer=readBuffer.split()
              print(" Found atom: {:<3} {: .8f} {: .8f} {: .8f} in current Cartesian Coordinates".format(readBuffer[0],float(readBuffer[1]),float(readBuffer[2]),float(readBuffer[3])))
          else:
            break
    if verbosity >= 1:
      print("\nReading of geometry finished.\nAdding atoms to WellFARe molecule: ", molecule.name)
    for i in geom:
      readBuffer=i.split()
      molecule.addAtom(Atom(readBuffer[0],float(readBuffer[1]),float(readBuffer[2]),float(readBuffer[3])))
      if verbosity >= 2:
        print(" {:<3} {: .8f} {: .8f} {: .8f}".format(readBuffer[0],float(readBuffer[1]),float(readBuffer[2]),float(readBuffer[3])))
    f.close()
    
  # BOND ORDER READING SECTION
  bo = []
  bo = numpy.zeros((molecule.numatoms(), molecule.numatoms()))
  if program == "g09":
    f = open(filename,'r')
    for line in f:
      if line.find("Atomic Valencies and Mayer Atomic Bond Orders:") != -1:
        if verbosity >= 2:
          print("\nAtomic Valencies and Mayer Atomic Bond Orders found, reading data")
        bo = numpy.zeros((molecule.numatoms(), molecule.numatoms()))
        while True:
          readBuffer = f.__next__()
          # Check if the whole line is integers only (Header line)
          if isInt("".join(readBuffer.split())) == True:
            # And use this information to label the columns
            columns = readBuffer.split()
          # If we get to the Löwdin charges, we're done reading
          elif readBuffer.find("Lowdin Atomic Charges") != -1:
            break
          else:
            row = readBuffer.split()
            j = 1
            for i in columns:
              j = j + 1
              bo[int(row[0])-1][int(i)-1] = float(row[j])
    f.close()
    if verbosity >= 3:
          print("\nBond Orders:")
          numpy.set_printoptions(suppress=True)
          numpy.set_printoptions(formatter={'float': '{: 0.3f}'.format})
          print(bo)
  if program == "orca":
    f = open(filename,'r')
    for line in f:
      if line.find("Mayer bond orders larger than 0.1") != -1:
        if verbosity >= 2:
          print("\nMayer bond orders larger than 0.1 found, reading data")
        bo = numpy.zeros((molecule.numatoms(), molecule.numatoms()))
        while True:
          readBuffer = f.__next__()
          # Check if the whole line isn't empty (in that case we're done)
          if readBuffer and readBuffer.strip():
            # Break the line into pieces
            readBuffer = readBuffer[1:].strip()
            readBuffer = readBuffer.split("B")
            for i in readBuffer:
              bondpair1=int(i[1:4].strip())
              bondpair2=int(i[8:11].strip())
              order = i[-9:].strip()
              bo[bondpair1][bondpair2] = order
              bo[bondpair2][bondpair1] = order
          else:
            break
    f.close()
    if verbosity >= 3:
      print("\nBond Orders:")
      numpy.set_printoptions(suppress=True)
      numpy.set_printoptions(formatter={'float': '{: 0.3f}'.format})
      print(bo)
    
  # FORCE CONSTANT READING SECTION
  H = []
  H = numpy.zeros((3*molecule.numatoms(), 3*molecule.numatoms()))
  if program == "g09":
    f = open(filename,'r')
    for line in f:
      if line.find("Force constants in Cartesian coordinates") != -1:
        if verbosity >= 2:
          print("\nForce constants in Cartesian coordinates, reading data")
        H = numpy.zeros((3*molecule.numatoms(), 3*molecule.numatoms()))
        while True:
          readBuffer = f.__next__()
          # Check if the whole line is integers only (Header line)
          if isInt("".join(readBuffer.split())) == True:
            # And use this information to label the columns
            columns = readBuffer.split()
          # Once we find the FormGI statement, we're done reading
          elif readBuffer.find("FormGI is forming") != -1 or readBuffer.find("Cartesian forces in FCRed") != -1:
            break
          else:
            row = readBuffer.split()
            for i in range(0,len(row)-1):
              H[int(row[0])-1][int(columns[i])-1] =  row[i+1].replace('D','E')
              H[int(columns[i])-1][int(row[0])-1] =  row[i+1].replace('D','E')
    if verbosity >= 3:
          print("\nForce constants in Cartesian coordinates (Input orientation):")
          #numpy.set_printoptions(suppress=True)
          #numpy.set_printoptions(formatter={'float': '{: 0.3f}'.format})
          print(H)
    f.close()
  
  # Test if we actually have Mayer Bond orders
  if numpy.count_nonzero(bo) != 0:
    if verbosity >= 1:
          print("\nAdding bonds to WellFARe molecule: ", molecule.name)
          print("(using bond orders with a cutoff of {: .2f}):".format(bondcutoff))
    for i in range(0,molecule.numatoms()):
     for j in range(i+1,molecule.numatoms()):
         if bo[i][j] >= bondcutoff:
            molecule.addBond(i,j)
            if verbosity >= 2:
              print(" {:<3} ({:3d}) and {:<3} ({:3d}) (Bond order: {: .3f})".format(molecule.atoms[i].symbol, i, molecule.atoms[j].symbol, j, bo[i][j]))
  # Else use 130% of the sum of covalent radii as criterion for a bond (user defined: distfactor)
  else:
    if verbosity >= 1:
          print("\nAdding bonds to WellFARe molecule:", molecule.name)
          print("(using covalent radii scaled by {: .2f}):".format(distfactor))
    for i in range(0,molecule.numatoms()):
     for j in range(i+1,molecule.numatoms()):
         if molecule.atmatmdist(i,j)<=(SymbolToRadius[molecule.atoms[i].symbol]+SymbolToRadius[molecule.atoms[j].symbol])*distfactor:
            molecule.addBond(i,j)
            if verbosity >= 2:
              print(" {:<3} ({:3d}) and {:<3} ({:3d}) (Distance: {:.3f} A)".format(molecule.atoms[i].symbol, i, molecule.atoms[j].symbol, j, molecule.atmatmdist(i,j)))

  # Now that we know where the bonds are, find angles
  if verbosity >=2:
      print("\nAdding angles to WellFARe molecule: ", molecule.name)
  for i in range(0,len(molecule.bonds)):
    for j in range(i+1,len(molecule.bonds)):
      if molecule.bonds[i][0]==molecule.bonds[j][0]:
        molecule.addAngle(molecule.bonds[i][1],molecule.bonds[i][0],molecule.bonds[j][1])
        if verbosity >= 2:
              print(" {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) ({:6.2f} deg)".format(molecule.atoms[molecule.bonds[i][1]].symbol, molecule.bonds[i][1], molecule.atoms[molecule.bonds[i][0]].symbol, molecule.bonds[i][0], molecule.atoms[molecule.bonds[j][1]].symbol, molecule.bonds[j][1], math.degrees(molecule.bondangle(len(molecule.angles)-1))))
      if molecule.bonds[i][0]==molecule.bonds[j][1]:
        molecule.addAngle(molecule.bonds[i][1],molecule.bonds[i][0],molecule.bonds[j][0])
        if verbosity >= 2:
              print(" {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) ({:6.2f} deg)".format(molecule.atoms[molecule.bonds[i][1]].symbol, molecule.bonds[i][1], molecule.atoms[molecule.bonds[i][0]].symbol, molecule.bonds[i][0], molecule.atoms[molecule.bonds[j][0]].symbol, molecule.bonds[j][0], math.degrees(molecule.bondangle(len(molecule.angles)-1))))
      if molecule.bonds[i][1]==molecule.bonds[j][0]:
        molecule.addAngle(molecule.bonds[i][0],molecule.bonds[i][1],molecule.bonds[j][1])
        if verbosity >= 2:
              print(" {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) ({:6.2f} deg)".format(molecule.atoms[molecule.bonds[i][0]].symbol, molecule.bonds[i][0], molecule.atoms[molecule.bonds[i][1]].symbol, molecule.bonds[i][1], molecule.atoms[molecule.bonds[j][1]].symbol, molecule.bonds[j][1], math.degrees(molecule.bondangle(len(molecule.angles)-1))))
      if molecule.bonds[i][1]==molecule.bonds[j][1]:
        molecule.addAngle(molecule.bonds[i][0],molecule.bonds[i][1],molecule.bonds[j][0])
        if verbosity >= 2:
              print(" {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) ({:6.2f} deg)".format(molecule.atoms[molecule.bonds[i][0]].symbol, molecule.bonds[i][0], molecule.atoms[molecule.bonds[i][1]].symbol, molecule.bonds[i][1], molecule.atoms[molecule.bonds[j][0]].symbol, molecule.bonds[j][0], math.degrees(molecule.bondangle(len(molecule.angles)-1))))

  # Same for dihedrals: Use angles to determine where they are
  if verbosity >= 2:
      print("\nAdding dihedrals to WellFARe molecule: ", molecule.name)
  for i in range(0,len(molecule.angles)):
    for j in range(i+1,len(molecule.angles)):
        if molecule.angles[i][1]==molecule.angles[j][0] and molecule.angles[i][2]==molecule.angles[j][1]:
          molecule.addDihedral(molecule.angles[i][0],molecule.angles[i][1],molecule.angles[i][2],molecule.angles[j][2])
          if verbosity >= 2:
            print(" {:<3} ({:3d}), {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) ({: 7.2f} deg)".format(molecule.atoms[molecule.angles[i][0]].symbol, molecule.angles[i][0], molecule.atoms[molecule.angles[i][1]].symbol, molecule.angles[i][1], molecule.atoms[molecule.angles[i][2]].symbol, molecule.angles[i][2], molecule.atoms[molecule.angles[j][2]].symbol, molecule.angles[j][2], math.degrees(molecule.dihedralangle(len(molecule.dihedrals)-1))))
        if molecule.angles[i][1]==molecule.angles[j][2] and molecule.angles[i][2]==molecule.angles[j][1]:
          molecule.addDihedral(molecule.angles[i][0],molecule.angles[i][1],molecule.angles[i][2],molecule.angles[j][0])
          if verbosity >= 2:
            print(" {:<3} ({:3d}), {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) ({: 7.2f} deg)".format(molecule.atoms[molecule.angles[i][0]].symbol, molecule.angles[i][0], molecule.atoms[molecule.angles[i][1]].symbol, molecule.angles[i][1], molecule.atoms[molecule.angles[i][2]].symbol, molecule.angles[i][2], molecule.atoms[molecule.angles[j][0]].symbol, molecule.angles[j][0], math.degrees(molecule.dihedralangle(len(molecule.dihedrals)-1))))
        if molecule.angles[i][1]==molecule.angles[j][0] and molecule.angles[i][0]==molecule.angles[j][1]:
          molecule.addDihedral(molecule.angles[i][2],molecule.angles[j][0],molecule.angles[j][1],molecule.angles[j][2])
          if verbosity >= 2:
            print(" {:<3} ({:3d}), {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) ({: 7.2f} deg)".format(molecule.atoms[molecule.angles[i][2]].symbol, molecule.angles[i][2], molecule.atoms[molecule.angles[j][0]].symbol, molecule.angles[j][0], molecule.atoms[molecule.angles[j][1]].symbol, molecule.angles[j][1], molecule.atoms[molecule.angles[j][2]].symbol, molecule.angles[j][2], math.degrees(molecule.dihedralangle(len(molecule.dihedrals)-1))))
        if molecule.angles[i][1]==molecule.angles[j][2] and molecule.angles[i][0]==molecule.angles[j][1]:
          molecule.addDihedral(molecule.angles[i][2],molecule.angles[j][2],molecule.angles[j][1],molecule.angles[j][0])
          if verbosity >= 2:
            print(" {:<3} ({:3d}), {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) ({: 7.2f} deg)".format(molecule.atoms[molecule.angles[i][2]].symbol, molecule.angles[i][2], molecule.atoms[molecule.angles[j][2]].symbol, molecule.angles[j][2], molecule.atoms[molecule.angles[j][1]].symbol, molecule.angles[j][1], molecule.atoms[molecule.angles[j][0]].symbol, molecule.angles[j][0], math.degrees(molecule.dihedralangle(len(molecule.dihedrals)-1))))

  # Now that we know bonds, angles and dihedrals, we determine the corresponding force constants
  # Bonds first:
  if verbosity >= 2:
    print("\nAdding Force Field bond stretching terms to WellFARe molecule: ", molecule.name)
  for i in range(0,len(molecule.bonds)):
    #print(molecule.atoms[molecule.bonds[i][0]].coord[1])
    a = numpy.array([molecule.atoms[molecule.bonds[i][0]].coord[0],molecule.atoms[molecule.bonds[i][0]].coord[1],molecule.atoms[molecule.bonds[i][0]].coord[2]])
    b = numpy.array([molecule.atoms[molecule.bonds[i][1]].coord[0],molecule.atoms[molecule.bonds[i][1]].coord[1],molecule.atoms[molecule.bonds[i][1]].coord[2]])
    c1 = (a-b)
    c2 = (b-a)
    c = numpy.zeros(molecule.numatoms()*3)
    c[3*molecule.bonds[i][0]] = c1[0]
    c[3*molecule.bonds[i][0]+1] = c1[1]
    c[3*molecule.bonds[i][0]+2] = c1[2]
    c[3*molecule.bonds[i][1]] = c2[0]
    c[3*molecule.bonds[i][1]+1] = c2[1]
    c[3*molecule.bonds[i][1]+2] = c2[2]
    c=c/numpy.linalg.norm(c)
    fc = numpy.dot(numpy.dot(c,H),numpy.transpose(c))
    if fc < 0.002:
      ProgramWarning()
      print(" This force constant is smaller than 0.002")
    if verbosity >= 2:
      print(" {:<3} ({:3d}) and {:<3} ({:3d}) (Force constant: {: .3f})".format(molecule.atoms[molecule.bonds[i][0]].symbol, molecule.bonds[i][0], molecule.atoms[molecule.bonds[i][1]].symbol, molecule.bonds[i][1], fc))
    molecule.addFFStretch(molecule.bonds[i][0],molecule.bonds[i][1],molecule.atmatmdist(molecule.bonds[i][0],molecule.bonds[i][1]),1,[fc])

  # Then 1,3-stretches:
  if verbosity >= 2:
    print("\nAdding Force Field 1,3-bond stretching terms to WellFARe molecule: ", molecule.name)
  for i in range(0,len(molecule.angles)):
    a = numpy.array([molecule.atoms[molecule.angles[i][0]].coord[0],molecule.atoms[molecule.angles[i][0]].coord[1],molecule.atoms[molecule.angles[i][0]].coord[2]])
    b = numpy.array([molecule.atoms[molecule.angles[i][2]].coord[0],molecule.atoms[molecule.angles[i][2]].coord[1],molecule.atoms[molecule.angles[i][2]].coord[2]])
    c1 = (a-b)
    c2 = (b-a)
    c = numpy.zeros(molecule.numatoms()*3)
    c[3*molecule.angles[i][0]] = c1[0]
    c[3*molecule.angles[i][0]+1] = c1[1]
    c[3*molecule.angles[i][0]+2] = c1[2]
    c[3*molecule.angles[i][1]] = c2[0]
    c[3*molecule.angles[i][1]+1] = c2[1]
    c[3*molecule.angles[i][1]+2] = c2[2]
    c=c/numpy.linalg.norm(c)
    fc = numpy.dot(numpy.dot(c,H),numpy.transpose(c))
    if fc < 0.002:
      ProgramWarning()
      print(" This force constant is smaller than 0.002")
    if verbosity >= 2:
      print(" {:<3} ({:3d}) and {:<3} ({:3d}) (Force constant: {: .3f})".format(molecule.atoms[molecule.angles[i][0]].symbol, molecule.angles[i][0], molecule.atoms[molecule.angles[i][0]].symbol, molecule.angles[i][0], fc))
    molecule.addFFStr13(molecule.angles[i][0],molecule.angles[i][2],molecule.atmatmdist(molecule.angles[i][0],molecule.angles[i][2]),1,[fc])

  # Then angle bends:
  if verbosity >= 2:
    print("\nAdding Force Field angle bending terms to WellFARe molecule: ", molecule.name)
  for i in range(0,len(molecule.angles)):
    a = numpy.array([molecule.atoms[molecule.angles[i][0]].coord[0],molecule.atoms[molecule.angles[i][0]].coord[1],molecule.atoms[molecule.angles[i][0]].coord[2]])
    b = numpy.array([molecule.atoms[molecule.angles[i][1]].coord[0],molecule.atoms[molecule.angles[i][1]].coord[1],molecule.atoms[molecule.angles[i][1]].coord[2]])
    c = numpy.array([molecule.atoms[molecule.angles[i][2]].coord[0],molecule.atoms[molecule.angles[i][2]].coord[1],molecule.atoms[molecule.angles[i][2]].coord[2]])
    aprime = a-b
    bprime = c-b
    p=numpy.cross(aprime,bprime)
    adprime=numpy.cross(p,aprime)
    bdprime=numpy.cross(bprime,p)
    c = numpy.zeros(molecule.numatoms()*3)
    c[3*molecule.angles[i][0]] = adprime[0]
    c[3*molecule.angles[i][0]+1] = adprime[1]
    c[3*molecule.angles[i][0]+2] = adprime[2]
    c[3*molecule.angles[i][2]] = bdprime[0]
    c[3*molecule.angles[i][2]+1] = bdprime[1]
    c[3*molecule.angles[i][2]+2] = bdprime[2]
    c=c/numpy.linalg.norm(c)
    fc = numpy.dot(numpy.dot(c,H),numpy.transpose(c))
    if fc < 0.002:
      ProgramWarning()
      print(" This force constant is smaller than 0.002")
    if verbosity >= 2:
      print(" {:<3} ({:3d}), {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) (Force constant: {: .3f})".format(molecule.atoms[molecule.angles[i][0]].symbol, molecule.angles[i][0], molecule.atoms[molecule.angles[i][1]].symbol, molecule.angles[i][1], molecule.atoms[molecule.angles[j][1]].symbol, molecule.angles[j][1], molecule.atoms[molecule.angles[i][2]].symbol, molecule.angles[i][2], fc))
    molecule.addFFBend(molecule.angles[i][0],molecule.angles[i][1],molecule.angles[i][2],molecule.bondangle(i),2,[fc])

  # Dihedral torsions last:
  if verbosity >= 2:
    print("\nAdding Force Field torsion terms to WellFARe molecule: ", molecule.name)
  for i in range(0,len(molecule.dihedrals)):
    a = numpy.array([molecule.atoms[molecule.dihedrals[i][0]].coord[0],molecule.atoms[molecule.dihedrals[i][0]].coord[1],molecule.atoms[molecule.dihedrals[i][0]].coord[2]])
    b = numpy.array([molecule.atoms[molecule.dihedrals[i][1]].coord[0],molecule.atoms[molecule.dihedrals[i][1]].coord[1],molecule.atoms[molecule.dihedrals[i][1]].coord[2]])
    c = numpy.array([molecule.atoms[molecule.dihedrals[i][2]].coord[0],molecule.atoms[molecule.dihedrals[i][2]].coord[1],molecule.atoms[molecule.dihedrals[i][2]].coord[2]])
    d = numpy.array([molecule.atoms[molecule.dihedrals[i][3]].coord[0],molecule.atoms[molecule.dihedrals[i][3]].coord[1],molecule.atoms[molecule.dihedrals[i][3]].coord[2]])
    aprime = a-b
    dprime = d-c
    c1prime = c-b
    c2prime = b-c
    p1=numpy.cross(aprime,c1prime)
    p2=numpy.cross(dprime,c2prime)
    c = numpy.zeros(molecule.numatoms()*3)
    c[3*molecule.dihedrals[i][0]] = p1[0]
    c[3*molecule.dihedrals[i][0]+1] = p1[1]
    c[3*molecule.dihedrals[i][0]+2] = p1[2]
    c[3*molecule.dihedrals[i][2]] = p2[0]
    c[3*molecule.dihedrals[i][2]+1] = p2[1]
    c[3*molecule.dihedrals[i][2]+2] = p2[2]
    c=c/numpy.linalg.norm(c)
    fc = numpy.dot(numpy.dot(c,H),numpy.transpose(c))
    if fc < 0.002:
      ProgramWarning()
      print(" This force constant is smaller than 0.002")
    if verbosity >= 2:
      print(" {:<3} ({:3d}), {:<3} ({:3d}), {:<3} ({:3d}) and {:<3} ({:3d}) (Force constant: {: .3f})".format(molecule.atoms[molecule.dihedrals[i][0]].symbol, molecule.dihedrals[i][0], molecule.atoms[molecule.dihedrals[i][1]].symbol, molecule.dihedrals[i][1], molecule.atoms[molecule.dihedrals[i][2]].symbol, molecule.dihedrals[i][2], molecule.atoms[molecule.dihedrals[i][3]].symbol, molecule.dihedrals[i][3], fc))
    molecule.addFFTorsion(molecule.dihedrals[i][0],molecule.dihedrals[i][1],molecule.dihedrals[i][2],molecule.dihedrals[i][3],molecule.dihedralangle(i),1,[fc])

  # End of routine

###############################################################################
#                                                                             #
# The main part of the program starts here                                    #
#                                                                             #
###############################################################################

# Print GPL v3 statement and program header
ProgramHeader()

# Determine the name of the file to be read
infile = iofiles(sys.argv[1:])

# print("Number of Atoms: ", reactant_mol.numatoms(), "Multiplicity: ", reactant_mol.mult)

# print(molecule)
# print("Molecular mass = ", reactant_mol.mass())
# reactant_mol.orient()

# print(reactant_mol.gaussString())

# print("Bonds:")
# for i in reactant_mol.bonds:
#   print(i)
#
# print("")
# print("Angles:")
# for i in reactant_mol.angles:
#   print(i)
#
# print("")
# print("Angles in degrees:")
# for i in range(len(reactant_mol.angles)):
#   print(math.degrees(reactant_mol.bondangle(i)))
#
# print("")
# print("Dihedrals:")
# for i in reactant_mol.dihedrals:
#   print(i)
#
# print("")
# print("Dihedral angles in degrees:")
# for i in range(len(reactant_mol.dihedrals)):
#   print(math.degrees(reactant_mol.dihedralangle(i)))

# print("")
# print("Bond Stretches:")
# for i in reactant_mol.stretch:
#   print(i)
#
# print("")
# print("1-3 Bond Stretches:")
# for i in reactant_mol.str13:
#   print(i)
#
# print("")
# print("Angle Bends:")
# for i in reactant_mol.bend:
#   print(i)
#
# print("")
# print("Dihedral Torsions:")
# for i in reactant_mol.tors:
#   print(i)

reactant_mol = Molecule("Reactant",0)
extractCoordinates("g09-dielsalder-r.log", reactant_mol, verbosity = 2)

product_mol = Molecule("Product",0)
extractCoordinates("g09-dielsalder-p.log", product_mol, verbosity = 2)

# print("\nCartesian Coordinates (as one list):")
# print(reactant_mol.cartesianCoordinates())

print("\nForce Field Energy:")
print(reactant_mol.FFEnergy(reactant_mol.cartesianCoordinates(), verbosity = 1))

print("\nDistort Geometry and print energy again:")
coordinates2optimiseR = reactant_mol.cartesianCoordinates()
coordinates2optimiseP = product_mol.cartesianCoordinates()

coordinates2optimiseR = (numpy.array(coordinates2optimiseR)+(numpy.array(coordinates2optimiseP))/2.0)

print(reactant_mol.FFEnergy(coordinates2optimiseR, verbosity = 1))

print("\nGeometry Optimizer:")
xopt = scipy.optimize.fmin_bfgs(reactant_mol.FFEnergy, coordinates2optimiseR, gtol=0.00005)
print("\nOptimized Geometry:")
print(xopt)

ProgramFooter()
