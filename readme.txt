Calibration

Code to use: Calibration.py (located on the desktop)

How to:
First prepare the calibration samples.
Use at least 4 samples with different pCO2 values.
Decide the order of your samples and the length of each measurement.
Open Calibration.py in Thonny by clicking on it twice.
After the code opens in Thonny click on the green “Run” button.
The terminal of Thonny will show the outputs of the code.
Before the first measurement starts, the following user-inputs have to be given: 
IMPORTANT: place the sensor in the sample before confirming the last input

Number of calibration samples (as integer XX)
Given mbar value (as float X.XX)
Length of this measurement in full minutes (as integer XX)

After putting in these numbers and confirm them with "enter", the code will start the first measurements.
After the given time, the code will show the measured pCO2 value in the Thonny terminal.
For the second sample the code will ask again for the following inputs:
IMPORTANT: place the sensor in the sample before confirming the last input

Given mbar value (as float X.XX)
Length of this measurement in full minutes (as integer XX)

After putting in these numbers and confirm them with "enter", the code will start the next set of measurements.
After the given time, the code will show the measured pCO2 value in the Thonny terminal.
These steps will repeat until the last sample is reached.
After the measurements of the last sample, the input prompt will appear again.
This time the numbers are irrelevant and do not contribute to the calibration.
Please still use the right format: X.XX and XX
Now the code calculates the slope, the intercept and the R^2.
It will print each value in the Thonny terminal.

The calibration file is saved as a csv file in "/media/pi/boot/pCO2_Sensor_Data/CSV-Files/".
The name is in the format "Calibration_YYYY.MM.DD.csv".
The slope, the intercept and R^2 are needed to start the measurement.


Measurement

Codes to use: Measurement.py + dash_usage.py (both located on the desktop)

How to:
Open Measurement.py in Thonny by clicking twice on it.
After the code opens in Thonny click on the green “Run” button.
The terminal of Thonny will show the outputs of the code.
To start the measurement the code needs the following inputs, which are the results of the calibration:

the slope (as float = X.XX)
the intercept (as float = X.XX)
R^2 (as float = X.XX)

After putting in these numbers and confirm them with "enter", the code will start the measurements.
Every 4 days the code will create a new csv file and the visualization shows 4 days.
To visualize the measurements open the terminal of the raspberry pi.
Use autofill by pressing the "up" button on your keyboard or type "XXX" directly in the command line and press "enter" to confirm.
After this, there should appear some text in the terminal.
This text tells where the visualization is shown  (127.0.0.1:8050) and if it is stable.
The visualization updates itself, for every time a line with "import data" is printed in the terminal.

To see the visualization open the web browser and go to "http://127.0.0.1:8050/" by using the bookmark or tipping it in the address line.
The measurement file is saved as a csv file in "/media/pi/boot/pCO2_Sensor_Data/CSV-Files/".
The name is in the format "YYYY.MM.DD.csv", it relates to the start of the 4-day-measurement.

IMPORTANT: The visualization needs to be restarted after 4 days.
For this the terminal window has to be closed.
Use autofill by pressing the "up" button on your keyboard or type "XXX" directly in the command line and press "enter" to confirm.
After this, there should appear some text in the terminal.
This text tells where the visualization is shown  (127.0.0.1:8050) and if it is stable.
The visualization updates itself, for every time a line with "import data" is printed in the terminal.

To see the visualization open the web browser and go to "http://127.0.0.1:8050/" by using the bookmark or tipping it in the address line.