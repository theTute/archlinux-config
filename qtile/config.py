from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import os, subprocess, json

# mod keys
mod = "mod4"
alt = "mod1"

# Theme
home = os.path.expanduser("~")
with open(os.path.join(home, ".config/themesConfig/theme.json"), "r") as f:
    theme = json.load(f)


keys = [

    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),

    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Spawn rofi"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "12340"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            Key([mod, alt], i.name, lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(
        border_normal=theme["surface"],
        border_focus=theme["primary_muted"],
        border_width=theme["border_width"],
        single_border_width=theme["border_width"],
        margin=theme["margin"],
        ),
    layout.MonadWide(
        border_normal=theme["surface"],
        border_focus=theme["primary_muted"],
        border_width=theme["border_width"],  
        single_border_width=theme["border_width"],
        margin=theme["margin"],
        ),
    layout.Max(
        border_normal=theme["surface"],
        border_focus=theme["primary_muted"],
        border_width=theme["border_width"],
        margin=theme["margin"],
        ),
]

widget_defaults = dict(
    font="sans",
    fontsize=14,
    padding=4,
)
extension_defaults = widget_defaults.copy()

screens = [
    #First screen
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(" Groups ", background=theme["surface"]),
                widget.Sep(foreground=theme["primary"]),

                widget.GroupBox(
                    disable_drag=True,
                    highlight_method='line',
                    highlight_color=theme["surface"],
                    this_current_screen_border=theme["primary_muted"],
                    ),
                widget.Sep(foreground=theme["primary"]),
                widget.WindowName(max_chars=80),

                widget.Spacer(),

                widget.Systray(background=theme["background"]),
                widget.Spacer(5),
                widget.Sep(foreground=theme["primary"]),

                widget.Clock(
                    format="%y/%m/%d %a %H:%M ",
                    background=theme["surface"],
                ) 
            ],
            28,
            margin=theme["margin"],
            opacity=0.9,
            background = theme["background"]

        ),
        bottom=bar.Gap(theme["margin_thin"]),
    ),
    #Second Screen
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(" Groups ", background=theme["surface"]),
                widget.Sep(foreground=theme["primary"]),

                widget.GroupBox(
                    disable_drag=True,
                    highlight_method='line',
                    highlight_color=theme["surface"],
                    this_current_screen_border=theme["primary_muted"],
                    ),

                widget.TextBox("arch@neko"),
                widget.Sep(foreground=theme["primary"]),

                widget.Spacer(),

                widget.Sep(foreground=theme["primary"]),
                widget.Clock(
                    format="%y/%m/%d %a %H:%M ",
                    background=theme["surface"],
                ) 
            ],
            28,
            margin=theme["margin"],
            opacity=0.9,
            background = theme["background"]

        ),
        bottom=bar.Gap(theme["margin_thin"]),
    ),
 

]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
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
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    processes = [ 
            ['discord'],
            ['picom']
        ]
    for p in processes:
        subprocess.Popen(p)

