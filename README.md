# Information
The function of this code is to find ***n***, the refractive index of a medium, given experimental ThZ data. The process is as follows:

1. Time-transmission intensity data is recorded using a Terahertz Spectrometer.
2. Fast-Fourier Transform Analysis is applied to the experimental data, transforming it into frequency-magnitude data.
3. For each frequency, the ratio of the magnituded record in Medium X and air is recorded. As the magnitude in air for any frequency wil be higher, this ratio will always be $\large \leq 1$.
4. The formula 

$\Large \frac{t_{\text{layer}}}{t_{\text{air}}} = \frac{\frac{4n}{(n+1)^2} e^{ink_0 d}}{e^{ik_0 d}} = \frac{4n}{(n+1)^2} e^{i(n-1)k_0 d}$

will be used to calculate ***n***, the refractive index of the medium, using an optimization algorithm. Given $\large \frac{t_{layer}}{t_{air}}$, $\large k_0$ ($\large k_0=\frac{2\pi f}{c}$) where $\large f$ is frequency, and the thickness of the layer $\large d$, the refractive index $\large n$ can be subsequently approximated.

# Using the Program
1. First, append the necessary time-transmission data information to *data.txt*.
2. Run *main.py*. Manual fitting of data is currently preferred for accuracy reasons. A while loop will run which will allow the user to manually select the indices of data they wish to use, which they can also view visually.
3. The program will output the calculated ***n*** values for the manually fitted frequencies the user decides.
