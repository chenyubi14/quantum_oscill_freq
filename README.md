# theory background
For theoretical background, chapter 14 of Solid State Physics by Ashcroft/Mermin is a good reference.
This is a set of tools I found to calculate quantum oscillation frequencies for magnetic susceptibility (de HAAS-van ALPHEN effect), conductivity (Shubnikov-de Haas effect), and magnetorestriction, etc.

The quantum oscillation frequencies are proportional to extremal Fermi surface areas (Onsage relation, eq 14.15 in Ashcroft/Mermin), so the key is to calculate Fermi surface, and find extremal area perpendicular to applied magnetic field.

I have found a set of useful online tools and formed a working flow. I also made additional changes to adjust for more needs.

# Working flow
## Calculate Fermi surface
Use a dense K-grid to calculate Fermi surface by VASP, and use c2x (https://www.c2x.org.uk/fermi/vasp.html) to get a fermi_surface.bxsf file. The .bsxf file stores the information of band energies at the discrete dense K-point grid.
## Obtain Fermi surface
