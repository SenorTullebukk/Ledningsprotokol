# file: run_mspython_on_dgn.py
# Purpose: Launch MicroStation, open a DGN, run an MSPy script, then close MicroStation.
# Notes:
#  - Requires MicroStation 2024+ (Python Manager) and pywin32 installed.
#  - The MSPy script runs INSIDE MicroStation via the `python load` key-in.

import os
import time
import traceback
import win32com.client as win32
import pythoncom

def run_mspython_on_dgn(
    dgn_path: str,
    mspy_script_path: str,
    read_only: bool = True,
    visible: bool = False,
    wait_done_file: str | None = None,
    wait_timeout_s: int = 600,
    autosave: bool = False
) -> int:
    """
    Returns 0 on success, non-zero on failure.
    """
    # Normalize path
    dgn_path = os.path.abspath(dgn_path)

    # Open DGN file with default associated program
    try:
        os.startfile(dgn_path)
    except Exception as e:
        print(f"Failed to open DGN file: {e}")
        return 4

    time.sleep(5)  # Wait for the program to start and load the file

    app = None
    try:
        # Ensure COM is initialized in this thread
        pythoncom.CoInitialize()

        # Bind to MicroStation
        app = win32.gencache.EnsureDispatch("MicroStationDGN.Application")
        app.Visible = bool(visible)

        # Wait until MicroStation has an active design file
        max_wait = 30  # seconds
        start_time = time.time()
        design_file = None
        while time.time() - start_time < max_wait:
            try:
                design_file = app.ActiveDesignFile
                if design_file and design_file.FullName.lower() == dgn_path.lower():
                    break
            except Exception:
                pass
            time.sleep(1)
        if not design_file or design_file.FullName.lower() != dgn_path.lower():
            print(f"[ERROR] Failed to open DGN file: {dgn_path}")
            return 5

        # Optional: confirm we have an active design file
        _ = app.ActiveDesignFile

        # --- Run the MSPy script inside MicroStation ---
        # You can load .py or .pyc; both are supported by docs/presentations.
        # Key-in must quote any path with spaces.
        keyin = f'python load "{mspy_script_path}"'
        app.CadInputQueue.SendKeyin(keyin)

        # If you want to wait until the script signals completion, let the
        # MSPy script create a sentinel file and wait for it here.
        if wait_done_file:
            wait_done_file = os.path.abspath(wait_done_file)
            print(f"[INFO] Waiting for sentinel: {wait_done_file}")
            deadline = time.time() + wait_timeout_s
            while time.time() < deadline:
                if os.path.exists(wait_done_file):
                    print("[INFO] MSPy script signaled completion.")
                    break
                time.sleep(0.5)
            else:
                print("[WARN] Timeout waiting for sentinel file.")

        # Save or discard changes as desired
        if autosave and not read_only:
            try:
                # Save Settings + Design (optional)
                app.CadInputQueue.SendKeyin("file design")  # same as File > Save
            except Exception:
                pass

        # Close MicroStation
        try:
            # Prefer explicit quit; fall back to EXIT key-in
            app.Quit()  # may not exist on some versions
        except Exception:
            app.CadInputQueue.SendKeyin("exit")

        return 0

    except Exception:
        print("[EXC] Failure while automating MicroStation:")
        traceback.print_exc()
        try:
            if app is not None:
                app.CadInputQueue.SendKeyin("exit")
        except Exception:
            pass
        return 1

    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass