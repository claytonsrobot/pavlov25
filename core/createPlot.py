"""
Title: createPlot.py
Author: Clayton Bennett
Creted 11 December 2024
"""
import matplotlib.pyplot as plt

# Create your plot
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])

# Save the figure as a PDF
plt.savefig("my_plot.pdf")

# Save the figure as a SVG
plt.savefig("my_plot.svg")

# Save the figure as a PNG
plt.savefig("my_plot.png")