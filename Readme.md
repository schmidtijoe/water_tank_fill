# Water tank fill volume measurement

Small Project to measure and display the fill volume of a rain water tank.


* Uses a raspberry pi zero with apache webserver
Files under the /var/www/html:
- index.html
- data.json
- long.json

Files somewhere on the pi:
- ultrasonic.py

Additional temperature sensor applied to calculate sound speed in cooler environment.

---------------
Steps:
- For headless setup of pi wifi refer to https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
- Get sensors and if necessary install, see https://tutorials-raspberrypi.de/entfernung-messen-mit-ultraschallsensor-hc-sr04/ for sound module, https://tutorials-raspberrypi.de/raspberry-pi-temperatur-mittels-sensor-messen/ for temperature measurement.
- update and install apache webserver: https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md
- copy files to /var/www/ folder
- check ultrasonic.py to utilize right gpios and to find the .json files in the correct folders
- scheme will be updated
- setup crontab to schedule ultrasound.py to run however often you fancy
- disable wifi powermanagement (idle mode)

Enjoy chart on pis ip in browser :)
❮img src="images/example_webview.png" width="200" ❯
