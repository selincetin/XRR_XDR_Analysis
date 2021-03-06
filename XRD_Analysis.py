import numpy as np
import matplotlib.pyplot as plt
import re
import zscan_fun 
import file_reading
from math import pi
from scipy.signal import argrelextrema 
import heapq 
from csaps import CubicSmoothingSpline
import XRD_fun
from scipy.optimize import curve_fit

#user_lambda = input("Enter lambda (Angstroms) ")
user_lambda = 1.54184 
step_size = .02
scan_speed = .25
spec_res = 0 
rocking_res = 0 

zscan = open('Smartlab data/Zscan_0007_Scan2020Jan23-191605.dat', 'r')
xrr_spec = open('Smartlab data/spec2Pt111_Al2O3_006_1.dat', 'r')
xrr_bkg = open('Smartlab data/bkg2Pt111_Al2O3_006.dat', 'r')
#rocking = open('Smartlab data/RC_Pt_111_0013_Scan2020Jan23-194300_1.dat', 'r')

#xrr_spec = open('Smartlab data/2theta_Al2O3_0016_Scan2020Jan23-192933.dat', 'r')
#rocking = open('Smartlab data/RC_Al2O3_0010_Scan2020Jan23-193141.dat', 'r')

#xrr_spec = open('C:/Users/selin/Downloads/2020_8_21_DATAFILES/2020_8_21_DATAFILES/PLD02112020_MoO2/2TW_MoO2_200_0013_Scan2020Jul18-192754.txt', 'r')
#xrr_bkg = open('C:/Users/selin/Downloads/2020_8_21_DATAFILES/2020_8_21_DATAFILES/PLD02112020_MoO2/2TW_BKG_MoO2_200_0014_Scan2020Jul18-193932.txt', 'r')

# read files into lists, turn lists into numpy matrices
zscan_z, zscan_cps = file_reading.pull_data(zscan)
spec_theta, spec_cps = file_reading.pull_data(xrr_spec)
bkg_theta, bkg_cps = file_reading.pull_data(xrr_bkg)  
#rock_theta, rock_cps = file_reading.pull_data(rocking) #maybe I should change theta on spec and bkg to 2theta for clarity 

#get the effective beam height, STB intensity 
stb_inten, effective_beam_height,_,_,_,_,_ = zscan_fun.stb_intensity_and_eff_beam_height(zscan_z, zscan_cps)

#Specular & background 
spec_q = 4 * pi * np.sin(np.deg2rad(spec_theta / 2)) / user_lambda
bkg_q = 4 * pi * np.sin(np.deg2rad(bkg_theta / 2)) / user_lambda

#difference between specular cps and background cps; normalize by STB intensity 
diff_cps = spec_cps - bkg_cps
norm_reflectivity = diff_cps / stb_inten

#compute error bars 
error_bars = np.sqrt((spec_cps * step_size * 60 / scan_speed) + (bkg_cps * step_size * 60 / scan_speed)) / stb_inten

#find the start and end indices of the bragg peak

#testing 
bragg_start_ind, bragg_end_ind = XRD_fun.find_bragg_peak_user_assist(spec_q, norm_reflectivity)

#bragg_start_ind, bragg_end_ind = XRD_fun.find_bragg_peak_alt(spec_q, norm_reflectivity)

#bragg_start_ind, bragg_end_ind = XRD_fun.find_bragg_peak(spec_q, norm_reflectivity)
#bragg_start_ind, bragg_end_ind = XRD_fun.find_bragg_peak_rc(spec_q, norm_reflectivity)
#bragg_start_ind = bragg_start_ind[0]
#bragg_end_ind = bragg_end_ind[0]

#reduce the data to only the bragg peak -- this is the data to be used when Gaussian fitting the bragg peak 
bragg_refl = norm_reflectivity[bragg_start_ind:bragg_end_ind]
bragg_q = spec_q[bragg_start_ind:bragg_end_ind]

