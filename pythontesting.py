import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from scipy.interpolate import interp1d
from scipy.ndimage import median_filter
from csaps import CubicSmoothingSpline
from scipy.interpolate import UnivariateSpline

#zscan = open('Smartlab data/ZscanSTBXRR_0014_Scan2020Jan24-124745.dat', 'r')
xrr_spec = open('Smartlab data/spec2Pt111_Al2O3_006_1.dat', 'r')
xrr_bkg = open('Smartlab data/bkg2Pt111_Al2O3_006.dat', 'r')
# not sure if this is the right set of files lol 

#zscan = open('Smartlab data/Zscan_0007_Scan2020Jan23-191605.dat', 'r')
#zscan = open('Zscan_1.DAT', 'r')
zscan = open('Zscan_2.DAT', 'r')
#zscan = open('Zscan_XRR_0009_Scan2020Feb07-220747.DAT', 'r')

# read files into lists, turn lists into numpy matrices
# possibly change so that sybols to ignore are more general? / ask Carlos
# if there are any others? 
zscan_z  = []
zscan_cps = []
for line in zscan:
    if line[0] != "*" and line[0] != "#" and line[0] != ";":
        z, cps = line.split(' ')
        cps = cps.strip('\n')
        zscan_z.append(float(z))
        zscan_cps.append(float(cps))

zscan.close()
zscan_z = np.array(zscan_z)
zscan_cps = np.array(zscan_cps)

spec_theta  = []
spec_cps = []
for line in xrr_spec:
    if line[0] != "*" and line[0] != "#":
        theta, cps = line.split(' ')
        cps = cps.strip('\n')
        spec_theta.append(float(theta))
        spec_cps.append(float(cps))

xrr_spec.close()
spec_theta = np.array(spec_theta)
spec_cps = np.array(spec_cps)

bkg_theta  = []
bkg_cps = []
for line in xrr_bkg:
    if line[0] != "*" and line[0] != "#":
        theta, cps = line.split(' ')
        cps = cps.strip('\n')
        bkg_theta.append(float(theta))
        bkg_cps.append(float(cps))

xrr_bkg.close()
bkg_theta = np.array(bkg_theta)
bkg_cps = np.array(bkg_cps)        

print(zscan_z)
print(zscan_cps)
#print(spec_theta)
#print(spec_cps)
#print(bkg_theta)
#print(bkg_cps)

#test = scipy.signal.savgol_filter(zscan_cps, 101, polyorder=7, deriv=0)
#testgrad = np.gradient(test, zscan_z) 

#tst = scipy.ndimage.median_filter(zscan_cps, size=5)
#tstg = np.gradient(tst, zscan_z)

#tstgg = scipy.ndimage.median_filter(tstg, size=5)
#tstg2 = scipy.signal.savgol_filter(tstg, 101, polyorder=7, deriv=0)

#tstggg = scipy.ndimage.median_filter(first_deriv, size=5)

#cp = CubicSmoothingSpline(zscan_z, zscan_cps, smooth=0.99995).spline
#cpgrad = cp.derivative(nu=1)
#spl = UnivariateSpline(zscan_z, zscan_cps, k=4, s= 1e15)
#spl2 = UnivariateSpline(zscan_z, first_deriv, k=4, s= 3e15)
#cpnewt = np.gradient(spl(z2), z2)
#dd22 = np.gradient(cpnewt, z2)
#dd3 = np.gradient(cpgrad(z2), z2)
#plt.plot(zscan_z, zscan_cps)
#plt.plot(zscan_z, tst)
#plt.plot(zscan_z, test)
#plt.plot(z2, spl(z2))
#plt.plot(zscan_z, ftwo(x2))
#plt.figure()
#plt.plot(z2, cpgrad(z2))
#plt.plot(z2, cpnewt)
#plt.plot(zscan_z, tstg)
#plt.plot(zscan_z, tstg2)
#plt.plot(zscan_z, testgrad)
#plt.plot(zscan_z, newt)
#plt.plot(zscan_z, tstgg)
#plt.plot(zscan_z, np.gradient(tstg2, zscan_z))
#plt.plot(zscan_z, np.gradient(testgrad, zscan_z))
#plt.figure()
#plt.plot(z2, dd22)
#plt.plot(z2, dd3)
#plt.plot(z2, spl2(z2))
#plt.plot(zscan_z, zscan_cps, 'o', z2, cp(z2), '-')


first_deriv = np.gradient(zscan_cps, zscan_z)
z2 = np.linspace(zscan_z[0], zscan_z[zscan_z.size - 1], zscan_z.size)

d1_fun = CubicSmoothingSpline(zscan_z, first_deriv, smooth=0.99995).spline
d2 = np.gradient(d1_fun(z2), z2)

#filter_arr = d1_fun(z2) < 0 
#reduced_d1 = d1_fun(z2)[filter_arr]
#reduced_z2 = z2[filter_arr]

d1 = d1_fun(z2)

#edge case never gets above 0 
min_pos = d1.argmin()
curr_val = d1[min_pos]
curr_index = min_pos
while curr_val < 0:
    curr_index = curr_index + 1
    curr_val = d1[curr_index]
    print(curr_val)

print("done")    

end_ind = curr_index 

curr_val = d1[min_pos]
curr_index = min_pos
while curr_val < 0:
    curr_index = curr_index - 1
    curr_val = d1[curr_index]
    print(curr_val)
    

start_ind = curr_index 

reduced_d1 = d1[start_ind:end_ind]
reduced_z2 = z2[start_ind:end_ind]


plt.plot(zscan_z, zscan_cps)
plt.figure()
plt.plot(zscan_z, first_deriv)
plt.plot(z2, d1_fun(z2))
plt.plot(reduced_z2, reduced_d1)
plt.figure()
plt.plot(z2, d2) 
plt.plot(reduced_z2, np.gradient(reduced_d1, reduced_z2))
plt.figure()
plt.plot(z2, np.gradient(d2, z2)) 
plt.plot(reduced_z2, np.gradient(np.gradient(reduced_d1, reduced_z2), reduced_z2))

print(max(d2))
print(min(d2))
max_pos = d2.argmax()
min_pos = d2.argmin()

print(z2[max_pos])
print(z2[min_pos])

plt.show()




