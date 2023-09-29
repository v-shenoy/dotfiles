#!/bin/bash

# Screen layout
xrandr --output HDMI-1 --left-of eDP-1 --auto

# Compositor
picom --config  ~/.config/picom/picom.conf &
