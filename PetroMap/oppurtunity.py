from sklearn.preprocessing import MinMaxScaler
from scipy.interpolate import Rbf
import numpy as np
import matplotlib.pyplot as plt

class OppurtunityContour:
    def __init__(self, data, backend='matplotlib', grid_points=399, well_names=None):
        self.data = data
        self.backend = backend
        self.grid_points = grid_points
        self.well_names = well_names

        # Coordinates
        self.X = data['XCOORD'].values.__abs__()
        self.Y = data['YCOORD'].values.__abs__()

        # Create meshgrid
        self.grid_x, self.grid_y = np.meshgrid(
            np.linspace(min(self.X), max(self.X), self.grid_points),
            np.linspace(min(self.Y), max(self.Y), self.grid_points)
        )

    def plot_oppurtunity_map(self, variables=['PAY', 'POROSITY', 'SW'], weights=None,
                    title="Opportunity Map", cmap='viridis', function='linear', epsilon=None,
                    highlight_percentile=80):
        """
        Plot the contour map using RBF interpolation with a composite score of chosen variables.

        Parameters
        ----------
        variables : list of str
            Names of variables in the data to include in the composite score
        weights : list of float, optional
            Weight for each variable; defaults to equal weighting
        title : str
            Plot title
        cmap : str
            Colormap
        function : str
            RBF function type 
        epsilon : float, optional
            RBF epsilon
        highlight_percentile : float
            Percentile threshold to highlight top opportunity zones
        """
        # Default equal weights if not provided
        if weights is None:
            weights = [1/len(variables)] * len(variables)
        elif len(weights) != len(variables):
            raise ValueError("Length of weights must match length of variables")

        # Normalize variables and compute composite score
        normalized_vars = []
        scaler = MinMaxScaler()
        for var in variables:
            if var.upper() == 'SW':
                val = 1 - self.data[var].values.__abs__()  # invert SW
            else:
                val = self.data[var].values.__abs__()
            normalized_vars.append(scaler.fit_transform(val.reshape(-1, 1)).flatten())

        # Composite score with adjustable weights
        self.Z = np.zeros_like(normalized_vars[0])
        for i, norm_var in enumerate(normalized_vars):
            self.Z += weights[i] * norm_var

        # RBF interpolation
        rbf = Rbf(self.X, self.Y, self.Z, function=function, epsilon=epsilon)
        self.grid_z = rbf(self.grid_x, self.grid_y)

        # Identify top opportunity zones
        threshold = np.percentile(self.grid_z, highlight_percentile)
        highlight_mask = self.grid_z >= threshold

        # Plotting
        if self.backend == 'matplotlib':
            fig, ax = plt.subplots(figsize=(8,6))
            contour = ax.contourf(self.grid_x, self.grid_y, self.grid_z, cmap=cmap)
            ax.scatter(self.X, self.Y, c='red', marker='o', label='Data points')

            # Highlight top opportunity zones

            # Optional well names
            if self.well_names is not None:
                for i, name in enumerate(self.well_names):
                    ax.text(self.X[i], self.Y[i], name, fontsize=9, color='white', ha='left', va='bottom')

            fig.colorbar(contour, ax=ax, label='Composite Score')
            ax.set_title(title)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.legend()
            return fig

        elif self.backend == 'plotly':
            import plotly.graph_objects as go
            fig = go.Figure(data=[go.Contour(
                z=self.grid_z,
                x=np.linspace(min(self.X), max(self.X), self.grid_points),
                y=np.linspace(min(self.Y), max(self.Y), self.grid_points),
                colorscale=cmap,
                contours=dict(showlines=False)
            )])
            fig.add_trace(go.Scatter(
                x=self.X, y=self.Y,
                mode='markers+text' if self.well_names else 'markers',
                text=self.well_names if self.well_names else None,
                textposition='top right',
                marker=dict(color='red', size=6),
                name='Data points'
            ))
            fig.update_layout(title=title, xaxis_title='X', yaxis_title='Y')
            return fig
