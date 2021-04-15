# packages needed:
- ocrmypdf
- tesseract
- tesseract-lang

# Raspberry preparations
- create file "ssh" in boot partition
- create file "wpa_supplicant.conf" in boot partition

country=DE
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
scan_ssid=1
ssid="your_wifi_ssid"
psk="your_wifi_password"
}
