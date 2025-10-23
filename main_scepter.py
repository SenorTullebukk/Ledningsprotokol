import geopandas as gpd
import matplotlib.pyplot as plt
import math
import ezdxf
from pathlib import Path
from shapely.geometry import LineString, Polygon, Point

def Start_scepterprogram():
    data_dir = Path(__file__).resolve().parent / "Diverse" / "DXF_Filer"
    data_dir.mkdir(parents=True, exist_ok=True)

    def _extract_points(entity):
        # return list of (x,y) tuples for polyline-like entities
        for fn in ("get_points", "points", "vertices"):
            if hasattr(entity, fn):
                pts = []
                try:
                    for p in getattr(entity, fn)():
                        pts.append((float(p[0]), float(p[1])))
                    return pts
                except Exception:
                    # some variants return iterables differently, try fallback below
                    pass
        # fallback: try iterating attributes
        try:
            return [(float(v[0]), float(v[1])) for v in entity]
        except Exception:
            return []

    gdf_records = []
    dxf_files = list(data_dir.glob("*.dxf"))

    for dxf_path in dxf_files:
        try:
            doc = ezdxf.readfile(str(dxf_path))
        except Exception as e:
            print(f"Failed to read {dxf_path.name}: {e}")
            continue
        msp = doc.modelspace()
        for entity in msp:
            try:
                etype = entity.dxftype()
                layer = getattr(getattr(entity, "dxf", None), "layer", "")
                geom = None

                if etype == "LINE":
                    start = entity.dxf.start
                    end = entity.dxf.end
                    geom = LineString([(float(start[0]), float(start[1])), (float(end[0]), float(end[1]))])

                elif etype in ("LWPOLYLINE", "POLYLINE"):
                    pts = _extract_points(entity)
                    if not pts:
                        continue
                    closed = getattr(entity, "closed", False) or (pts[0] == pts[-1])
                    geom = Polygon(pts) if closed else LineString(pts)

                elif etype == "POINT":
                    loc = entity.dxf.location
                    geom = Point(float(loc[0]), float(loc[1]))

                elif etype == "CIRCLE":
                    c = entity.dxf.center
                    r = float(entity.dxf.radius)
                    geom = Point(float(c[0]), float(c[1])).buffer(r, resolution=64)

                elif etype == "ARC":
                    c = entity.dxf.center
                    r = float(entity.dxf.radius)
                    start_ang = float(entity.dxf.start_angle)
                    end_ang = float(entity.dxf.end_angle)
                    # sample the arc with 36 segments
                    ang1 = math.radians(start_ang)
                    ang2 = math.radians(end_ang)
                    # ensure direction and proper sampling across angle wrap
                    if ang2 < ang1:
                        ang2 += 2 * math.pi
                    n = max(8, int((ang2 - ang1) / (math.pi / 36)) + 1)
                    pts = []
                    for i in range(n + 1):
                        a = ang1 + (ang2 - ang1) * i / n
                        pts.append((float(c[0]) + r * math.cos(a), float(c[1]) + r * math.sin(a)))
                    geom = LineString(pts)

                if geom is not None:
                    gdf_records.append({
                        "filename": dxf_path.name,
                        "layer": layer,
                        "etype": etype,
                        "geometry": geom
                    })
            except Exception:
                # skip problematic entity
                continue

    if not gdf_records:
        print("No DXF entities imported.")
        gdf_all = gpd.GeoDataFrame(columns=["filename", "layer", "etype", "geometry"])
    else:
        gdf_all = gpd.GeoDataFrame(gdf_records, geometry="geometry")
        print(f"Imported {len(gdf_all)} entities from {len(dxf_files)} DXF files.")

    return gdf_all
    

if __name__ == "__main__":
    gpfall = Start_scepterprogram()
    import matplotlib.pyplot as plt

    if gpfall.empty:
        print("No features to plot.")
    else:
        fig, ax = plt.subplots(figsize=(10, 10))

        polys = gpfall[gpfall.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
        if not polys.empty:
            polys.plot(
                ax=ax,
                column="layer",
                cmap="tab20c",
                alpha=0.5,
                edgecolor="k",
                linewidth=0.5,
                legend=False,
            )

        lines = gpfall[gpfall.geometry.geom_type.isin(["LineString", "MultiLineString"])]
        if not lines.empty:
            lines.plot(
                ax=ax,
                column="etype",
                cmap="tab10",
                linewidth=1,
                legend=False,
            )

        pts = gpfall[gpfall.geometry.geom_type.isin(["Point", "MultiPoint"])]
        if not pts.empty:
            pts.plot(ax=ax, color="red", markersize=20, zorder=3)

        ax.set_title("Imported DXF Entities")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_aspect("equal", adjustable="datalim")
        plt.tight_layout()
        plt.show()