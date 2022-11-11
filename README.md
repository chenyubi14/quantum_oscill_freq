# Theorical background
For theoretical background, chapter 14 of Solid State Physics by Ashcroft/Mermin is a good reference.
This repository contains a set of tools I found to calculate quantum oscillation frequencies for magnetic susceptibility (de HAAS-van ALPHEN effect), conductivity (Shubnikov-de Haas effect), and magnetorestriction, etc.

The quantum oscillation frequencies are proportional to extremal Fermi surface areas (Onsage relation, eq 14.15 in Ashcroft/Mermin), so the key is to calculate Fermi surface, and find extremal area perpendicular to applied magnetic field.

I have found a set of useful online tools and developped a working flow. I also made additional changes to adjust for more needs.

# Working flow
## DFT calculation to obtain Fermi surface
First run a VASP job by a dense K-grid for Fermi surface calculation, and use c2x (https://www.c2x.org.uk/fermi/vasp.html) to get a fermi_surface.bxsf file. The .bxsf file stores the information of Fermi surface by saving band energies at the dense K-point grid.
## File format change
The .bxsf file needs some modifications as the requirement of the next step. Here are a complete set of notes for this step. 
(1) Download xcrysden in a linux system (http://www.xcrysden.org/Download.html). Xcrysden is supposed to work for MacOS, but I did not figure it out for Mac.
(2) Output band-specific .bxsf files in xcrysden for bands with Fermi surface (http://www.xcrysden.org/doc/fermi.html). 
You may also refer to SKEAF README to see why the requirements are necessary. 

## Quantum oscillation frequencies by SKEAF
The implementation principle is well illustrated in the SKEAF paper (https://arxiv.org/pdf/0803.1895.pdf). In principle, you can download the original version of SKEAF (http://www.democritos.it/pipermail/xcrysden/2012-July/001234.html), but I have made some changes to the source for an easier usage. Please download my updated SKEAF version. 
(1) Compile the SKEAF codes by `gfortran skeaf_v1p3p0_r149.F90 -o skeaf` and `gfortran ELK_exciting_BXSFconverter_v04.F90 -o bxsfconverter`. You will have two binaries compiled named `skeaf` and `bxsfconverter`. Move these two binaries to your working directory, or add the their location to `$PATH` in `.bashrc`
(2) Run `bxsfconverter`, make the following choices: band.bxsf(filename), n(not on a periodic grid), n(not having factor 2*Pi), e(energy unit is eV), n(not divided exponent), n(not switched sign), converted.bxsf(output filename)
Note if you don't use my updated version, you will only have two choices for energy unit: hartree and rydberg.
As a result, you will see a file with name `converted.bxsf`, and we will use it for skeaf calculation
(3) Run SKEAF to by directly typing `skeaf` in your terminal.
