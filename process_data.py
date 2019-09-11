"""
Comand for comparing two sources of solar radiance data

Run from the command line like so
```
    > python process_data.py INPUT_CSV_FILE POSTCODE --output_file=OUTPUT_CSV_FILE --output_endpoint=OUTPUT_API_URL
```

Inputs:
 * CSV data from a weather station (first command line argument)

Outputs:
 * CSV to write results to (second command line argument)
 * endpoint for posting JSON results (third command line argument)

"""

from lib import model


if __name__ == '__main__':
    # Read weather station solar data CSV (first command line argument)
    print('Reading weather station solar data...')

    # Read daily total data (from grid files / or directly from BOM?)

    # Align to a hourly timestamp

    # Write output to CSV

    # Visualise results

    # Additional Task: Write output to an endpoint

    # Additional Task: detect anomalies
    # anomaly_detection_results = model.detect_anomalies([], [], [])
