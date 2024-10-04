import numpy as np

def get_reflectivity_at_location(ZC_reconstructed, Axis1, Axis2, zAxis,location, altitude=None):
    """
    Get the reflectivity values at a given longitude and latitude, optionally at a given altitude.
    
    Parameters:
    ZC_reconstructed (np.ndarray): The reconstructed reflectivity grid.
    Axis1 (np.ndarray): The latitude axis.
    Axis2 (np.ndarray): The longitude axis.
    zAxis (np.ndarray): The altitude axis.
    location (tuple): A tuple containing the longitude and latitude.

    altitude (float, optional): The altitude to get reflectivity values for. If None, return values for all altitudes.
    
    Returns:
    np.ndarray: The reflectivity values at the given location and altitude, or an empty array if out of bounds.
    """
    longitude, latitude = location
    
    # Find the closest indices for the given longitude and latitude
    x_idx = (np.abs(Axis2 - longitude)).argmin()
    y_idx = (np.abs(Axis1 - latitude)).argmin()
 
    # Check if the indices are out of bounds
    if longitude < Axis2.min() or longitude > Axis2.max() or latitude < Axis1.min() or latitude > Axis1.max():
        return np.array([])  # Return an empty array if out of bounds
    
    if altitude is not None:
        # Find the closest index for the given altitude
        z_idx = (np.abs(zAxis - altitude)).argmin()
        return ZC_reconstructed[y_idx, x_idx, z_idx]
    else:
        # Return reflectivity values for all altitudes
        return ZC_reconstructed[y_idx, x_idx, :]

# Example usage:
# reflectivities = get_reflectivity_at_location(ZC_reconstructed, Axis1, Axis2, zAxis, longitude, latitude, altitude)