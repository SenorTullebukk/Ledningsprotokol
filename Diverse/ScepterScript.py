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

def get_element_properties(eeh, dgnModel, levelCache):
    """Extract all available properties and geometry attributes from an element."""
    props = {}
    props['ElementId'] = str(eeh.GetElementId())
    props['ElementType'] = str(eeh.GetElementType())
    props['Is3d'] = dgnModel.Is3d()
    # Use ElementPropertiesGetter to get the element class
    try:
        props['Class'] = str(ElementPropertiesGetter(eeh).GetElementClass())
    except Exception:
        props['Class'] = ""
    props['IsComplexHeader'] = eeh.Element.IsComplexHeader() if hasattr(eeh, 'Element') else False
    # Level
    try:
        levelId = ElementPropertiesGetter(eeh).GetLevel()
        levelName = ""
        if levelCache is not None:
            levelHandle = levelCache.GetLevel(levelId, False)
            if levelHandle is not None and levelHandle.IsValid():
                levelName = levelHandle.GetName()
        props['Level'] = levelName
    except Exception:
        props['Level'] = ""
    # Geometry
    try:
        elemType = eeh.GetElementType()
        msElem = eeh.GetElement()
        if elemType == MSElementTypes.eLINE_ELM:
            if hasattr(msElem, "line_3d"):
                start = msElem.line_3d.start
                end = msElem.line_3d.end
            elif hasattr(msElem, "line_2d"):
                start = msElem.line_2d.start
                end = msElem.line_2d.end
            else:
                start = end = None
            if start and end:
                props['Geometry'] = f"Line: ({start.x},{start.y},{getattr(start, 'z', 0.0)}) ; ({end.x},{end.y},{getattr(end, 'z', 0.0)})"
        elif elemType == MSElementTypes.eLINE_STRING_ELM:
            curve = ICurvePathQuery.ElementToCurveVector(eeh)
            if curve is not None:
                for i in range(len(curve)):
                    cp = curve[i]
                    if cp.GetCurvePrimitiveType() == ICurvePrimitive.eCURVE_PRIMITIVE_TYPE_LineString:
                        pts = cp.GetLineString()
                        vert_str = "; ".join([f"({pt.x},{pt.y},{getattr(pt, 'z', 0.0)})" for pt in pts])
                        props['Geometry'] = f"LineString: {vert_str}"
        elif elemType == MSElementTypes.eSHAPE_ELM:
            curve = ICurvePathQuery.ElementToCurveVector(eeh)
            if curve is not None:
                for i in range(len(curve)):
                    cp = curve[i]
                    if cp.GetCurvePrimitiveType() == ICurvePrimitive.eCURVE_PRIMITIVE_TYPE_LineString:
                        pts = cp.GetLineString()
                        vert_str = "; ".join([f"({pt.x},{pt.y},{getattr(pt, 'z', 0.0)})" for pt in pts])
                        props['Geometry'] = f"Shape: {vert_str}"
        elif elemType == MSElementTypes.eCOMPLEX_CHAIN_HEADER_ELM:
            # Complex Chain: collect all sub-elements' geometry
            chain_geom = []
            curve = ICurvePathQuery.ElementToCurveVector(eeh)
            if curve is not None:
                for i in range(len(curve)):
                    cp = curve[i]
                    if cp.GetCurvePrimitiveType() == ICurvePrimitive.eCURVE_PRIMITIVE_TYPE_LineString:
                        pts = cp.GetLineString()
                        chain_geom.append("; ".join([f"({pt.x},{pt.y},{getattr(pt, 'z', 0.0)})" for pt in pts]))
                    elif cp.GetCurvePrimitiveType() == ICurvePrimitive.eCURVE_PRIMITIVE_TYPE_Line:
                        seg = cp.GetLine()
                        chain_geom.append(f"({seg.point[0].x},{seg.point[0].y},{getattr(seg.point[0], 'z', 0.0)}) ; "
                                         f"({seg.point[1].x},{seg.point[1].y},{getattr(seg.point[1], 'z', 0.0)})")
            props['Geometry'] = "ComplexChain: " + " | ".join(chain_geom)
        elif elemType == MSElementTypes.eELLIPSE_ELM:
            ell = eeh.GetElement()
            if hasattr(ell, "ellipse_3d"):
                center = ell.ellipse_3d.center
                props['Geometry'] = f"Ellipse center: ({center.x},{center.y},{getattr(center, 'z', 0.0)})"
            elif hasattr(ell, "ellipse_2d"):
                center = ell.ellipse_2d.center
                props['Geometry'] = f"Ellipse center: ({center.x},{center.y},0.0)"
        elif elemType == MSElementTypes.eCELL_HEADER_ELM:
            cellName = ""
            try:
                cellName = eeh.GetCellName()
            except Exception:
                pass
            props['Geometry'] = f"CellHeader: {cellName}"
        elif elemType == MSElementTypes.eTEXT_ELM or elemType == MSElementTypes.eTEXT_NODE_ELM:
            try:
                textQuery = eeh.GetITextQuery()
                if textQuery and textQuery.IsTextElement(eeh):
                    textPart = DimensionTextPartId.Create(0, eDIMTEXTPART_Primary, eDIMTEXTSUBPART_Main)
                    textBlock = textQuery.GetTextPart(eeh, textPart)
                    if textBlock and not textBlock.IsEmpty():
                        props['Geometry'] = f"Text: {textBlock.ToString().GetWCharCP()}"
            except Exception:
                pass
    except Exception as ex:
        props['Geometry'] = f"Error: {ex}"
    return props

