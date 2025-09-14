### Version History
### - v0: Sep 12, 2025, [github/@aasfaw](https:github.com/aasfaw)

import matplotlib.pyplot as plotter; plotter.rcParams['font.family'] = 'Monospace'
from math import comb, ceil
import numpy as np

def plot_logical_error_probabilities(distances, physical_errors, all_logical_errors, all_analytical_errors, ylim=[1e-10, 1.1]):
    
    plotter.figure(figsize=(10, 8))

    num_curves = 1 if distances is None else len(distances)
    colors = plotter.cm.viridis(np.linspace(0, 0.8, num_curves))

    plotter.loglog(physical_errors, physical_errors, label = 'Unprotected qubit',
                          linewidth=2, linestyle = '--', color='gray',
                          )
    
    if distances is None:
        plotter.loglog(physical_errors, all_logical_errors,
                          marker='o', linewidth=2, markersize=8,
                          color=colors[0],
                          )
    else:
        if all_analytical_errors is None:
            for distance, logical_errors, color in zip(distances, all_logical_errors, colors):
                    plotter.loglog(physical_errors, logical_errors, label = f'd = {distance}',
                                  marker='o', linewidth=2, markersize=8,
                                  color=color,
                                  )
        else:
            for distance, logical_errors, analytical_errors, color in zip(distances, all_logical_errors, all_analytical_errors, colors):
                plotter.loglog(physical_errors, logical_errors, label = f'd = {distance} simulated',
                              marker='o', linewidth=2, markersize=8,
                              color=color,
                              )
                plotter.loglog(physical_errors, analytical_errors, label = f'd = {distance} analytical',
                              linewidth=2, linestyle = '--', color=color,
                              )
    
    plotter.legend()
    plotter.xlim([physical_errors.min(), physical_errors.max()])
    plotter.ylim(ylim)
    plotter.grid(visible=True, which='major', axis='both')
    plotter.xlabel('Physical error probability')
    plotter.ylabel('Logical error probability')
    plotter.tight_layout()
    plotter.show()

def get_logical_error_probability_analytical(distances, physical_errors):

    # # method 1: small p approximation
    # all_analytical_errors = []
    # for distance in distances:
    #     t = ceil(distance / 2)
    #     analytical_errors = comb(distance, t) * physical_errors**t
    #     all_analytical_errors.append(analytical_errors)

    # method 2: full expression
    all_analytical_errors = []
    for distance in distances:
        analytical_error = 0
        for i in range(ceil(distance/2.), distance + 1):
            analytical_error += comb(distance, i) * physical_errors**i * (1-physical_errors)**(distance-i)
        all_analytical_errors.append(analytical_error)

    return all_analytical_errors