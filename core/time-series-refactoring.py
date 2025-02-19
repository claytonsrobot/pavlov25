import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from rdp import rdp  # Install with: pip install rdp

# Step 1: Generate 1000 time series data points
np.random.seed(42)
time_vector = np.linspace(0, 10, 1000)  # 1000 evenly spaced time values
raw_signal = np.sin(time_vector * 2 * np.pi / 10) + np.random.normal(scale=0.2, size=len(time_vector))  # Sine wave + noise

# Step 2A: Anomaly Detection Filtering (removes extreme outliers)
threshold = 2  # Define anomaly threshold
anomaly_indices = np.abs(raw_signal - np.mean(raw_signal)) < threshold
filtered_time_anomaly = time_vector[anomaly_indices]
filtered_signal_anomaly = raw_signal[anomaly_indices]

# Step 2B: Douglas-Peucker Filtering (reduces complexity)
tolerance = 0.05  # Adjust for more/less simplification
simplified_points = rdp(np.column_stack((time_vector, raw_signal)), epsilon=tolerance)
filtered_time_douglas, filtered_signal_douglas = simplified_points[:, 0], simplified_points[:, 1]

# Step 2C: Apply Both Filters in Sequence (Anomaly First, Then Douglas-Peucker)
filtered_time_anomaly_then_douglas = filtered_time_anomaly
filtered_signal_anomaly_then_douglas = filtered_signal_anomaly

simplified_points_combined = rdp(
    np.column_stack((filtered_time_anomaly_then_douglas, filtered_signal_anomaly_then_douglas)), 
    epsilon=tolerance
)
filtered_time_combined, filtered_signal_combined = simplified_points_combined[:, 0], simplified_points_combined[:, 1]

# Step 3: Resample All Filtered Versions onto a 50-Point Uniform Grid
new_time_vector = np.linspace(time_vector[0], time_vector[-1], 50)  # 50 evenly spaced points

# Interpolating each filtered version onto the 50-point time vector
interp_anomaly = interp1d(filtered_time_anomaly, filtered_signal_anomaly, kind='linear', fill_value="extrapolate")
interp_douglas = interp1d(filtered_time_douglas, filtered_signal_douglas, kind='linear', fill_value="extrapolate")
interp_combined = interp1d(filtered_time_combined, filtered_signal_combined, kind='linear', fill_value="extrapolate")

resampled_signal_anomaly = interp_anomaly(new_time_vector)
resampled_signal_douglas = interp_douglas(new_time_vector)
resampled_signal_combined = interp_combined(new_time_vector)

# Step 4: Plot the Results
plt.figure(figsize=(12, 6))

plt.plot(time_vector, raw_signal, 'k-', alpha=0.3, label="Raw Signal (1000 points)")
plt.plot(new_time_vector, resampled_signal_anomaly, 'r-o', markersize=3, label="Resampled Anomaly Filtered (50 points)")
plt.plot(new_time_vector, resampled_signal_douglas, 'b-s', markersize=3, label="Resampled Douglas-Peucker (50 points)")
plt.plot(new_time_vector, resampled_signal_combined, 'g-^', markersize=3, label="Resampled Combined (50 points)")

plt.legend()
plt.xlabel("Time")
plt.ylabel("Signal Value")
plt.title("Comparison of Different Filtering Methods (Resampled to 50 Points)")
plt.show()