#p0 = [np.zeros([1, bragg_q.size]), 1, 1, np.zeros([1, bragg_q.size])]
#p0 = [np.log10(np.average([bragg_cps[0], bragg_cps[bragg_cps.size - 1]])), .1, 1, np.average([bragg_q[0], bragg_q[bragg_q.size - 1]])]
#np.log10(bragg_cps[0])
#coeff, var_matrix = curve_fit(XRD_fun.gauss, bragg_q, np.log10(bragg_cps), p0=p0)

#Gaussian fit the bragg peak. Area (10) may need to be changed between this, rocking curve, substrate peak, etc. Try integrating
p0 = [np.average([bragg_refl[0], bragg_refl[bragg_refl.size - 1]]), 10, (bragg_q[0] - bragg_q[bragg_q.size - 1]) / 2, np.average([bragg_q[0], bragg_q[bragg_q.size - 1]])]
coeff, var_matrix = curve_fit(XRD_fun.gauss, bragg_q, bragg_refl, p0=p0)

fit = XRD_fun.gauss(bragg_q, *coeff)
FWHM = abs(np.sqrt(2 * np.log(2)) * coeff[2])

#vertical domain size 
vert_domain_size = 2 * pi * 0.94 / np.sqrt(np.power(FWHM, 2) - np.power(spec_res, 2))

#plt.plot(bragg_q, np.log10(bragg_cps))
#plt.plot(bragg_q, fit)
#plt.plot(bragg_q, np.log10(fit))
#print((spec_q[bragg_start_ind], spec_q[bragg_end_ind]))

plt.figure()
plt.plot(bragg_q, bragg_refl, label="raw data")
plt.plot(bragg_q, fit, label="Gaussian fit")
plt.xlabel(r'q ($\mathrm{\AA}$)')
plt.ylabel("Reflectivity")
plt.title("q vs Reflectivity")
plt.legend()
plt.yscale("log")

plt.figure()
plt.plot(spec_q, norm_reflectivity)
plt.plot(bragg_q, fit, label="Gaussian fit")
plt.xlabel(r'q ($\mathrm{\AA}$)')
plt.ylabel("Reflectivity")
plt.title("q vs Reflectivity")
plt.yscale("log")

plt.figure()
plt.errorbar(spec_q[2:], norm_reflectivity[2:], yerr=error_bars[2:], ecolor='red')
plt.xlabel(r'q ($\mathrm{\AA}$)')
plt.ylabel("Reflectivity")
plt.title("q vs Reflectivity")
plt.yscale("log")

plt.show()

#find the start and end indices of the bragg peak
#rc_start_ind, rc_end_ind = XRD_fun.find_bragg_peak(rock_theta, (rock_cps / stb_inten)) 
rc_start_ind, rc_end_ind = XRD_fun.find_bragg_peak_rc(rock_theta, (rock_cps / stb_inten)) 
rc_start_ind = rc_start_ind[0]
rc_end_ind = rc_end_ind[0]

#reduce the data to only the bragg peak -- this is the data to be used when lorentz fitting the bragg peak 
rc_refl = (rock_cps / stb_inten)[rc_start_ind:rc_end_ind]
rc_btheta = rock_theta[rc_start_ind:rc_end_ind]

p0 = [np.average([rc_refl[0], rc_refl[rc_refl.size - 1]]), 10, (rc_btheta[0] - rc_btheta[rc_btheta.size - 1]) / 2, np.average([rc_btheta[0], rc_btheta[rc_btheta.size - 1]])]
coeff, var_matrix = curve_fit(XRD_fun.lorentz, rc_btheta, rc_refl, p0=p0)

fit2 = XRD_fun.lorentz(rc_btheta, *coeff)

plt.figure()
plt.plot(rock_theta, rock_cps)
plt.yscale("log")

plt.figure()
plt.plot(rc_btheta, rc_refl, label="raw data")
plt.plot(rc_btheta, fit2, label="Lorentz fit")
plt.show()





