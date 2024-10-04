import h5py
import pandas as pd

def read_rain_data(h5_file, station_id, year=None, month=None, day=None, hour=None, minute=None):
    """
    Reads rain data from an HDF5 file for a specified station, with filtering options for year, month, day, hour, and minute.
    
    Parameters:
    h5_file (str): The path to the HDF5 file.
    station_id (str): The station ID to read data for.
    year (str, optional): The year to filter by (format 'YYYY').
    month (str, optional): The month to filter by (format 'MM').
    day (str, optional): The day to filter by (format 'DD').
    hour (str, optional): The hour to filter by (format 'HH').
    minute (str, optional): The minute to filter by (format 'mm').
    
    Returns:
    pd.DataFrame: A DataFrame containing the utc and RS_05 data.
    """
    def construct_group_path():
        group_path = station_path
        for level, name in zip(levels, level_names):
            if level is not None:
                group_path += f'/{level}'
            else:
                break  # Stop adding levels once we encounter the first None
        return group_path

    def recursive_read(group, remaining_levels, utc_values=None):
        """
        Recursively read through the HDF5 file structure to gather data points.
        """
        if len(remaining_levels) == 0:  # Base case: no remaining levels
            print(f"Reading data from group: {group.name}")
            print(f"Available datasets: {list(group.keys())}")
            if 'RS_05' not in group:
                raise KeyError(f"Group {group.name} does not contain 'RS_05' dataset.")
            rs_05 = group['RS_05'][()]
            for u, r in zip(utc_values, rs_05):
                results.append({'utc': u, 'RS_05': r})
        else:
            current_level = remaining_levels[0]
            
            if current_level is not None:  # If we have a specific value, only read that subgroup
                if current_level in group:
                    if len(remaining_levels) == 1 and 'utc' in group:
                        utc_values = group['utc'][()]
                    recursive_read(group[current_level], remaining_levels[1:], utc_values)
                else:
                    raise KeyError(f"Group {group.name} does not contain subgroup {current_level}.")
            else:  # Otherwise, iterate over all subgroups
                for subgroup in group.keys():
                    if len(remaining_levels) == 1 and 'utc' in group:
                        utc_values = group['utc'][()]
                    recursive_read(group[subgroup], remaining_levels[1:], utc_values)

    # Initialize variables
    results = []
    levels = [year, month, day, hour]
    level_names = ['year', 'month', 'day', 'hour']
    station_path = f'/{station_id}'

    # Open the HDF5 file and read data
    with h5py.File(h5_file, 'r') as h5:
        group_path = construct_group_path()
        print(f"Constructed group path: {group_path}")
        if group_path in h5:
            # Ensure utc_values is initialized at the hour level
            utc_values = None
            if hour is not None and 'utc' in h5[group_path]:
                utc_values = h5[group_path]['utc'][()]
            recursive_read(h5[group_path], levels[len(levels):], utc_values)
        else:
            raise ValueError(f"Group path {group_path} not found in HDF5 file.")

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Filter by minute if specified
    if minute is not None:
        minute = int(minute)  # Convert minute to integer
        minute_index = minute // 5  # Calculate the index for the 5-minute interval
        df = df.iloc[minute_index:minute_index+1]  # Select the specific row for the minute

    return df