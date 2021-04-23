#!/bin/bash

PASS=scan

# Install all the needed stuff
export DEBIAN_FRONTEND=noninteractive
apt-get -y update
apt-get -y upgrade
apt-get -y install \
	vim \
	git \
	screen \
       	samba \
	samba-common-bin \
	zsh \
	xserver-xorg \
	xserver-xorg-video-all \
	xserver-xorg-input-all \
	xserver-xorg-core \
	xinit \
	x11-xserver-utils \
	chromium-browser \
	wget \
	python3-venv \
	tesseract-ocr \
	tesseract-ocr-deu \
	ocrmypdf

cat <<EOT >> /etc/dhcpcd.conf
interface wlan0
static ip_address=10.0.0.32/24
static routers=10.0.0.1
static domain_name_servers=1.2.3.4
EOT

# Choosing right display orientation
### echo lcd_rotate=2 >> /boot/config.txt

echo "pi:$PASS" | chpasswd
hostnamectl set-hostname snet-scanbot

cat <<EOT > /etc/hosts
127.0.0.1	localhost
::1		localhost ip6-localhost ip6-loopback
ff02::1		ip6-allnodes
ff02::2		ip6-allrouters
127.0.1.1		snet-scanbot
EOT

# Creating the scan user
sudo useradd scan --password $PASS --create-home
runuser -u scan -- mkdir /home/scan/scantarget
sudo chmod -R o+w /home/scan


# Creating Samba stuff
echo -ne "$PASS\n$PASS\n" | smbpasswd -a -s scan

cat <<EOT > /etc/samba/smb.conf
[global]
   workgroup = WORKGROUP
   log file = /var/log/samba/log.%m
   max log size = 1000
   logging = file
   panic action = /usr/share/samba/panic-action %d
   server role = standalone server
   obey pam restrictions = yes
   unix password sync = yes
   passwd program = /usr/bin/passwd %u
   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .
   pam password change = yes
   map to guest = bad user
[scantarget]
   path = /home/scan/scantarget
   writeable=Yes
   create mask=0777
   directory mask=0777
   public=no
EOT

cat <<EOT > /home/pi/.xinitrc
#!/bin/sh
# ~/.xinitrc
xset -dpms
xset s off
xset s noblank

xscreensaver &
unclutter -idle 0 &
chromium-browser www.heise.de  \
    --start-fullscreen --kiosk --incognito --noerrdialogs --lang=en-US,en \
    --disable-translate --no-first-run --fast --fast-start --window-position=0,0 --window-size=800,600 \
    --disable-infobars --disable-features=TranslateUI \
    --disk-cache-dir=/dev/null --password-store=basic
EOT

cat <<EOT > /home/pi/.xscreensaver
timeout: 0:01:00
lock: False
splash: False
dpmsEnabled: True
dpmsQuickOff: True
mode: blank
EOT


#enable autologin
#mv  /etc/lightdm/lightdm.conf > /etc/lightdm/lightdm.conf.old
#sed '/autologin-user=/ a autologin-user=pi' /etc/lightdm/lightdm.conf.old > /etc/lightdm/lightdm.conf

# install scanbot software
git clone https://github.com/sommeru/scanbot.git
cd scanbot
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip


pip install -r requirements.txt

