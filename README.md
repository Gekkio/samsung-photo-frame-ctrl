Samsung photo frame control
=================

A small Python application for controlling Samsung photo frames.

Based on the work of [Grace Woo & others](http://web.media.mit.edu/~gracewoo/stuff/picframe/). One large difference is that my application adds an extra control message that prevents the photo frame from exiting mini display mode.

Features
--------

* If a photo frame is in mass storage mode, the program will change it into mini display mode.
* If a photo frame is in mini display mode, the program will send the jpeg that was specified as the program argument to the photo frame. *The JPEG must be prescaled to the exactly correct size!*
* window-in-frame.sh which shows a user selected application window in the photo frame (needs Imagemagick!)

Supported photo frames
----------------------

* SPF-107H (not tested)
* SPF-87H
* (In theory) Other similar Samsung photo frames should work once their product IDs are added into the code

Dependencies
------------

* [pyusb 1.0](http://sourceforge.net/apps/mediawiki/pyusb) (This is an alpha quality library so it is *not* the one usually packaged in linux distributions. For example, the normal Ubuntu version of python-usb won't work!). **Update:** [Experimental Ubuntu PPA packages for Lucid/Maverick/Natty](http://launchpad.net/~gekkio/+archive/pyusb)

Usage
-----

### Show JPEG image with the exactly correct size in photo frame

`sudo ./frame-ctrl.py my_correctly_scaled_image.jpg`

or

`cat my_correctly_scaled_image.jpg | sudo ./frame-ctrl.py`

### Automatically scale an image and show it in the photo frame (needs Imagemagick). _Replace 800x480 with the correct resolution for your device_

`cat some_image_supported_by_imagemagick | convert - -resize 800x480 - | montage - -background black -geometry 800x480 jpeg:- | sudo ./frame-ctrl.py`

### Show an application window in photo frame (needs Imagemagick). _Replace 800x480 in window-in-frame.sh with the correct resolution for your device_

`sudo ./window-in-frame.sh` and click on an application window to select it

FAQ
---

### Can I use my photo frame as a mini monitor in Linux?

Nope. In theory it's possible but it would require an X driver that would repeatedly compress frames into JPEG format and send them to the photo frame. This is exactly what the Frame Manager software does in Windows.

### Why do I need to use sudo?

libusb needs direct access to the usb device and unless you have set up permissions explicitly, you won't have access to the raw usb devices.
