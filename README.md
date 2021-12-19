# RPi-webcom-collector #

collect webcams in local area

## Installation ##
install all needed packages to prepare the software environtent of your Raspberry Pi:
```bash
sudo apt-get update && sudo apt-get upgrade && sudo apt-get install python3-pip git ffmpeg
sudo pip3 install getmac
```
and this tool itself:
```bash
cd /opt
sudo git clone https://github.com/Starwhooper/RPi-webcam-collector
sudo mkdir /var/www/html/camimages
```

## First configurtion ##
```bash
sudo chmod +x /opt/RPi-webcam-collector/collect.py
sudo cp /opt/RPi-webcam-collector/config.json.example /opt/RPi-webcam-collector/config.json
sudo nano /opt/RPi-webcam-collector/config.json
```


## Start ##
Its also able to add it in cron via ```sudo crontab -e```, it prevent doublicate starts
```bash
/opt/RPi-webcam-collector
```

## Update ##
If you already use it, feel free to update with
```bash
cd /opt/RPi-webcam-collector
sudo git pull origin main
```