# DJ Bot!

This needs to be copied onto a Raspberry Pi.
For now it's woefully undocumented, sorry!

After copying the files over, 

	sudo cp botapp.service /lib/systemd/system/
	sudo chmod 644 /lib/systemd/system/botapp.service
	sudo systemctl daemon-reload
	sudo systemctl enable botapp.service
