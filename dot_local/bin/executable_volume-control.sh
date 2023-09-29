#!/bin/bash

# Get the current volume level
function get_volume() {
    pactl list sinks | grep "Volume:" -m 1 | awk -F/ '{print $2}' | tr -d '[:space:]%'
}

# Check if muted
function is_muted() {
    pactl list sinks | grep "Mute:" -m 1 | awk -F: '{print $2}' | tr -d '[:space:]'
}

# Update and notify
if [ "$1" = "toggle_mute" ]; then
    pactl set-sink-mute @DEFAULT_SINK@ toggle
    if [ "$(is_muted)" = "yes" ]; then
        dunstify -r 1 -h int:value:0 -i ~/.local/icons/volume-x.svg -t 2000 "Muted"
    else
        volume="$(get_volume)"
        dunstify -r 1 -h int:value:$volume -i ~/.local/icons/volume-2.svg -t 2000 "Volume: $volume%"
    fi
else
    pactl set-sink-mute @DEFAULT_SINK@ 0
    pactl set-sink-volume @DEFAULT_SINK@ "$1%"
    volume="$(get_volume)"

    if [[ "$1" == *-* ]]; then 
        dunstify -r 1 -h int:value:$volume -i ~/.local/icons/volume-1.svg -t 2000 "Volume: $volume%"
    else
        dunstify -r 1 -h int:value:$volume -i ~/.local/icons/volume-2.svg -t 2000 "Volume: $volume%"
    fi
fi
