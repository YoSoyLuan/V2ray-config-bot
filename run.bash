#!/bin/bash
sudo apt-get install wget
wget https://github.com/luan-03/V2ray-Bot/archive/refs/heads/main.zip
sudo apt-get install unzip
unzip main.zip
sleep 2
sudo apt-get install python3-pip
pip3 install -r V2ray-Bot-main/requirements.txt
echo "Edita el archivo de configuracion"
sleep 2
nano V2ray-Bot-main/config.py
echo "Now Run Bot in background"
sleep 2
(cd V2ray-Bot-main && python3 main.py &)
(cd V2ray-bot-main && python3 update.py &)
echo "Terminado"
exit

