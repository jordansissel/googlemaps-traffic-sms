#!/bin/sh

found=0
for tries in 1 2 3 4 5 6 7; do
  DISPLAY=`perl -e 'srand(time()); print int(rand() * 1000)'`
  export DISPLAY
  if [ ! -e "/tmp/.X11-unix/X$DISPLAY" ]; then
    DISPLAY=":$DISPLAY"
    echo $DISPLAY
    startx -- /usr/local/bin/Xvfb $DISPLAY -screen 0 800x600x24 > /dev/null 2>&1 &
    found=1
    break
  fi
done

sleep 3600
if [ "$found" -eq "0" ]; then
  echo "Tried to find an unused X server, but none were found"
  exit 1
fi


title="traffic $$"
echo "Title: $title"
xulrunner application.ini --url "$1" --title "$title" &
sleep 8

wid="$(xdotool search --title "$title")"
tmp="$(mktemp /tmp/traffic.jpg.XXXXXXX)"
rm $tmp
tmp="$tmp.jpg"
echo "wid: $wid"
import -window root $tmp
#import -window $wid -rotate 90 $tmp
echo $tmp

pkill -f "xulrunner.*$title"
pkill -f "X.*$DISPLAY"
