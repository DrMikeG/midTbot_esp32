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

For my colour wires, the correct wiring colours away from the ESP board are RGBY/GPBW
Wrong! Today the correct colours are: RGBY/WBPG

## Setting the X,Y 0,0 point.##
Homing does not set a 0,0 point. You need to tell it where that is. 
Home is min(X),max(Y) (top left hand corner)
Typically you would want jog to the lower left point and the set the 0,0 there.
min(X),min(Y) (lower left hand corner)
After homing move the down in negative Y. Be sure you don't hit the limit of travel. If you do, re-home and try again. 
Once there, set the 0,0. There are also zeroing buttons near the jog panel in the GUI.

## Pen Servo Setup ##

// Required
$rst=#
$3=4 (reverse the Z direction) (Has this reversed X and Y?!)
$102=90 (short pen lower stroke)
G10L2P0Z-5 (Avoid grounding pen at home.)

G0Z5 is pen up.

Clear the homing alarm by sending $X over the serial port.
Next send $rst=#. This will reset any machine offsets that might be in memory.
Send G0Z5 the servo should move to one end of the travel.
You can see the other end of the travel by sending G0Z0.
Send G0Z5 again to move to the pen up position. The servo should be rotating clockwise to lift the pen and counterclockwise to lower it. 

I need to send $3=4 to reverse the Z direction
(Not all servos travel the same way. If yours is going the wrong way, send $3=4 to reverse the Z direction.)

With the machine at Z5, mount the servo horn in a position that holds up the pen lift part. You want it to be holding the pen up close to the max height, but there should be a little travel left.


Changing $102 (adjusts Z0) From default (100). Sending $102=90 add 10% towards Z5 (up))

Used G0Z0 to install pen

## Home and first draw ##
Using WebUI 

Jogged as far in -Y as I dare.
Not sure I hit the zeroing button in the UI? (It dropped the pen) 
G10L20P0X0Y0 

I've drawn to test drawings of midthead.gcode (both seem to finish with a long random line with the pend down?!)

Trying to debug random line on completion? 
https://ncviewer.com/ shows this isn't a g-line. It could either be the home command or part of the firmware?

Also homed X and Y independently from Z? This stopped the pen dropping.
Click the X and Y wheel cross not the combine X/Y/Z one.

## Process ##
[Position bad paper]
Power on
Connect to wifi (12345678)
$X (clear alarm)
G0Z0 (pen down)
[Fit pen]
G0Z5 (pen up)
G10L2P0Z-5 (Avoid grounding pen at home.)
[Position good paper]
Click home Y
Click home X
Move -Y by about -1000 to move to bottom left corner of range
Click zero X
Click zero Y
[Need to figure out drawing Csys from 0,0 process]
[Execute GCode to draw picture]

if gcode contains G28 you may wish to remove it? Just end on pen up!

## How to make GCode ##
https://youtu.be/bbe56S_O-uI

Open Inkscape
> Document Properties
>> Default UNITS mm
>> Units mm
>> Width 180 (plotter bed size)
>> Height 220 

Import image into inkscape
Scale
Goto path tab
> Trace bitmap
>> Update
>> Ok
>> Close
Delete image (keep path)
Select object, on path menu click on object to path
>> Path tab
>>> Dynamic offset


/Volumes/ExtData03_2TB/Users/mik

## Added inkscape MakerBot Unicorn G-Code extension ##

Test params:
50/30/150/150/1500/1000/0/0 


https://shopcraftables.com/free-svg-cut-files/?sort=featured&page=6