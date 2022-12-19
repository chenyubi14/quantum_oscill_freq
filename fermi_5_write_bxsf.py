import numpy as np
from ase.io import read
import os
import sys
import argparse

print('2pi is NOT in k definition!')

class ebands3d(object):
    '''
    '''

    def __init__(self, efermi, kmesh, kpoints, energies, rlat):
        '''
        Initialization
        '''
        print('usage: obj.read_bxsf(efermi, kmesh, kpoints, energies)')
        self.read_bxsf(efermi, kmesh, kpoints, energies, rlat) # self.efermi is read from .bxsf 
        # reset the Fermi energy by the given value
        #if efermi:
        #    self.efermi=efermi
        self.find_fermicrossing_bands()
        self.get_fermi_ebands3d()

    def get_fermi_ebands3d(self):
        '''
        For those bands that cross the Fermi level, unfold the band energies on
        the irreducible BZ onto the whole reciprocal primitive cell.
        '''

        # band energies of the k-points within the primitive cell
        self.fermi_ebands3d_uc = []
        # band energies of the k-points within the Brillouin Zone
        # self.fermi_ebands3d_bz = []

        # nx, ny, nz = self.kmesh
        for ispin in range(self.nspin):
            uc_tmp = []
            # bz_tmp = []
            for iband in self.fermi_xbands[ispin]: # the band that crosses with Fermi level
                # the band energies of the k-points within primitive cell
                etmp = self.ir_ebands[ispin, : , iband]
                etmp.shape = list(reversed(self.kmesh)) 
                etmp = np.swapaxes(etmp, 0, 2) 
                #etmp = self.ir_ebands[ispin, :, iband] # shape is (nx*ny*nz)
                #etmp.shape = list(self.kmesh) # shape is (nx, ny, nz)
                # I removed 'reversed' in the original form: list(reversed(self.kmesh))
                # it is because, in the original form, x-index in the "grid" runs fastest # which is given by self.fs_kpath
                # # make the band energies periodic in the primitive cell
                # etmp = np.tile(etmp, (2,2,2))[:nx+1, :ny+1, :nz+1]
                uc_tmp.append(etmp)

            self.fermi_ebands3d_uc.append(uc_tmp)
            # self.fermi_ebands3d_bz.append(bz_tmp)

    def find_fermicrossing_bands(self):
        '''
        Find the index of the bands that cross the Fermi level.
        '''

        band_index = np.arange(self.nbnds, dtype=int)

        band_energy_max = np.max(self.ir_ebands, axis=1)
        band_energy_min = np.min(self.ir_ebands, axis=1)
        fermi_cross_band = (band_energy_min < self.efermi) & (
            self.efermi < band_energy_max)

        self.fermi_xbands = [band_index[fermi_cross_band[ii]]
                             for ii in range(self.nspin)]
        print('fermi crossing bands', self.fermi_xbands)

        if np.sum([x.size for x in self.fermi_xbands]) == 0:
            raise ValueError(
                "No surface found at {:8.4f} eV!".format(self.efermi))

    def read_bxsf(self, efermi, kmesh, kpoints, energies, rlat):
        '''
        Read band energies from VASP EIGENVAL file.
        '''

        self.kmesh = kmesh
        self.ir_kpath = kpoints # (kpoints_num, 3)
        self.ir_ebands = energies[np.newaxis, :, :]  # (1, kpoints_num, band_num)

        self.nspin = 1                  # pretend it is spin degenerate
        self.nbnds = np.shape(self.ir_ebands)[-1]
        self.efermi = efermi
        self.reclat = rlat # reciprocal lattice
        
        
    def to_bxsf(self, prefix='ebands3d', ncol=6):
        ''' 
        Output the ebands3d as Xcrysden .bxsf format.
        '''

        with open('{:s}.bxsf'.format(prefix), 'w') as out:
            out.write("BEGIN_INFO\n")
            out.write("  # Launch as: xcrysden --bxsf ebands3d.bxsf\n")
            out.write("  Fermi Energy: {:12.6f}\n".format(self.efermi))
            out.write("END_INFO\n\n")

            out.write("BEGIN_BLOCK_BANDGRID_3D\n")
            out.write("  band_energies\n")
            out.write("  BANDGRID_3D_BANDS\n")

            # the number of bands that corss the Fermi level
            number_fermi_xbands = sum([len(xx) for xx in self.fermi_xbands])
            out.write("    {:d}\n".format(number_fermi_xbands))
            # number of data-points in each direction (i.e. nx ny nz for 3D gr)
            out.write("    {:5d}{:5d}{:5d}\n".format(*(x for x in self.kmesh)))
            # origin of the bandgrid.
            # Warning: origin should be (0,0,0) (i.e. Gamma point)
            out.write("    {:16.8f}{:16.8f}{:16.8f}\n".format(0.0, 0.0, 0.0))
            # Reciprocal lattice vector
            out.write(
                '\n'.join(["    " + ''.join(["%16.8f" % xx for xx in row])
                           for row in self.reclat]) # should use self.reclat HERE !!!
            )   

            for ispin in range(self.nspin):
                sign = 1 if ispin == 0 else -1
                for ii in range(len(self.fermi_xbands[ispin])):
                    iband = self.fermi_xbands[ispin][ii]
                    b3d = self.fermi_ebands3d_uc[ispin][ii].copy()
                    nx, ny, nz = b3d.shape
                    b3d.shape = (nx * ny, nz)

                    out.write("\n    BAND: {:5d}\n".format(iband * sign))
                    out.write(
                        '\n'.join(["    " + ''.join(["%16.8e" % xx for xx in row])
                                   for row in b3d])
                    )
                    # np.savetxt(out, b3d, fmt='%16.8E')

            out.write("\n  END_BANDGRID_3D\n")
            out.write("END_BLOCK_BANDGRID_3D\n")

