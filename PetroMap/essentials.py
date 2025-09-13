# file: contourmap.py

import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

try:
    import plotly.graph_objects as go
    plotly_available = True
except ImportError:
    plotly_available = False

class ContourMap:
    """
    ContourMap class to generate contour maps from X, Y, Z data using cubic spline interpolation.
    
    Parameters:
    -----------
    X : array-like
        X coordinates of points
    Y : array-like
        Y coordinates of points
    Z : array-like
        Z values at the points
    grid_points : int
        Number of points in the interpolation grid along each axis
    backend : str, optional
        'matplotlib' or 'plotly' (default 'matplotlib')
    well_names : list of str, optional
        Names of the wells/data points to show on the plot
    """

    def __init__(self, X, Y, Z, grid_points=100, backend='matplotlib', well_names=None):
        self.X = np.array(X)
        self.Y = np.array(Y)
        self.Z = np.array(Z)
        self.grid_points = grid_points
        self.backend = backend.lower()
        self.well_names = well_names
        
        if self.backend == 'plotly' and not plotly_available:
            print("Plotly not found. Falling back to matplotlib.")
            self.backend = 'matplotlib'

        # Generate grid
        self.grid_x, self.grid_y = np.meshgrid(
            np.linspace(min(self.X), max(self.X), self.grid_points),
            np.linspace(min(self.Y), max(self.Y), self.grid_points)
        )

        # Interpolate Z values on the grid
        self.grid_z = griddata(
            points=(self.X, self.Y),
            values=self.Z,
            xi=(self.grid_x, self.grid_y),
            method='cubic'
        )

    def plot_cubicmap(self, title="Contour Map", cmap='viridis'):
        """
        Plot the contour map using the selected backend.
        """
        if self.backend == 'matplotlib':
            fig, ax = plt.subplots(figsize=(8,6))

            # Create contour plot
            contour = ax.contourf(self.grid_x, self.grid_y, self.grid_z, cmap=cmap)

            # Scatter data points
            ax.scatter(self.X, self.Y, c='red', marker='o', label='Data points')

            # Plot well names if provided
            if self.well_names is not None:
                for i, name in enumerate(self.well_names):
                    ax.text(self.X[i], self.Y[i], name, fontsize=9, color='white', ha='left', va='bottom')

            # Add colorbar
            fig.colorbar(contour, ax=ax, label='Z')

            # Set titles and labels
            ax.set_title(title)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.legend()
            # Return the figure object instead of showing it
            return fig


        elif self.backend == 'plotly':
            fig = go.Figure(data=[go.Contour(
                z=self.grid_z,
                x=np.linspace(min(self.X), max(self.X), self.grid_points),
                y=np.linspace(min(self.Y), max(self.Y), self.grid_points),
                colorscale='Viridis',
                contours=dict(showlines=False)
            )])
            fig.add_trace(go.Scatter(
                x=self.X, y=self.Y, mode='markers+text' if self.well_names else 'markers',
                text=self.well_names if self.well_names else None,
                textposition='top right',
                marker=dict(color='red', size=6),
                name='Data points'
            ))
            fig.update_layout(title=title, xaxis_title='X', yaxis_title='Y')
            return fig  
    def plot_knnmap(self, title="Contour Map", cmap='viridis', n_neighbors=5):
        """
        Plot the contour map using KNN interpolation on the selected backend and return Matplotlib figure if backend is matplotlib.
        """
        from sklearn.neighbors import KNeighborsRegressor

        # Fit KNN on the input data
        knn = KNeighborsRegressor(n_neighbors=n_neighbors, weights='distance')
        knn.fit(np.column_stack((self.X, self.Y)), self.Z)

        # Predict Z values on the grid
        self.grid_z = knn.predict(np.column_stack((self.grid_x.ravel(), self.grid_y.ravel())))
        self.grid_z = self.grid_z.reshape(self.grid_x.shape)

        if self.backend == 'matplotlib':
            fig, ax = plt.subplots(figsize=(8,6))
            contour = ax.contourf(self.grid_x, self.grid_y, self.grid_z, cmap=cmap)
            ax.scatter(self.X, self.Y, c='red', marker='o', label='Data points')

            if self.well_names is not None:
                for i, name in enumerate(self.well_names):
                    ax.text(self.X[i], self.Y[i], name, fontsize=9, color='white', ha='left', va='bottom')

            fig.colorbar(contour, ax=ax, label='Z')
            ax.set_title(title)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.legend()
            
            # Return the figure object
            return fig

        elif self.backend == 'plotly':
            import plotly.graph_objects as go
            fig = go.Figure(data=[go.Contour(
                z=self.grid_z,
                x=np.linspace(min(self.X), max(self.X), self.grid_points),
                y=np.linspace(min(self.Y), max(self.Y), self.grid_points),
                colorscale='Viridis',
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
    def plot_rbfmap(self, title="Contour Map", cmap='viridis', function='multiquadric', epsilon=None):
        """
        Plot the contour map using RBF (Radial Basis Function) interpolation.
        
        Parameters:
        -----------
        title : str
            Title of the plot
        cmap : str
            Colormap for matplotlib backend
        function : str
            Type of RBF: 'multiquadric', 'inverse', 'gaussian', 'linear', 'cubic', 'quintic', 'thin_plate'
        epsilon : float, optional
            Adjustable parameter for some RBF functions; if None, it's determined automatically
        """
        # Fit RBF to the input data
        rbf = Rbf(self.X, self.Y, self.Z, function=function, epsilon=epsilon)
        
        # Predict Z values on the grid
        self.grid_z = rbf(self.grid_x, self.grid_y)
        
        # Plotting
        if self.backend == 'matplotlib':
            fig, ax = plt.subplots(figsize=(8,6))
            contour = ax.contourf(self.grid_x, self.grid_y, self.grid_z, cmap=cmap)
            ax.scatter(self.X, self.Y, c='red', marker='o', label='Data points')
            
            if self.well_names is not None:
                for i, name in enumerate(self.well_names):
                    ax.text(self.X[i], self.Y[i], name, fontsize=9, color='white', ha='left', va='bottom')
            
            fig.colorbar(contour, ax=ax, label='Z')
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
                colorscale='Viridis',
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
   