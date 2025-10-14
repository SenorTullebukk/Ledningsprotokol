import os
import sys
import subprocess

# Path to MicroStation executable (update this to your installation path)
MICROSTATION_EXE = r"C:\Program Files\Bentley\MicroStation 2025\MicroStation.exe"
# Path to your .dgn file
DGN_FILE = r"C:\Path\To\Your\File.dgn"
# Path to your MsPy python script
MSPY_SCRIPT = r"C:\Path\To\Your\MsPyScript.py"

def run_microstation_with_script():
    # Build command to open MicroStation with the .dgn file and run the MsPy script
    # This assumes MsPy is integrated and callable from MicroStation's command line
    command = [
        MICROSTATION_EXE,
        DGN_FILE,
        "-wa", "MsPy",  # Load MsPy add-in
        "-script", MSPY_SCRIPT  # Run the python script
    ]
    # Start MicroStation
    proc = subprocess.Popen(command)
    proc.wait()
    # After script runs, close MicroStation without saving
    # This part may require automation via MsPy or MicroStation's API

if __name__ == "__main__":
    run_microstation_with_script()