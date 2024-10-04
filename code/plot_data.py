from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def plot_reflectivity_grid(ZC_reconstructed, Axis1, Axis2, zAxis, radar_name, utc_time, locations=None):
    """
    Plot the 2D slices of the reconstructed reflectivity grid.
    
    Parameters:
    ZC_reconstructed (np.ndarray): The reconstructed reflectivity grid.
    Axis1 (np.ndarray): The latitude axis.
    Axis2 (np.ndarray): The longitude axis.
    zAxis (np.ndarray): The altitude axis.
    radar_name (str): The radar name.
    utc_time (float): The UTC time of the data.
    locations (list of tuples, optional): List of (longitude, latitude) tuples to plot on the grid.
    """
    # Convert UTC time to human-readable format
    human_readable_time = datetime.fromtimestamp(utc_time, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Define a colormap
    colormap = cm.get_cmap('viridis', len(zAxis))

    # Iterate over the zAxis levels and plot each slice
    for i, z in enumerate(zAxis):
        ZC_slice = ZC_reconstructed[:, :, i]
        # Mask NaN values for transparency
        masked_ZC_slice = np.ma.masked_where(np.isnan(ZC_slice), ZC_slice)
        # Plot the slice with transparency
        c = ax.pcolormesh(Axis2, Axis1, masked_ZC_slice, cmap=colormap, alpha=0.5, shading='auto')

    # Add colorbar
    cbar = fig.colorbar(c, ax=ax)
    cbar.set_label('Reflectivity (dBZ)')

    # Plot locations if provided
    if locations:
        for location in locations:
            longitude, latitude = location
            ax.plot(longitude, latitude, 'ro')  # Plot as red dots
            ax.text(longitude, latitude, f'({longitude}, {latitude})', color='red', fontsize=8)

    # Set axis labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(f'Reflectivity Grid\nRadar: {radar_name}, Time: {human_readable_time}')

    # Show the plot
    plt.show()
    
def plot_reflectivity_altitude(ZC_reconstructed, Axis1, Axis2, zAxis, radar_name, utc_time, locations=None):
    """
    Plot the 2D slices of the reconstructed reflectivity grid with colorbar based on zAxis.
    
    Parameters:
    ZC_reconstructed (np.ndarray): The reconstructed reflectivity grid.
    Axis1 (np.ndarray): The latitude axis.
    Axis2 (np.ndarray): The longitude axis.
    zAxis (np.ndarray): The altitude axis.
    radar_name (str): The radar name.
    utc_time (float): The UTC time of the data.
    locations (list of tuples, optional): List of (longitude, latitude) tuples to plot on the grid.
    """
    # Convert UTC time to human-readable format
    human_readable_time = datetime.fromtimestamp(utc_time, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Define a colormap
    colormap = cm.get_cmap('plasma', len(zAxis))

    # Iterate over the zAxis levels and plot each slice
    for i, z in enumerate(zAxis):
        ZC_slice = ZC_reconstructed[:, :, i]
        # Mask NaN values for transparency
        masked_ZC_slice = np.ma.masked_where(np.isnan(ZC_slice), ZC_slice)
        # Plot the slice with transparency
        c = ax.pcolormesh(Axis2, Axis1, masked_ZC_slice, cmap=colormap, alpha=0.5, shading='auto')

    # Add colorbar based on zAxis
    cbar = fig.colorbar(cm.ScalarMappable(cmap=colormap), ax=ax)
    cbar.set_ticks(np.linspace(0, len(zAxis) - 1, len(zAxis)))
    cbar.set_ticklabels([f'{int(z)}' for z in zAxis])
    cbar.set_label('Altitude (m)')

    # Plot locations if provided
    if locations:
        for location in locations:
            longitude, latitude = location
            ax.plot(longitude, latitude, 'ro')  # Plot as red dots
            ax.text(longitude, latitude, f'({longitude}, {latitude})', color='red', fontsize=8)

    # Set axis labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(f'Reflectivity Grid by Altitude\nRadar: {radar_name}, Time: {human_readable_time}')

    # Show the plot
    plt.show()