# This code is property of neco arc
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡔⣻⠁⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⢀⣾⠳⢶⣦⠤⣀⠀⠀⠀⠀⠀⠀⠀⣾⢀⡇⡴⠋⣀⠴⣊⣩⣤⠶⠞⢹⣄⠀⠀⠀
#⠀⠀⠀⠀⢸⠀⠀⢠⠈⠙⠢⣙⠲⢤⠤⠤⠀⠒⠳⡄⣿⢀⠾⠓⢋⠅⠛⠉⠉⠝⠀⠼⠀⠀⠀
#⠀⠀⠀⠀⢸⠀⢰⡀⠁⠀⠀⠈⠑⠦⡀⠀⠀⠀⠀⠈⠺⢿⣂⠀⠉⠐⠲⡤⣄⢉⠝⢸⠀⠀⠀
#⠀⠀⠀⠀⢸⠀⢀⡹⠆⠀⠀⠀⠀⡠⠃⠀⠀⠀⠀⠀⠀⠀⠉⠙⠲⣄⠀⠀⠙⣷⡄⢸⠀⠀⠀
#⠀⠀⠀⠀⢸⡀⠙⠂⢠⠀⠀⡠⠊⠀⠀⠀⠀⢠⠀⠀⠀⠀⠘⠄⠀⠀⠑⢦⣔⠀⢡⡸⠀⠀⠀
#⠀⠀⠀⠀⢀⣧⠀⢀⡧⣴⠯⡀⠀⠀⠀⠀⠀⡎⠀⠀⠀⠀⠀⢸⡠⠔⠈⠁⠙⡗⡤⣷⡀⠀⠀
#⠀⠀⠀⠀⡜⠈⠚⠁⣬⠓⠒⢼⠅⠀⠀⠀⣠⡇⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⡀⢹⠀⠸⡄⠀⠀
#⠀⠀⠀⡸⠀⠀⠀⠘⢸⢀⠐⢃⠀⠀⠀⡰⠋⡇⠀⠀⠀⢠⠀⠀⡿⣆⠀⠀⣧⡈⡇⠆⢻⠀⠀
#⠀⠀⢰⠃⠀⠀⢀⡇⠼⠉⠀⢸⡤⠤⣶⡖⠒⠺⢄⡀⢀⠎⡆⣸⣥⠬⠧⢴⣿⠉⠁⠸⡀⣇⠀
#⠀⠀⠇⠀⠀⠀⢸⠀⠀⠀⣰⠋⠀⢸⣿⣿⠀⠀⠀⠙⢧⡴⢹⣿⣿⠀⠀⠀⠈⣆⠀⠀⢧⢹⡄
#⠀⣸⠀⢠⠀⠀⢸⡀⠀⠀⢻⡀⠀⢸⣿⣿⠀⠀⠀⠀⡼⣇⢸⣿⣿⠀⠀⠀⢀⠏⠀⠀⢸⠀⠇
#⠀⠓⠈⢃⠀⠀⠀⡇⠀⠀⠀⣗⠦⣀⣿⡇⠀⣀⠤⠊⠀⠈⠺⢿⣃⣀⠤⠔⢸⠀⠀⠀⣼⠑⢼
#⠀⠀⠀⢸⡀⣀⣾⣷⡀⠀⢸⣯⣦⡀⠀⠀⠀⢇⣀⣀⠐⠦⣀⠘⠀⠀⢀⣰⣿⣄⠀⠀⡟⠀⠀
#⠀⠀⠀⠀⠛⠁⣿⣿⣧⠀⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⣿⣿⡿⠈⠢⣼⡇⠀⠀
#⠀⠀⠀⠀⠀⠀⠈⠁⠈⠻⠈⢻⡿⠉⣿⠿⠛⡇⠒⠒⢲⠺⢿⣿⣿⠉⠻⡿⠁⠀⠀⠈⠁⠀⠀
#⢀⠤⠒⠦⡀⠀⠀⠀⠀⠀⠀⠀⢀⠞⠉⠆⠀⠀⠉⠉⠉⠀⠀⡝⣍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⡎⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⡰⠋⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⢡⠈⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⡇⠀⠀⠸⠁⠀⠀⠀⠀⢀⠜⠁⠀⠀⠀⡸⠀⠀⠀⠀⠀⠀⠀⠘⡄⠈⢳⡀⠀⠀⠀⠀⠀⠀⠀
#⡇⠀⠀⢠⠀⠀⠀⠀⠠⣯⣀⠀⠀⠀⡰⡇⠀⠀⠀⠀⠀⠀⠀⠀⢣⠀⢀⡦⠤⢄⡀⠀⠀⠀⠀
#⢱⡀⠀⠈⠳⢤⣠⠖⠋⠛⠛⢷⣄⢠⣷⠁⠀⠀⠀⠀⠀⠀⠀⠀⠘⡾⢳⠃⠀⠀⠘⢇⠀⠀⠀
#⠀⠙⢦⡀⠀⢠⠁⠀⠀⠀⠀⠀⠙⣿⣏⣀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣧⡃⠀⠀⠀⠀⣸⠀⠀⠀
#⠀⠀⠀⠈⠉⢺⣄⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⣤⣀⣠⡾⠃⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠣⢅⡤⣀⣀⣠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠉⠉⠉⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠁⠀⠉⣿⣿⣿⣿⣿⡿⠻⣿⣿⣿⣿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⠀⠀⠀⠀⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣟⠀⠀⢠⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⠀⠀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡏⠀⠀⢸⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⠀⠀⠀⢺⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠈⠉⠻⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀       
