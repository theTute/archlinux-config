import sys
import json

if len(sys.argv) < 2:
    print("Uso: python generate_kitty_theme.py <archivo_json>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r') as f:
    palette = json.load(f)

lines = [
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
    f"font_family {palette['font']}"
]

with open("kitty-theme.conf", "w") as f:
    f.write("\n".join(lines))

print("Tema generado como kitty-theme.conf")