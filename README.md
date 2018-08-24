# Mobileye Viewer
A tool made with Flask and Chart.js to visualise data from both a Mobileye camera and a driver control unit for use in self-driving cars. The Flask server reads in CAN data by reading the output from the `candump` with the `subprocess` module. It then parses the relevant bytes, and sends a json object via HTTP server-sent events to all connected clients. The webpage displays a graph of the left and right lane boundaries, as well as the speed and heading angle of the car. 

## Usage
This tool was intended to run on embedded hardware with a dedicated CAN port. Make sure that your board has the correct drivers before you decide to run it.  
If your computer does not have Flask, run
```bash
    pip install Flask
```
The server will run on both python 2 and python 3, so the version of python you install Flask on is irrelevant. Clone this respository with
```bash
    git clone https://github.com/falafel72/mobileye_viewer
```
and run it with
```bash
    python app.py
```
Any computer connected to the same network should be able to view the webpage at the url `server_ip_address:5000`.

## Potential Improvements
Ideally CAN data would be read using python's `can` library or Kvaser's `canlib`, but I was unable to install either of these on the board I was using. Moving the CAN receiving logic to python would eliminate the need to read every incoming data packet, making the program more efficient. More information could also be displayed, such as the locations of cars or other obstacles in front of the car. A more realistic map would be useful for this purpose, requiring a migration away from Chart.js to a more specialised 3d rendering tool.  
