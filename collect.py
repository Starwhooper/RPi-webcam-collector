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
import sys
import json

def camoutput(cammodell,mac,camlink,ip,imgsrc,column):
 output = ''
 if column == 1:
  output += '<tr><td>'
 elif column == 2:
  output += '<td>'
 elif column == 3:
  output += '<td>'

 output += cammodell + ' ' + mac[9:] + ' <a href="' + camlink + '">IP: ' + ip + '<img src="' + imgsrc + '"></a>'

 if column == 1:
  output += '</td>'
 elif column == 2:
  output += '</td>'
 elif column == 2:
  output += '</td></tr>'

 return(output)

parent_dir = os.path.split(os.path.abspath(__file__))[0]
column = 1


##### import config.json
try:
 with open(parent_dir + '/config.json','r') as file:
  cf = json.loads(file.read())
except:
 sys.exit('exit: The configuration file ' + os.path.split(os.path.abspath(__file__))[0] + '/config.json does not exist or has incorrect content. Please rename the file config.json.example to config.json and change the content as required ')

ip = str((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
ipareaparts = ip.split('.')

htmlstring = '<!DOCTYPE HTML>\n<!--get awesomefonts from here: https://fontawesome.com/v5.15/icons/cloud-sun?style=solid //-->\n<html>\n<head>\n<meta charset="utf-8"/>\n<meta http-equiv="refresh" content="60">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">\n'
try:
 htmlstring += '<style>\n'
 htmlstring += open(parent_dir + '/format.css','r').read()
 htmlstring += '</style>\n'
except: 
 htmlstring += '<!-- no format.css found //-->\n'
 htmlstring += '</style>\n'

htmlstring += '</head><body>'
htmlstring += '<h1><i class="fas fa-video" style="color:crimson"></i> Webcam</h1><p class="small">Date: ' + datetime.date.today().strftime('%a')[:2] + datetime.date.today().strftime(', %d. %b.\'%y') +  ' Time: ' + time.strftime('%H:%M:%S', time.localtime()) + '</h1>\n'

htmlstring += '<table>'

for ipchangepart in range(0,255):
 ip = ipareaparts[0] + '.' + ipareaparts[1] + '.' + ipareaparts[2] + '.' + str(ipchangepart)
 mac = get_mac_address(ip=ip)
 if mac != "00:00:00:00:00:00":
  try: user = cf['camdevices'][mac]['user']
  except: user = ''
  try: password = cf['camdevices'][mac]['password']
  except: password = ''
  if len(str(mac)) == 17:
   if str(mac[:8]) == "f0:00:00":
    videoin = 'rtsp://' + ip + '/stream1'
    videoout = '/var/www/html/camimages/' + mac.replace(':', '') + '-output.jpg'
    os.system('ffmpeg -hide_banner -loglevel error -y -i ' + videoin + ' -ss 5 -vf scale=600:-1 -frames:v 1 ' + videoout)
    cammodell = 'SV3C Camera (A-Series)'
    camlink = 'http://' + ip
    imgsrc = 'camimages/' + mac.replace(':', '') + '-output.jpg'
    htmlstring += camoutput(cammodell,mac,camlink,ip,imgsrc,column)
    column = column + 1
   elif str(mac[:8]) == "00:e0:59":
    videoin = 'rtsp://' + ip + ':554/12'
    videoout = '/var/www/html/camimages/' + mac.replace(':', '') + '-output.jpg'
    os.system('ffmpeg -hide_banner -loglevel error -y -i ' + videoin + ' -ss 5 -vf scale=600:-1 -frames:v 1 ' + videoout)
    cammodell = 'SV3C Camera (HX-Series)'
    camlink = 'http://' + ip + '/web/admin.html'
    imgsrc = 'camimages/' + mac.replace(':', '') + '-output.jpg'
    htmlstring += camoutput(cammodell,mac,camlink,ip,imgsrc,column)
    column = column + 1
   elif str(mac[:8]) == "e0:b9:4d":
    cammodell = 'Digoo'
    camlink = 'http://' + ip + ':81/videostream.cgi?loginuse=' + user + '&loginpas=' + password
    imgsrc = 'http://' + ip + ':81/videostream.cgi?loginuse=' + user + '&loginpas=' + password
    htmlstring += camoutput(cammodell,mac,camlink,ip,imgsrc,column)
    column = column + 1
   elif str(mac[:8]) == "34:94:54":
    cammodell = 'EPS32-CAM'
    camlink = 'http://' + ip + '/mjpeg/1'
    imgsrc = 'http://' + ip + '/mjpeg/1'
    htmlstring += camoutput(cammodell,mac,camlink,ip,imgsrc,column)
    column = column + 1
   else:
    print('non cams found: ' + str(mac) + ' ' + str(ip))
   
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
