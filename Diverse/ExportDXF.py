from MSPyBentley import *
from MSPyECObjects import *
from MSPyBentleyGeom import *
from MSPyDgnPlatform import *
from MSPyDgnView import *
from MSPyMstnPlatform import *

import tkinter as tk
from tkinter import filedialog

def save_as_dxf():
    # Prompt user for DXF output file path
    root = tk.Tk()
    root.withdraw()
    dxf_path = filedialog.asksaveasfilename(
        title="Save As DXF",
        defaultextension=".dxf",
        filetypes=[("DXF files", "*.dxf"), ("All files", "*.*")]
    )
    root.destroy()
    if not dxf_path:
        MessageCenter.ShowInfoMessage("Save As DXF cancelled.", "", False)
        return

    # Ensure path is quoted for key-in
    dxf_path_quoted = f'"{dxf_path}"'

    # Use MicroStation key-in to perform Save As DXF
    keyin = f'FILE SAVEAS DXF {dxf_path_quoted}'
    KeyinManager.QueueCommand(keyin, 0)
    MessageCenter.ShowInfoMessage(f"Save As DXF command sent: {dxf_path}", "", False)

save_as_dxf()