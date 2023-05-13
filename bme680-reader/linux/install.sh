sudo cp bme680-reader.service /etc/systemd/system/
systemctl status bme680-reader.service
sudo systemctl enable bme680-reader.service
sudo systemctl start bme680-reader.service