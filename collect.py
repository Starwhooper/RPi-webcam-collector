#!/usr/bin/python3
# Creator: Thiemo Schuff, thiemo@schuff.eu
# Source: https://github.com/Starwhooper/RPi-webcam-collector

try: from getmac import get_mac_address
except:
	print('python3 modul getmac is missed')
	print('please do follow command to get it')
	print(' ')
	print('sudo apt-get install python3-pip && sudo pip3 install getmac')
	exit()

import urllib.request
import socket
import datetime
import time
import os

ip = str((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
ipareaparts = ip.split('.')

htmlstring = '<!DOCTYPE HTML>\n<!--get awesomefonts from here: https://fontawesome.com/v5.15/icons/cloud-sun?style=solid //-->\n<html>\n<head>\n<meta charset="utf-8"/>\n<meta http-equiv="refresh" content="5">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">\n'
htmlstring += '<style>\n'
htmlstring += 'h1 {font-size: 3.0rem; background: lightgreen;}\n'
htmlstring += 'h2 {font-size: 2.0rem;}\n'
htmlstring += 'a:link, a:visited, a:hover, a:active {  background-color: lightgray;  color: white;/*  padding: 14px 25px;*/  text-align: center;  text-decoration: none;  display: inline-block;  width: 100%;}\n'
htmlstring += 'html {	font-family: Arial;	display: inline-block;	margin: 0px auto;	text-align: center;}\n'
htmlstring += 'p {	font-size: 3.0rem;}\n'
htmlstring += 'p.small {	font-size: 1.0rem;}\n'
htmlstring += 'table{  margin-left: auto;  margin-right: auto;  border: 1px solid black;  border-collapse: collapse;}\n'
htmlstring += 'td,th,tr {    border: 1px solid black;    border-collapse: collapse;    font-size: 0.8rem;}\n'
htmlstring += 'img {    max-width: 100%;    height: auto;}\n'
htmlstring += '</style>\n'
htmlstring += '</head><body>'
htmlstring += '<h1><i class="fas fa-video" style="color:crimson"></i> Webcam</h1><p class="small">Date:' + datetime.date.today().strftime('%a')[:2] + datetime.date.today().strftime(', %d. %b.\'%y') +  'Time:' + time.strftime('%H:%M:%S', time.localtime()) + '</h1>\n'
htmlstring += '<table>'

for ipchangepart in range(0,255):
	ip = ipareaparts[0] + '.' + ipareaparts[1] + '.' + ipareaparts[2] + '.' + str(ipchangepart)
	mac = get_mac_address(ip=ip)
	if mac != "00:00:00:00:00:00":
		if len(str(mac)) == 17:
			if str(mac[:8]) == "f0:00:00":
				htmlstring += '<tr><td>SV3C Camera (A-Series) ' + mac[9:] + '<br/>IP: <a href="http://' + ip + '">IP: ' + ip + '</a></td></tr>\n'
				videoin = 'rtsp://' + ip + '/stream1'
				videoout = '/var/www/html/camimages/' + mac.replace(':', '') + '-output.jpg'
				os.system('ffmpeg -y -i ' + videoin + ' -ss 5 -vf scale=600:-1 -frames:v 1 ' + videoout)
				htmlstring += '<tr><td><img src="camimages/' + mac.replace(':', '') + '-output.jpg"></td></tr>\n'

			if str(mac[:8]) == "00:e0:59":
				htmlstring += '<tr><td>SV3C Camera (HX-Series) ' + mac[9:] + '<br/><a href="http://' + ip + '/web/admin.html">IP: ' + ip + '</a></td></tr>\n'
				videoin = 'rtsp://' + ip + ':554/12'
				videoout = '/var/www/html/camimages/' + mac.replace(':', '') + '-output.jpg'
				os.system('ffmpeg -y -i ' + videoin + ' -ss 5 -vf scale=600:-1 -frames:v 1 ' + videoout)
				htmlstring += '<tr><td><img src="camimages/' + mac.replace(':', '') + '-output.jpg"></td></tr>\n'

htmlstring += '</table>'
htmlstring += "</body>\n"
htmlstring += "</html>\n"

try: htmlfile = open('/var/www/html/webcam.html','w')
except:
	print('file /var/www/html/webcam.html not aviable of permission missed')
	print('please do follow command to get it:')
	print('sudo touch /var/www/html/webcam.html && sudo chmod 777 /var/www/html/webcam.html')
htmlfile.write(htmlstring)
htmlfile.close
