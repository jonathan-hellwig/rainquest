import h5py
import numpy as np
import pandas as pd

def read_radar_data(h5_file, radar_name, year, month=None, day=None, hour=None, minute=None,valid_altitudes=False):
    """
    Reconstructs the reflectivity grid from an HDF5 radar file for a specific time acquisition
    or a range of acquisitions based on the specified year, month, day, hour, and minute.
    
    Parameters:
    h5_file (str): The path to the HDF5 file.
    radar_name (str): The radar name to read data for.
    year (str): The year to filter by (format 'YYYY').
    month (str, optional): The month to filter by (format 'MM').
    day (str, optional): The day to filter by (format 'DD').
    hour (str, optional): The hour to filter by (format 'HH').
    minute (str, optional): The minute to filter by (format 'mm').
    
    Returns:
    pd.DataFrame: A DataFrame containing the reconstructed grid data for all matching acquisitions.
    """


    # Open the HDF5 file
    with h5py.File(h5_file, 'r') as h5:
        # Read Axis1, Axis2, and zAxis from the radar group (common to all time acquisitions)
        group_path = f'/{radar_name}'
        Axis1 = h5[group_path]['Axis1'][:].flatten()
        Axis2 = h5[group_path]['Axis2'][:].flatten()
        zAxis = h5[group_path]['zAxis'][:].flatten()

        # Determine original grid size based on sizes of Axis1, Axis2, and zAxis
        # original_grid_size = (len(Axis1), len(Axis2), len(zAxis))
        # original_grid_size = (len(Axis1[0,:]), len(Axis2), len(zAxis))


        # Read radar position (latitude, longitude, elevation) from the radar group
        radar_lat = h5[group_path].attrs['radar_latitude'][0]
        radar_lon = h5[group_path].attrs['radar_longitude'][0]
        radar_alt = h5[group_path].attrs['radar_elevation'][0]
        radar_pos = [radar_lon, radar_lat, radar_alt]

        # Define the base group path
        base_group_path = f'/{radar_name}/{year}/{month}/{day}/{hour}/{minute}'
   
        x_indices = h5[base_group_path + '/Axis2_index'][:]
        y_indices = h5[base_group_path + '/Axis1_index'][:]
        zAxis_indices = h5[base_group_path + '/zAxis_index'][:]
        z_values = h5[base_group_path + '/zAxis_values'][:, :]
        utc_time = h5[base_group_path].attrs['UTC'][0]
        # utc_time = pd.to_datetime(utc_time_str, unit='s')
        
        if valid_altitudes:
            original_grid_size = (len(Axis1), len(Axis2), len(zAxis_indices[0,:]))
            zAxis = zAxis[zAxis_indices - 1].flatten()  # Adjust zAxis to only include valid altitudes
            
        else:
            original_grid_size = (len(Axis1), len(Axis2), len(zAxis))
        

        # Initialize the reconstructed grid with NaNs
        ZC_reconstructed = np.full(original_grid_size, np.nan)
        
        # Reconstruct the grid by iterating over the sparse indices
        for idx in range(len(x_indices[0,:])):
            # print("idx:", idx)
            x = x_indices[0,idx]-1 # Subtract 1 to convert to 0-based index
            y = y_indices[0,idx]-1
            # print("x:", x)
            # print("y:", y)
            if valid_altitudes:
                ZC_reconstructed[x, y, :] = z_values[:,idx]
            else:     
                z = zAxis_indices-1
                # Map z_values to the correct z-levels using zAxis_index
                ZC_reconstructed[x, y, z] = z_values[:,idx]

    return ZC_reconstructed, Axis1, Axis2, zAxis, utc_time, radar_pos


