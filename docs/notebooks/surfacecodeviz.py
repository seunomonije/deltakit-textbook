import cirq
import matplotlib.pyplot as plotter
from matplotlib.patches import Circle, Rectangle
import numpy as np

class PlanarSurfaceCode:
    """
    Unrotated planar surface code with respective qubit layout.
    We will use a grid structure showing:
    - Data qubits (D)
    - X ancillas (X)
    - Z ancillas (Z)    
    """
    
    def __init__(self, distance):
        self.distance = distance
        self.data_qubits, self.z_ancillas, self.x_ancillas = self.layout_planar_surface_code(distance)
        self._define_stabilizers()
    
    def layout_planar_surface_code(self, d):
        """
        Layout surface code on a nearest neighbor
        grid.

        """
        data_qubits = {}
        z_anc = {} # qubits for Z stabilizers
        x_anc = {} # qubits for X stabilizers
        for i in range(2 * d - 1):
            for j in range(2 * d - 1):
                if (i + j) % 2 == 0:
                    data_qubits[(i, j)] = cirq.GridQubit(i, j)
                elif i % 2 == 0:
                    z_anc[(i, j)] = cirq.GridQubit(i, j)
                else:
                    x_anc[(i, j)] = cirq.GridQubit(i, j)
        return data_qubits, z_anc, x_anc
    
    def _define_stabilizers(self):
        """
        Define stabilizer generators for the surface code.

        """
        self.x_stabilizers = {}
        self.z_stabilizers = {}
        
        # X stabilizers - each X ancilla measures 4 neighboring data qubits
        for pos in self.x_ancillas:
            i, j = pos
            neighbors = [
                (i-1, j), (i+1, j), (i, j-1), (i, j+1)
            ]
            # Only include neighbors that are data qubits
            data_neighbors = [n for n in neighbors if n in self.data_qubits]
            if data_neighbors:  # Only add if there are valid neighbors
                self.x_stabilizers[pos] = data_neighbors
        
        # Z stabilizers - each Z ancilla measures 4 neighboring data qubits  
        for pos in self.z_ancillas:
            i, j = pos
            neighbors = [
                (i-1, j), (i+1, j), (i, j-1), (i, j+1)
            ]
            # Only include neighbors that are data qubits
            data_neighbors = [n for n in neighbors if n in self.data_qubits]
            if data_neighbors:  # Only add if there are valid neighbors
                self.z_stabilizers[pos] = data_neighbors

    def visualize_layout(self):
        """
        Visualize the surface code layout with data qubits and ancillas.
        
        """
        fig, ax = plotter.subplots(1, 1, figsize=(10, 8))
        
        size = 2 * self.distance - 1
        
        # Draw data qubits
        for pos in self.data_qubits:
            i, j = pos
            color = 'lightblue'
            circle = Circle((j, size-1-i), 0.3, color=color, ec='black', linewidth=2)
            ax.add_patch(circle)
            ax.text(j, size-1-i, 'D', ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Draw X ancillas
        for pos in self.x_ancillas:
            i, j = pos
            color = 'lightgreen'
            
            square = Rectangle((j-0.3/2, size-1-i-0.3/2), 0.3, 0.3, 
                             color=color, ec='black', linewidth=2)
            ax.add_patch(square)
            ax.text(j, size-1-i, 'X', ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Draw Z ancillas
        for pos in self.z_ancillas:
            i, j = pos
            color = 'lightyellow'   
            diamond_x = [j, j+0.15, j, j-0.15, j]
            diamond_y = [size-1-i+0.15, size-1-i, size-1-i-0.15, size-1-i, size-1-i+0.15]
            ax.plot(diamond_x, diamond_y, 'k-', linewidth=2)
            ax.fill(diamond_x, diamond_y, color=color)
            ax.text(j, size-1-i, 'Z', ha='center', va='center', fontweight='bold', fontsize=8)
        
        # Draw stabilizer connections
        for pos, data_qubits_list in self.x_stabilizers.items():
            i, j = pos
            for di, dj in data_qubits_list:
                ax.plot([j, dj], [size-1-i, size-1-di], 'g--', alpha=0.7, linewidth=2)
        
        for pos, data_qubits_list in self.z_stabilizers.items():
            i, j = pos
            for di, dj in data_qubits_list:
                ax.plot([j, dj], [size-1-i, size-1-di], 'y--', alpha=0.7, linewidth=2)
        
        ax.set_xlim(-0.5, size-0.5)
        ax.set_ylim(-0.5, size-0.5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        title = f'Distance-{self.distance} Planar Surface Code Layout'
        ax.set_title(title, fontsize=16, fontweight='bold')
        
        legend_elements = [
            Circle((0, 0), 0.1, color='lightblue', ec='black', label='Data Qubit'),
            Rectangle((0, 0), 0.1, 0.1, color='lightgreen', ec='black', label='X Ancilla'),
            Rectangle((0, 0), 0.1, 0.1, color='lightyellow', ec='black', label='Z Ancilla'),
        ]
        
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
        plotter.tight_layout()
        plotter.show()
        
        # Print surface code parameters
        print(f"Surface Code Distance: {self.distance}")
        print(f"Total qubits: {len(self.data_qubits) + len(self.x_ancillas) + len(self.z_ancillas)}")
        print(f"Data qubits: {len(self.data_qubits)}")
        print(f"X ancillas: {len(self.x_ancillas)}")
        print(f"Z ancillas: {len(self.z_ancillas)}")
        print(f"X stabilizers: {len(self.x_stabilizers)}")
        print(f"Z stabilizers: {len(self.z_stabilizers)}")