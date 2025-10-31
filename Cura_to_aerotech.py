import tkinter as tk
from tkinter import filedialog
import os

REFERENCE_Z_OFFSET = 124.572  # mm

def convert_to_aerotech(cura_lines, layer_height, nozzle_diameter, syringe_length):
    output = []
    current_layer = 0
    z_shift = syringe_length - REFERENCE_Z_OFFSET

    for line in cura_lines:
        original_line = line.rstrip()

        # Preserve Cura layer markers
        if original_line.strip().startswith(';LAYER:'):
            try:
                current_layer = int(original_line.strip().split(':')[1])
            except ValueError:
                pass
            output.append(original_line)
            continue

        if not original_line.strip():
            continue

        tokens = original_line.strip().split()
        gcode = tokens[0]

        if gcode.startswith(('M', 'T', 'G92', 'G28')):
            continue

        seen_axes = set()
        filtered_tokens = [gcode]

        for token in tokens[1:]:
            if len(token) < 2:
                continue

            axis = token[0]
            value = token[1:]

            if axis == 'Z' and 'Z' not in seen_axes:
                try:
                    base_z = (current_layer * layer_height) + nozzle_diameter
                    adjusted_z = base_z - z_shift  # ← Fixed: subtract shift instead of add
                    filtered_tokens.append(f"Z{adjusted_z:.3f}")
                    seen_axes.add('Z')
                except ValueError:
                    continue
            elif axis in {'X', 'Y', 'F'} and axis not in seen_axes:
                filtered_tokens.append(token)
                seen_axes.add(axis)

        if len(filtered_tokens) > 1 or gcode in {'G90', 'G91'}:
            if ';' in original_line:
                comment = original_line[original_line.index(';'):]
                output.append(' '.join(filtered_tokens) + ' ' + comment)
            else:
                output.append(' '.join(filtered_tokens))

    return output

def main():
    try:
        layer_height = float(input("Enter layer height in mm (e.g., 0.2): "))
        nozzle_diameter = float(input("Enter nozzle diameter in mm (e.g., 0.4): "))
        syringe_length = float(input("Enter syringe length in mm (e.g., 126.572): "))
    except ValueError:
        print("Invalid numeric input.")
        return

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Select Cura G-code File",
        filetypes=[("G-code files", "*.gcode"), ("All files", "*.*")]
    )

    if not path:
        print("No file selected.")
        return

    with open(path, 'r') as f:
        lines = f.readlines()

    converted = convert_to_aerotech(lines, layer_height, nozzle_diameter, syringe_length)

    base, ext = os.path.splitext(path)
    output_path = f"{base}_aerotech_modified{ext}"

    with open(output_path, 'w') as f:
        f.write('\n'.join(converted))

    print(f"Aerotech-compatible G-code saved to:\n{output_path}")

if __name__ == "__main__":
    main()
