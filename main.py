import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import re
from scipy.optimize import minimize_scalar

# Convert paired data to a list of tuples
def paired_to_tuple_arr(paired_data):
    tuple_arr = []
    lines = paired_data.strip("\n")
    for line in lines:
        row = line.split()
        tuple_arr.append((float(row[0]), float(row[1])))
    return tuple_arr

# Convert a list of tuples to paired data format
def tuple_arr_to_paired(tuple_arr):
    paired_data = ""
    for tuple_pair in tuple_arr:
        paired_data += f"{tuple_pair[0]}\t{tuple_pair[1]}\n"
    return paired_data

# Perform Fourier transform on data tuples
def fourier(data_tuples):
    x = [item[0] for item in data_tuples]
    y = [item[1] for item in data_tuples]

    y_fft = np.fft.fft(y)
    frequencies = np.fft.fftfreq(len(y), d=(x[1] - x[0]))
    magnitudes = np.abs(y_fft)

    positive_indices = frequencies >= 0
    positive_frequencies = frequencies[positive_indices]
    positive_magnitudes = magnitudes[positive_indices]

    fft_data = list(zip(positive_frequencies, positive_magnitudes))

    plt.figure(figsize=(10, 5))
    plt.plot(positive_frequencies, positive_magnitudes, label='FFT Magnitude')
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    plt.title('FFT of Data')
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    return [(float(freq), float(mag)) for freq, mag in fft_data]

# Extract raw data from a text file
def extract_data():
    with open("data.txt", "r") as file:
        lines = file.readlines()

    air_rawdata = []
    medium_rawdata = []
    current_section = None

    for line in lines:
        if "Air Raw Data" in line:
            current_section = "air"
        elif "Medium Raw Data" in line:
            current_section = "medium"
        elif current_section:
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            if numbers:
                x = float(numbers[0])
                y = float(numbers[1])
                if current_section == "air":
                    air_rawdata.append((x, y))
                elif current_section == "medium":
                    medium_rawdata.append((x, y))
    
    return air_rawdata, medium_rawdata

# Append data to a text file
def append_data(paired_data, data_title):
    with open("data.txt", "a") as file:
        file.write(data_title)
        file.write(paired_data)

# Main script execution starts here
air_rawdata, medium_rawdata = extract_data()
air_fftdata = fourier(air_rawdata)
medium_fftdata = fourier(medium_rawdata)
append_data(tuple_arr_to_paired(air_fftdata), "\nAir FFT Table\nFrequency           Amplitude\n")
append_data(tuple_arr_to_paired(medium_fftdata), "\nMedium FFT Table\nFrequency           Amplitude\n")

frequencies = [pair[0] for pair in air_fftdata]
ratios = [air[1] / medium[1] for medium, air in zip(medium_fftdata, air_fftdata)]

# User input for frequency limits and plot the ratio fit
ratioFit = False
while not ratioFit:
    lowerLimit = int(input("Enter the lower limit for frequency (index of data point): "))
    upperLimit = int(input("Enter the upper limit for frequency (index of data point): "))

    # Ensure the limits are within the valid range
    if lowerLimit < 0 or upperLimit > len(frequencies) or lowerLimit >= upperLimit:
        print("Invalid limits. Please try again.")
        continue

    plt.figure(figsize=(10, 6))
    plt.plot(frequencies[lowerLimit:upperLimit], ratios[lowerLimit:upperLimit], marker='o')
    plt.title('Silicon Magnitude / Air Magnitude vs. Frequency')
    plt.xlabel('Frequency')
    plt.ylabel('Silicon Magnitude / Air Magnitude')
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    goodFit = input("Type 'Y' if the fit is good: ").strip().upper()
    if goodFit == "Y":
        frequencies = frequencies[lowerLimit:upperLimit]
        ratios = ratios[lowerLimit:upperLimit]
        ratioFit = True

# Constants
d = 0.00021  # Distance in meters

# Convert ratios and frequencies to numpy arrays
ratios = np.array(ratios)
frequencies = np.array(frequencies)

# Define the equation for magnitude calculation
def calculate_magnitude(n, f):
    expr = (4 * n / (n + 1)**2) * sp.exp(sp.I * (n - 1) * (2 * sp.pi * f * d / (3e8)))
    magnitude = abs(complex(expr.evalf()))
    return magnitude

# Objective function to minimize the difference between calculated and actual magnitude
def objective_function(n, f, ratio):
    return abs(calculate_magnitude(n, f) - ratio)

# Find the best guess for n
def find_best_n(f, ratio):
    result = minimize_scalar(objective_function, bounds=(1, 5), args=(f, ratio), method='bounded')
    return result.x

# Iterate over the provided values and find the best guess for n
best_n_values = []
for f, ratio in zip(frequencies, ratios):
    best_n = find_best_n(f, ratio)
    best_n_values.append(best_n)
    print(f"Best guess for n (f={f}, RHS={ratio}): {best_n}")
