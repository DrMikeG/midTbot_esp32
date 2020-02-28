# MidTBot ESP32

![](https://github.com/bdring/midTbot_esp32/blob/master/Docs/images/20190721_092227.jpg)

The MidTBot is a small and simple little pen plotter. All of the custom parts are 3D printed. The rest of the parts are low cost and easy to get.

The controller uses an ESP32 running Grbl_ESP32 firmware. It can be controlled via USB, Bluetooth or Wifi. You can simply upload gcode files to the unboard SD card and print.


The machine is controlled by a unique H-bot configuration, that uses a single belt. Two small stepper motors drive that belt in a special way to move in the X/Y plane. The pen is lifted by a hobby servo using a very simple and accurate mechanism.

[Here is a link to a video of the plotter in action.](https://www.youtube.com/watch?v=jiwWCrCfXrY)

The project is open source (Creative commons 4.0 Attribution - Share Alike) and all the files are in this Githob repo. Assembly instructions [are here](https://github.com/bdring/midTbot_esp32/wiki/Assembly-Instructions). If you have questions, please ask them by opening an issue in this repo.

### Check it out on GrabCad

Click on image for interactive viewer in browser.

[![GrabCAD](https://github.com/bdring/midTbot_esp32/blob/master/Docs/images/grabcad_model.png)](https://workbench.grabcad.com/workbench/projects/gcj3zJAQexD3ve_8KkwymatyKXhCWnRs8TB5U1ojGxl3s4#/space/gcP-lh4vchvUQ6FbfQFYGKVWLmIdnV8aq2IyxzoECw8woR/link/1918044)

### Kits

There currently are no full kits for sale. [Controller kits are available on Tindie](https://www.tindie.com/products/33366583/midtbot-esp32-v1-controller-kit/).

### Donation

This project represents a lot of work. Please consider a safe, secure and highly appreciated donation via the PayPal link below.

[![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=TKNJ9Z775VXB2)

## 2020-02-21 ##

I've got the latest arduino ide updated
I've added the esp32 board manager as described here https://github.com/espressif/arduino-esp32/blob/master/docs/arduino-ide/boards_manager.md

I've not pulled the development repo of https://github.com/espressif/arduino-esp32 - hopefully I don't need to do that?

I've copied the libraries from grbl\libs as described here: https://github.com/bdring/Grbl_Esp32/wiki/Compiling-the-firmware
/Volumes/ExtData03_2TB/Users/mike/Documents/Arduino/libraries

I've set the board settings in Ardino IDE as described here: https://github.com/bdring/Grbl_Esp32/wiki/Compiling-the-firmware

I've opened /Volumes/ExtData03_2TB/Users/mike/arduino/Grbl_Esp32/Grbl_Esp32/Grbl_Esp32.ino and I'm  trying to compile

Compiled unchanged...

The file "cpu_map.h" contains pin maps for several common setups. The master configuration file "config.h" selects one of those pin maps via a "#define" line near the top of that file.

Trying to program CPU_MAP_TEST_DRIVE onto actual board...

Compiled board with test_drive and that seemed to work.
Can't catch IP address on serial, but did find wifi GRBL_ESP, with password 12345678.
(See https://github.com/bdring/Grbl_Esp32/wiki/ESP3D-Web-UI-for-Grbl_ESP32)

You can also get them by sending $I on a serial terminal.

Changed config.h to have:
#define CPU_MAP_MIDTBOT // these are defined in cpu_map.h
recompiled and flashed to board.

Connected to the wifi network. Uploaded index.html.gz from this repo.

Putting esp board onto controller board
(Micro usb slot points off the edge of the board)

Plugged in stepper motor nearest boards (X?) Used UI to Jog X - it moves...
Connected second stepper - they both move when you job X/Y - remember it's a H-bot.

Connected up the servo. Jogged Z. That moves ok too.

Need to remember to adjust the stepper power to get the right cooking temp....

# 28th Feb 2020 #

Final screws arrived so attached steppers to the main board.
Threaded belt. Booted.

Need to follow instructions for attaching servo horn.

## Setting up the motors ##


Set the trimpot to minimum to start with, by turning the trimpot fully anti-clockwise. Turn clockwise until the motors are not skipping steps at your target speed and load.

https://github.com/bdring/midTbot_esp32/wiki/Setting-Up-the-Motors

https://github.com/bdring/midTbot_esp32/wiki/Setting-Up-the-Motors#overview-1

Set $rst=$ to reset all of the default Grbl settings.
Check the status by sending the ? character.
It should report that there is an alarm. This is because you have not homed yet.
Send $X to clear the alarm

Send $X to clear the alarm. You then need to send some small test moves to check the direction. 
Send G91 to put it in (incremental distance mode). Next send G0X2 to move the X axis 2mm to the right. Send G0Y2 to move the Y axis 2mm back. If either of these go the wrong direction you have to rotate one or more of the motor connectors 180 degrees.


Send $H to home the machine.

I think the wiring was correct all along - I just had one or more of the stepper drivers dialled down too low for homing work.
I cleared the alarm with $X, turned both trim pots a fraction clock-wise and rehomed in Y and X. Seemed fine so powered down for tonight.