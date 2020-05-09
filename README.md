# IoT Data Simulator

Graphical User Interface application that allows users to simulate a real-world scenario where IoT big data is gathered from 1000 user homes. The user then has the ability to perform data visualization, and save the data generated into a file.

## Installation

Before running this application you need to have installed several packages along with python3. To install the required dependencies run the following commands in your Terminal/Command Line Prompt:
```bash
pip install wxPython
pip install faker
pip install pandas
pip install matplotlib
```
Once done with installing the required dependencies, to run this application open a Terminal/Command Line Prompt window, navigate to the directory where the file app.py is found, and do:
```bash
python app.py
```

## Usage
Once the application is opened, the user will need to generate IoT data by clicking "File", and then clicking "Generate IoT".
After data has been generated, the user can:

* Save data as a JSON file.
* Save data as a CSV file.
* Compute common statistical values for the sensor data gathered.
* Plot four different histograms of the outside temperature sampled every 6 hours.
* Plot a line graph of the outside temperature vs the room temperature.
* Plot four histograms of room and outside temperature and humidity for all 1000 user entries.
