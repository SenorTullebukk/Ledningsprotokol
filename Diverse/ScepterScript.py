from MSPyBentley import *
from MSPyECObjects import *
from MSPyBentleyGeom import *
from MSPyDgnPlatform import *
from MSPyDgnView import *
from MSPyMstnPlatform import *

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

def get_lines_and_linestrings_in_model(dgnModel, modelName):
    graphicalElements = dgnModel.GetGraphicElements()
    rows = []
    dgnFile = dgnModel.GetDgnFile()
    fileName = os.path.basename(str(dgnFile.FileName)) if dgnFile is not None else ""
    # Prepare level cache once per model
    levelCache = dgnModel.GetLevelCache() if dgnModel is not None else None

    for elemRef in graphicalElements:
        eeh = EditElementHandle(elemRef, dgnModel)
        elemType = eeh.GetElementType()
        msElem = eeh.GetElement()
        # Get level name using ElementPropertiesGetter
        try:
            levelId = ElementPropertiesGetter(eeh).GetLevel()
            levelName = ""
            if levelCache is not None:
                levelHandle = levelCache.GetLevel(levelId, False)
                if levelHandle is not None and levelHandle.IsValid():
                    levelName = levelHandle.GetName()
        except Exception:
            levelName = ""
        if elemType == MSElementTypes.eLINE_ELM:
            try:
                # Use line_3d or line_2d property as available
                if hasattr(msElem, "line_3d"):
                    start = msElem.line_3d.start
                    end = msElem.line_3d.end
                elif hasattr(msElem, "line_2d"):
                    start = msElem.line_2d.start
                    end = msElem.line_2d.end
                else:
                    continue
                # Always provide z for 2d as 0.0
                start_str = f"({start.x},{start.y},{getattr(start,'z',0.0)})"
                end_str = f"({end.x},{end.y},{getattr(end,'z',0.0)})"
                rows.append({
                    "Model": modelName,
                    "FileName": fileName,
                    "Level": levelName,
                    "ElementType": "Line",
                    "ElementId": str(eeh.GetElementId()),
                    "Vertices": f"{start_str} ; {end_str}"
                })
            except Exception as ex:
                rows.append({
                    "Model": modelName,
                    "FileName": fileName,
                    "Level": levelName,
                    "ElementType": "Line",
                    "ElementId": str(eeh.GetElementId()),
                    "Vertices": f"Error: {ex}"
                })
        elif elemType == MSElementTypes.eLINE_STRING_ELM:
            try:
                # Use ICurvePathQuery to get CurveVector
                curve = ICurvePathQuery.ElementToCurveVector(eeh)
                if curve is not None:
                    for i in range(len(curve)):
                        cp = curve[i]
                        if cp.GetCurvePrimitiveType() == ICurvePrimitive.eCURVE_PRIMITIVE_TYPE_LineString:
                            pts = cp.GetLineString()
                            vert_str = "; ".join([f"({pt.x},{pt.y},{pt.z})" for pt in pts])
                            rows.append({
                                "Model": modelName,
                                "FileName": fileName,
                                "Level": levelName,
                                "ElementType": "LineString",
                                "ElementId": str(eeh.GetElementId()),
                                "Vertices": vert_str
                            })
            except Exception as ex:
                rows.append({
                    "Model": modelName,
                    "FileName": fileName,
                    "Level": levelName,
                    "ElementType": "LineString",
                    "ElementId": str(eeh.GetElementId()),
                    "Vertices": f"Error: {ex}"
                })
    return pd.DataFrame(rows)

def get_all_lines_and_linestrings_in_active_and_references():
    """
    Collects all line and linestring elements in the active model and all attached reference models.
    Returns a pandas DataFrame with element info.
    """
    ACTIVEMODEL = ISessionMgr.ActiveDgnModelRef
    dgnModel = ACTIVEMODEL.GetDgnModel()
    if dgnModel is None:
        print("No active DGN model.")
        return pd.DataFrame(columns=["Model", "FileName", "Level", "ElementType", "ElementId", "Vertices"])

    dfs = []
    modelInfo = dgnModel.GetModelInfo()
    modelName = modelInfo.GetName() if modelInfo is not None else "ActiveModel"
    dfs.append(get_lines_and_linestrings_in_model(dgnModel, modelName))

    # Go through all attached reference files
    attachments = dgnModel.GetDgnAttachments()
    if attachments is not None and len(attachments) > 0:
        for i in range(len(attachments)):
            attachment = attachments[i]
            refModel = attachment.GetDgnModel()
            if refModel is not None:
                refModelInfo = refModel.GetModelInfo()
                refModelName = refModelInfo.GetName() if refModelInfo is not None else f"Reference_{i}"
                dfs.append(get_lines_and_linestrings_in_model(refModel, refModelName))
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame(columns=["Model", "FileName", "Level", "ElementType", "ElementId", "Vertices"])

def get_lines_and_linestrings_dataframe():
    """
    Returns the collected DataFrame of line and linestring elements
    in the active model and all attached reference models.
    """
    data = get_all_lines_and_linestrings_in_active_and_references()
    return data

if __name__ == "__main__":
    df = get_lines_and_linestrings_dataframe()
    if df is None or df.empty:
        print("Ingen geometri fundet i filen.")
    else:
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
            title="Vælg hvor filen skal gemmes"
        )
        if save_path:
            df.to_pickle(save_path)
            print(f"Data gemt til: {save_path}")
        else:
            print("Ingen fil valgt. Data blev ikke gemt.")