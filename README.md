# RPI-webcam.collector
Detect Webcams by itself and publish it to website

## install ##
install all needed packages to prepare the software environtent of your Raspberry Pi:
```bash
sudo apt-get update && sudo apt-get upgrade && sudo apt-get install python3-pip git ffmpeg
sudo pip3 install getmac
```
and this tool itself:
```bash
cd /opt
sudo git clone https://github.com/Starwhooper/RPi-webcam-collector
sudo chmod +x /opt/RPi-webcam-collector/collect.py
sudo touch /var/www/html/webcam.html && sudo chmod 777 /var/www/html/webcam.html
```

## Update ##
If you already use it, feel free to update with
```bash
cd /opt/RPi-webcam-collector/
sudo git pull origin main
```

## start ##
add to cronjob
```bash
sudo crontab -e
*/5 * * * * /opt/RPi-webcam-collector/collect.py
```
