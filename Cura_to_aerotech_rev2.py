import numpy as np

input_path = input("input the input cura file name: ")
                  
output_path = input("input the output aerotech file name: ")

diameter_syringe = float(input("input the diameter of of the syringe (mm)"))

diameter_nozzle = float(input("input the diameter of of the nozzle (mm)"))

with open(input_path, 'r') as infile:
    lines = infile.readlines()

modified_lines = []

modified_lines.append("G90")
modified_lines.append("G1 F300")
modified_lines.append("G0 X223.648 Y158.222 Z0.872")

x = 223.648
y = 158.222
z = 0.872
x1 = y1 = e = u = f = 0

for line in lines:
    stripped = line.strip()

    if stripped.startswith("G1"):
        parts = stripped.split()  # makes list of parts i.e. ['G1', 'X1', 'Y1', 'E0.5']


        for part in parts:

            if part.startswith("F"):
                f = float(part[1:])
            elif part.startswith("X"):
                x1 = x - float(part[1:])
                x = float(part[1:])
            elif part.startswith("Y"):
                y1 = y - float(part[1:])
                y = float(part[1:])
            elif part.startswith("Z"):
                z = float(part[1:])
            elif part.startswith("E"):
                e = float(part[1:])
                u += np.sqrt((x1)**2 + (y1)**2) * ( (diameter_nozzle**2) / (diameter_syringe**2) ) 
        
        modified_lines.append("G1 X"+str(x)+" Y"+str(y)+" Z"+str(z)+" U"+str(u))
        
        
  
    elif stripped.startswith("G0"):
        parts = stripped.split()  # makes list of parts i.e. ['G1', 'X1', 'Y1', 'E0.5']


        for part in parts:

            if part.startswith("F"):
                f = float(part[1:])
            elif part.startswith("X"):
                x1 = x - float(part[1:])
                x = float(part[1:])
            elif part.startswith("Y"):
                y1 = y - float(part[1:])
                y = float(part[1:])
            elif part.startswith("Z"):
                z = float(part[1:])
            elif part.startswith("E"):
                e = float(part[1:])
                u += np.sqrt((x1)**2 + (y1)**2) * ( (diameter_nozzle**2) / (diameter_syringe**2) ) 

        modified_lines.append("G0 X"+str(x)+" Y"+str(y)+" Z"+str(z)+" U"+str(u))

# Write the list to a .gcode file
with open(output_path, "w") as file:
    for line in modified_lines:
        file.write(line + "\n")