def get_all_elements_in_model(dgnModel, modelName):
    """Collect all elements and their properties from a model."""
    graphicalElements = dgnModel.GetGraphicElements()
    rows = []
    dgnFile = dgnModel.GetDgnFile()
    fileName = os.path.basename(str(dgnFile.FileName)) if dgnFile is not None else ""
    levelCache = dgnModel.GetLevelCache() if dgnModel is not None else None

    for elemRef in graphicalElements:
        eeh = EditElementHandle(elemRef, dgnModel)
        props = get_element_properties(eeh, dgnModel, levelCache)
        props['Model'] = modelName
        props['FileName'] = fileName
        rows.append(props)
    return pd.DataFrame(rows)

def get_all_elements_in_active_and_references():
    """
    Collects all elements and their properties in the active model and all attached reference models.
    Returns a pandas DataFrame with all info.
    """
    ACTIVEMODEL = ISessionMgr.ActiveDgnModelRef
    dgnModel = ACTIVEMODEL.GetDgnModel()
    if dgnModel is None:
        print("No active DGN model.")
        return pd.DataFrame()

    dfs = []
    modelInfo = dgnModel.GetModelInfo()
    modelName = modelInfo.GetName() if modelInfo is not None else "ActiveModel"
    dfs.append(get_all_elements_in_model(dgnModel, modelName))

    # Go through all attached reference files
    attachments = dgnModel.GetDgnAttachments()
    if attachments is not None and len(attachments) > 0:
        for i in range(len(attachments)):
            attachment = attachments[i]
            refModel = attachment.GetDgnModel()
            if refModel is not None:
                refModelInfo = refModel.GetModelInfo()
                refModelName = refModelInfo.GetName() if refModelInfo is not None else f"Reference_{i}"
                dfs.append(get_all_elements_in_model(refModel, refModelName))
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    df = get_all_elements_in_active_and_references()
    if df is None or df.empty:
        print("Ingen geometri fundet i filen.")
    else:
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Vælg hvor filen skal gemmes"
        )
        if save_path:
            df.to_excel(save_path, index=False)
            print(f"Data gemt til: {save_path}")
        else:
            print("Ingen fil valgt. Data blev ikke gemt.")