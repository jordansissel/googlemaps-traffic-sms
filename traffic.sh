#!/bin/sh

title="traffic $$"
xulrunner application.ini --url "$1" --title "$title" &
sleep 8

wid="$(xdotool search --title "$title")"
tmp="$(mktemp /tmp/traffic.jpg.XXXXXXX)"
rm $tmp
tmp="$tmp.jpg"
import -window $wid -rotate 90 $tmp
echo $tmp

pkill -f "xulrunner.*$title"

