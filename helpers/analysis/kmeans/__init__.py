import json

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import aiofiles
import asyncio
import folium
import pathlib
import branca.element as be
import matplotlib.colors as mcolors

ROOT_PATH = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
DATA_PATH = ROOT_PATH / "data" / "v2"
DOCS_PATH = ROOT_PATH / "docs"

EARTH_RADIUS_KM = 6371
EPS_KM = 0.5  # 核心點半徑 (公里)
MIN_SAMPLES = 2  # 最小點數


async def get_json_files(json_file: pathlib.Path):
    async with aiofiles.open(json_file, mode="r") as f:
        json_content = await f.read()
    return json.loads(json_content)


def clean_data(centers: list[dict]) -> list[dict]:
    ok_centers = []
    for center in centers:
        branch_coordinates = center.get("branch_coordinates", None)
        fullname = center["fullname"]
        if isinstance(branch_coordinates, dict):
            ok_centers.append(
                {
                    "fullname": fullname,
                    "latitude": branch_coordinates["latitude"],
                    "longitude": branch_coordinates["longitude"],
                }
            )
            continue
        if isinstance(branch_coordinates, list):
            for branch_coordinate in branch_coordinates:
                name = "None" if (this_name := branch_coordinate.get("name")) is None else this_name
                ok_centers.append(
                    {
                        "fullname": fullname + "-" + name,
                        "latitude": branch_coordinate["latitude"],
                        "longitude": branch_coordinate["longitude"],
                    }
                )
            continue
        if branch_coordinates is None:
            pass
    return ok_centers


def kmeans_clustering(df: pd.DataFrame, n_clusters=20):
    coords = df[["latitude", "longitude"]].values

    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(coords)

    df["Cluster_ID"] = kmeans.labels_

    cluster_ids = sorted(df["Cluster_ID"].unique())

    df["latitude"] = df["latitude"].astype(np.float64)
    df["longitude"] = df["longitude"].astype(np.float64)

    map_center_lat = df["latitude"].mean()
    map_center_lon = df["longitude"].mean()

    colors = list(mcolors.TABLEAU_COLORS.keys())
    colormap = {}
    for i, c_id in enumerate(cluster_ids):
        colormap[c_id] = mcolors.TABLEAU_COLORS[colors[i % len(colors)]]
    colormap[-1] = "#000000"  # 黑色

    m = folium.Map(
        location=[map_center_lat, map_center_lon],
        zoom_start=10,
        tiles="CartoDB Positron",
        attr=f"Been Play 地點位置分析({EPS_KM=}, {MIN_SAMPLES=})",
        # tiles=f'Been Play 地點位置分析({EPS_KM=}, {MIN_SAMPLES=})'
    )
    for idx, row in df.iterrows():
        cluster_id = row["Cluster_ID"]
        lat = row["latitude"]
        lon = row["longitude"]
        name = row["fullname"]

        point_color = colormap[cluster_id]

        popup_text = f"""
        <div>
            <h3>{name}</h3>
            <p>經度: {lon:.4f}</p>
            <p>緯度: {lat:.4f}</p>
            <p>Group: {cluster_id}</p>
        </div>
        """
        iframe = be.IFrame(html=popup_text, width="vw50", height="vh50")
        popup = folium.Popup(iframe)

        folium.CircleMarker(
            location=(lat, lon),
            radius=5,  # 圓形大小
            color=point_color,  # 圓形邊框顏色
            fill=True,
            fill_color=point_color,  # 圓形填充顏色
            fill_opacity=0.9,
            popup=popup,  # 點擊時顯示資訊
        ).add_to(m)
    output_file = DOCS_PATH / "been_play_kmeans_clusters_map.html"
    m.save(output_file)


async def main():
    tasks = [get_json_files(file) for file in DATA_PATH.glob("*.json") if not file.name.startswith("_")]
    json_files = await asyncio.gather(*tasks)

    centers = clean_data([json_file["information"] for json_file in json_files])
    kmeans_clustering(pd.DataFrame(centers))


if __name__ == "__main__":
    asyncio.run(main())
