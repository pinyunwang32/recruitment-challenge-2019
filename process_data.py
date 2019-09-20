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
import numpy as np
import csv
import matplotlib.pyplot as plt
from lib import process_bom_grid_file as pf
import statistics 
import pandas
import csv
import requests
import urllib.request


def read_weather_station_data():
   
    with open('weather_station_20190601-20190731.csv') as csvfile:
        readCSV = pandas.read_csv(csvfile,header=None)
        dateTime = []
        solRads = []
        solRadHourly = []
        mjToW = 277.77777777778
        
        for i in range(1,17569):
#            print(readCSV.iloc[i])]
            data = readCSV.iloc[i]
            dateTime.append(data[0])
            solRads.append(float(data[5]))
    
    
    # Align to a hourly timestamp
    for i in range(1,721):
        solRadHourly.append(statistics.mean(solRads[(i-1)*12+1:(i-1)*12+1+11]))
        
        
def read_grid_file():
   
    solarOfTheDay = []
    solarIrraHourly = []
    
    for i in range(1,31):
        if i < 10:
            string = '0'+str(i)
        else:
            string = str(i)
            
        print('Reading grid file: '+string)
        
        grid_file_name = 'BOM_solar_grid_data_201906/201906'+string+'201906'+string+'.grid'
        data_by_location, start_date, end_date = pf.get_solar_exposure_data_from_grid_file(grid_file_name)
#        print(data_by_location['-27.45']['153.05'])
        solarOfTheDay.append(data_by_location['-27.45']['153.05'])
        solarDistribution = data_by_location['-27.45']['153.05']/24
#        print(solarDistribution)
        solarDistribution_w = solarDistribution*mjToW
        
        # Align to a hourly timestamp
        for j in range(1,25):
            solarIrraHourly.append(solarDistribution_w)
            
        
def plot_graph(x,y,title,xlabel,ylabel,colour):
               
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.plot(x,y, colour)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    

def write_csv():
    
    j = 1
    csvData = [['Time', 'Solar Radiation', 'Solar Irradiation']]
    with open('data.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
        for i in range(1,720):
            writer.writerow([str(j)+'/6/2019 '+str((i-1)%24)+':00:00',solRadHourly[i],solarIrraHourly[i]])
            if i%24==0:
                j = j+1
    csvFile.close()

def write_output_to_endpoint():
    
    with open('data.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            record = {'utc_timestamp':str(row[0]),'solar_ws': str(row[1]), 'solar_bom': str(row[2])}
#            print(record)
            
    data = {'candidate':'pinyunwang32','version':'test', 'records':str(record)}
    response = requests.post('https://qs3w5fq4oi.execute-api.ap-southeast-2.amazonaws.com/dev/ping', data) 
    
    print(response.status_code) 
    print(response.text) 
    
    
def download_bom():
    for i in range(1,31):
        if i < 10:
            string = '0'+str(i)
        else:
            string = str(i)
        print('Download BOM file '+string)
        url ='http://www.bom.gov.au/web03/ncc/www/awap/solar/solarave/daily/grid/0.05/history/nat/201907'+string+'201907'+string+'.grid.Z'
        r = requests.get(url, allow_redirects=True)
        with open('BOM/'+'201907'+string+'201907'+string+'.grid.Z', 'wb') as f:
            f.write(r.content)


if __name__ == '__main__':
    
    # Read weather station solar data CSV (first command line argument)
    print('Reading weather station solar data...\n')
    read_weather_station_data()
    print('Ploting weather station solar data...\n')
    plot_graph(list(range(1,721,1)),solRadHourly,'Solar Radiation in June (hourly)','Time (Hour)','W/m2','r')
        
    # Read daily total data (from grid files / or directly from BOM?)
    print('Reading daily total data from grid files...\n')
    read_grid_file()
    print('Ploting daily total data from grid files...\n')
    plot_graph(list(range(1,721,1)),solarIrraHourly,'Solar Irradiation in June (hourly)','Time (Hour)','W/m2','b')   

    # Write output to CSV
    print('Exporting CSV file...\n')
    write_csv()
    
    # Visualise results
    print('Ploting the comparision graph...\n')
    fig, ax = plt.subplots()
    ax.set_title('Comparision between Solar Radiation and Solar Irradiation in June (hourly)')
    plt.plot(x, solRadHourly, 'r') 
    plt.plot(x, solarIrraHourly, 'b')
    plt.show()

    # Additional Task: Write output to an endpoint
    print('Writing output to an endpoint...\n')
    write_output_to_endpoint()
    
    #Extra BOM data
    print('Downloading BOM data...\n')
    download_bom()
    
    # Additional Task: detect anomalies
    # anomaly_detection_results = model.detect_anomalies([], [], [])
