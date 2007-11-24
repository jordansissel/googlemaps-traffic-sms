#!/bin/sh

xulapp="/u9/psionic/projects/traffic/application.ini"

tries="1 2 3 4 5 6 7 8 9 10"
found=0
for t in $tries; do
  DISPLAY=`perl -e 'srand(time()); print int(rand() * 1000)'`
  export DISPLAY
  if [ ! -e "/tmp/.X11-unix/X$DISPLAY" ]; then
    DISPLAY=":$DISPLAY"
    echo $DISPLAY >&2
    startx -- /usr/local/bin/Xvfb $DISPLAY -screen 0 800x600x24 > /dev/null 2>&1 &
    found=1
    break
  fi
done

if [ "$found" -eq "0" ]; then
  echo "Tried to find an unused X server, but none were found" >&2
  exit 1
fi

for t in $tries; do
  xdpyinfo > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    break;
  fi
  echo "Waiting for Xvfb to start" >&2
  sleep 1
done

echo "X is running" >&2

tmp="$(mktemp /tmp/traffic.jpg.XXXXXXX)"

title="traffic $$"
echo "Title: $title" >&2
echo "URL: $1" >&2
xulrunner $xulapp --url "$1" --title "$title" >&2 &
echo "xulrunner exit: $?" >&2

for t in $tries; do
  wid="$(xdotool search --title "$title")"
  if [ ! -z "$wid" ]; then
    break
  fi
  echo "Waiting for xulrunner" >&2
  sleep 1
done

if [ -z "$wid" ]; then
  echo "Failed to find the xulrunner window" >&2
fi

rm $tmp
tmp="$tmp.jpg"
echo "wid: $wid" >&2

# Wait a few seconds for the page to load
sleep 15
xdotool search --title "$title" >&2
#import -window root $tmp
import -window $wid -rotate 90 $tmp
echo $tmp

exec 1>-
exec 2>-

pkill -f "xulrunner.*$title"
pkill -f "X.*$DISPLAY"
