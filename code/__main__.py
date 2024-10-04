# In rainquest/__main__.py

import argparse
from .rain_reader import read_rain_data

def main():
    parser = argparse.ArgumentParser(description="Read rain data from HDF5 files.")
    parser.add_argument("h5_file", type=str, help="Path to the HDF5 file.")
    parser.add_argument("station_id", type=str, help="Station ID to read data for.")
    parser.add_argument("--year", type=str, help="Year to filter data.")
    parser.add_argument("--month", type=str, help="Month to filter data.")
    parser.add_argument("--day", type=str, help="Day to filter data.")
    parser.add_argument("--hour", type=str, help="Hour to filter data.")
    parser.add_argument("--minute", type=str, help="Minute to filter data.")
    
    args = parser.parse_args()
    
    df = read_rain_data(
        args.h5_file,
        args.station_id,
        year=args.year,
        month=args.month,
        day=args.day,
        hour=args.hour,
        minute=args.minute
    )
    
    print(df)

if __name__ == "__main__":
    main()

