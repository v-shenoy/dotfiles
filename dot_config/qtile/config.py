import os, subprocess
import webbrowser

from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Terminal
terminal = guess_terminal("kitty")
browser = "firefox"
wallpaper = "~/Pictures/wallpapers/Black Cat.png"

# Keybindings
## Mod Key = Super / Windows key
mod = "mod4"

@lazy.function
def open_docs(qtile):
    webbrowser.open_new("https://docs.qtile.org/en/latest/")

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus left"),
    Key([mod], "left", lazy.layout.left(), desc="Move focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus right"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to next window in layout"),
    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows.
    Key([mod, "control"], "h", lazy.layout.grow_left().when(layout=["bsp", "columns"]), desc="Grow window left"),
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window right"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Applications
    Key([mod], "d", lazy.spawn("rofi -modi drun -show drun -show-icons"), desc="Launch rofi"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "f", lazy.spawn(browser), desc="Launch browser"),
    KeyChord([mod], "p", [
        Key([], "t", lazy.spawn(terminal), desc="Launch terminal"),
        Key([], "f", lazy.spawn(browser), desc="Launch browser"),
        ],
        mode=False,
        name="Launch",
    ),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc="Launch flameshot gui"),
    Key([], "Print", lazy.spawn("flameshot full"), desc="Take full screenshot"),

    # Layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle layouts"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle stack split"),

    # Misc.
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn command using prompt widget"),
    Key([mod], "l", lazy.spawn("betterlockscreen --lock dim"), desc="Lock screen"),
    Key([mod, "control"], "x", lazy.spawn("dm-tool switch-to-greeter"), desc="Lock screen"),

    # Qtile
    Key([mod, "control"], "d", open_docs, desc="Open Qtile Docs"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload Qtile config"),
]


# Workspaces
groups = [Group(str(i)) for i in range(1, 10)]
for group in groups:
    keys.extend(
        [
            Key([mod], group.name, lazy.group[group.name].toscreen(), desc=f"Switch to group {group.name}"),
            Key([mod, "shift"], group.name, lazy.window.togroup(group.name), desc=f"Move focused window to group {group.name}"),
        ]
    )

# Screens
screens = [
    Screen(
        wallpaper=wallpaper,
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox("default config", name="default"),
                widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Layouts
layout_defaults = {
    "border_focus": "#007030",
    "border_normal": "#220000",
    "border_width": 3,
    "margin": 5,
}
layouts = [
    layout.Bsp(**layout_defaults),
    layout.Columns(**layout_defaults),
    layout.Matrix(**layout_defaults),
    layout.Max(margin=layout_defaults.get("margin")),
    layout.MonadTall(**layout_defaults),
    layout.MonadWide(**layout_defaults),
    layout.Spiral(**layout_defaults),
    layout.TreeTab(**layout_defaults),
    layout.Zoomy(**layout_defaults),
]

# Mouse.
mouse = [
    # Drag floating layouts (left-click).    
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    # Resize floating layouts (right-click).
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    # Bring floating layouts to front (middle-click).
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# Misc.
auto_fullscreen = True
bring_front_click = False
cursor_warp = False
dgroups_key_binder = None
dgroups_app_rules = []
widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
floats_kept_above = True
focus_on_window_activation = "smart"
follow_mouse_focus = True
reconfigure_screens = True
wmname = "LG3D"
auto_minimize = True

@hook.subscribe.startup
def autostart():
    script = os.path.expanduser("~/.config/autostart.sh")
    subprocess.run([script])
