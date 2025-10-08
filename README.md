ContourMap Library Examples
This notebook demonstrates the usage of the ContourMap class from the essentials.py library.

The ContourMap class is designed to generate contour plots from scattered 2D data (X, Y, and Z values) using different interpolation methods.
![png](https://raw.github.com/Nashat90/PetroMap/main/ContourMapUsage_files/All.png)
## 1. Setup
First, let's import the necessary libraries and the ContourMap class itself. We'll also generate some sample data to work with.


```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# You'll need to have your essentials.py file in the same directory
from PetroMap.essentials import ContourMap
import pandas as pd
data = pd.read_excel("cleaned xy data.xlsx")
X = data.XCOORD
Y = data.YCOORD
Z = data.PAY
well_names = data.ALIAS.to_list()
```

## 2. Cubic Spline Interpolation with Matplotlib
The default interpolation method for ContourMap is cubic spline interpolation. This is great for creating a smooth, continuous surface. By default, the backend is set to 'matplotlib'.


```python
# Create a ContourMap instance for cubic interpolation
contour_cubic_mpl = ContourMap(X, Y, Z, well_names=well_names)

# Plot the map and display it
fig = contour_cubic_mpl.plot_cubicmap(title="Cubic Spline Interpolation (Matplotlib)")
plt.show()
```


    
![png](https://raw.githubusercontent.com/Nashat90/PetroMap/main/ContourMapUsage_files/ContourMapUsage_3_0.png)
    


## 3. K-Nearest Neighbors (KNN) Interpolation
The plot_knnmap method uses a machine learning approach (KNN) to interpolate the data. This can be useful for data with sharp discontinuities.


```python
# Create a ContourMap instance for KNN interpolation
contour_knn_mpl = ContourMap(X, Y, Z, well_names=well_names)

# Plot the map using KNN with 5 neighbors
fig = contour_knn_mpl.plot_knnmap(title="KNN Interpolation (Matplotlib)", n_neighbors=5)
plt.show()

```


    
![png](https://raw.githubusercontent.com/Nashat90/PetroMap/main/ContourMapUsage_files/ContourMapUsage_5_0.png)
    


## 4. Radial Basis Function (RBF) Interpolation
The plot_rbfmap method provides another powerful interpolation technique. You can specify different functions to control the shape of the surface.


```python
# Create a ContourMap instance for RBF interpolation
contour_rbf_mpl = ContourMap(X, Y, Z, well_names=well_names)

# Plot the map using RBF with the 'gaussian' function
fig = contour_rbf_mpl.plot_rbfmap(title="RBF Interpolation ('gaussian' function)", function='gaussian')
plt.show()

```


    
![png](https://raw.github.com/Nashat90/PetroMap/main/ContourMapUsage_files/ContourMapUsage_7_0.png)
    


## 5. Using the Plotly Backend
If you have Plotly installed, you can use a more interactive backend for your plots.


```python
# Create a ContourMap instance for cubic interpolation
contour_cubic_mpl = ContourMap(X, Y, Z, well_names=well_names, backend="plotly")

# Plot the map and display it
fig = contour_cubic_mpl.plot_cubicmap(title="Cubic Spline Interpolation (Matplotlib)")
fig.update_layout(height=1000, template="plotly_dark")
```



## 6. Using the Kriging Interploation
You can use Kriging interpolation to distribute geospatial properties using PyKrige Library
```python
# Create a ContourMap instance for Kriging Simulation
contour_cubic_mpl = ContourMap(X, Y, Z, well_names=well_names, backend="plotly")

# Plot the map and display it
fig = contour_cubic_mpl.plot_krigemap(title="Kriging Map")
fig.update_layout(height=800)

```
![png](https://raw.github.com/Nashat90/PetroMap/main/ContourMapUsage_files/Krige.png)
