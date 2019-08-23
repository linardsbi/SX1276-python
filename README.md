# SX1276-python
Rough API for the SX1276 chip that runs on Python
## Serial error
*Setting up serial for `Orange PI` on `Armbian`*

1. Find `armbianEnv.txt` in /boot/;
2. Add `overlays=uart1` to the file and reboot;
   If adding more than one serial bus, separate names with a comma
   eg. "overlays=uart1,uart2,uart3" and so on
3. Create an empty directory:
   `mkdir /sys/kernel/config/device-tree/overlays/uart1`;
4. Run `cat /boot/dtb/overlay/sun8i-h3-uart1.dtbo > /sys/kernel/config/device-tree/overlays/uart1/dtbo`;
5. Run `cat /dev/ttyS1` (depending on the serial port you specified; for uart1 it's ttyS1)
   Type anything to see if you get a response back.

If it still doesn't work, check [this](https://forum.armbian.com/topic/3557-orangepi-pc-gpio-uart-and-arduino/) or [this](https://forum.armbian.com/topic/1524-orange-pi-one-how-to-enable-uart/) thread on the Armbian forum
