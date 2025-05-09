import sys
import json
import os

if len(sys.argv) < 2:
    print("Uso: python generate_Theme.py <theme.json>")
    sys.exit(1)

home = os.path.expanduser("~")
json_path = sys.argv[1]

with open(json_path, 'r') as f:
    palette = json.load(f)

output_dir = os.path.join(home, ".config/themesConfig")
os.makedirs(output_dir, exist_ok=True)  # Crea el directorio si no existe

kitty = [
    f"background {palette['background']}",
    f"foreground {palette['foreground']}",
    f"cursor {palette['foreground']}",
    f"color0 {palette['black']}",
    f"color1 {palette['red']}",
    f"color2 {palette['green']}",
    f"color3 {palette['yellow']}",
    f"color4 {palette['blue']}",
    f"color5 {palette['magenta']}",
    f"color6 {palette['cyan']}",
    f"color7 {palette['white']}",
    f"color8 {palette['bright_black']}",
    f"color9 {palette['bright_red']}",
    f"color10 {palette['bright_green']}",
    f"color11 {palette['bright_yellow']}",
    f"color12 {palette['bright_blue']}",
    f"color13 {palette['bright_magenta']}",
    f"color14 {palette['bright_cyan']}",
    f"color15 {palette['bright_white']}",
    f"font_family {palette['font']}",
]

rofi = [
    "* {",
    f"font:   '{palette['font']}';",
    f"bg0     :{palette['background']};",
    f"bg1     :{palette['surface']};",
    f"bg2     :{palette['muted']};",
    f"bg3     :{palette['primary']};",
    f"fg0     :{palette['foreground']};",
    f"fg1     :{palette['primary_muted']};",
    f"fg2     :{palette['muted']};",
    f"fg3     :{palette['link']};",
    f"red     :{palette['red']};",
    f"green   :{palette['green']};",
    f"yellow  :{palette['yellow']};",
    f"blue    :{palette['blue']};",
    f"magenta :{palette['magenta']};",
    f"cyan    :{palette['cyan']};",
    "accent: @bg3;",
    "urgent: @yellow;",
    "background-color : transparent;",
    "text-color       : @fg0;",
    "margin  : 0;",
    "padding : 0;",
    "spacing : 0;",
    f"border: {palette['border_width']};",
    f"rounded: {palette['rounded']}px;",
    "}",
]


with open(os.path.join(output_dir, "kitty-theme.conf"), "w") as f:
    f.write('\n'.join(kitty))

with open(os.path.join(output_dir, "rofi-theme.rasi"), "w") as f:
    f.write('\n'.join(rofi))

print("Theme generated")