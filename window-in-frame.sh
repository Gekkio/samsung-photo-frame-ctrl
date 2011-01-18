#!/bin/sh

if [ `which notify-send` ]; then
  notify-send -u low -t 3000 "Choose which window you'd like to show in the photo frame"
fi

WINDOW_ID=`xwininfo -int |grep "xwininfo: Window id" | awk '{ print $4 }'`
GEOMETRY="800x480"

while true; do
  import -window $WINDOW_ID -strip -resize $GEOMETRY - | montage - -background black -geometry $GEOMETRY jpeg:- | ./frame-ctrl.py > /dev/null
  if [ "$?" != "0" ]; then
    exit $?
  fi
done
