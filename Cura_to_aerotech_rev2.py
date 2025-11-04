# gcode_modifier.py
def modify_gcode(input_path: str, output_path: str):
    """
    Reads a G-code file, modifies it, and writes out a new version.

    :param input_path: Path to the input G-code file
    :param output_path: Path to save the modified G-code
    """
    with open(input_path, 'r') as infile:
        lines = infile.readlines()

    modified_lines = []


for line in lines:
  stripped = line.strip()

  if stripped.startswith("G1"):
    parts = lstripped.split()  # makes list of parts i.e. ['G1', 'X1', 'Y1', 'E0.5']

    # Initialize variables (default to None or 0)
    x = y = e = None

    for part in parts:
        if part.startswith("X"):
            x = float(part[1:])  # take everything after 'X' and convert to float
        elif part.startswith("Y"):
            y = float(part[1:])
        elif part.startswith("E"):
            e = float(part[1:])
    
        
        


  
  elif stripped.startswith("G1"):


  



      for line in lines:
        stripped = line.strip()

        # Example modification: add comment before each G1 command
        if stripped.startswith("G1"):
            modified_lines.append("; Modified: movement command below\n")

            # (Optional) Example: scale extrusion values
            # If line contains "E" parameter, scale it
            parts = stripped.split()
            new_parts = []
            for part in parts:
                if part.startswith("E"):
                    try:
                        value = float(part[1:])
                        value *= 1.05  # scale extrusion by +5%
                        new_parts.append(f"E{value:.4f}")
                    except ValueError:
                        new_parts.append(part)
                else:
                    new_parts.append(part)
            stripped = " ".join(new_parts)
