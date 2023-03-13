import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
# doc: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html
import geojson
# for test
import matplotlib.pyplot as plt

from dwd_stations import get_stations


def create_points() -> np.array:
    points = []
    for station in get_stations():
        points.append([station.lat, station.lon])
    return np.array(list(points))


def create_voronoi_diagram(points: np.array) -> Voronoi:
    return Voronoi(points)


def create_geojson_polygons(voronoi: Voronoi) -> geojson:
    # without the polygons on the edge
    # generate points to create the missing polygons?

    points = []

    for region in voronoi.regions:
        if region != [] and -1 not in region:        # not outer region and not region on the edge
            points.append(region)

    return geojson.MultiPolygon([
        ([tuple(voronoi.vertices[region[count]]) for count in range(len(region))]) for region in points
    ])


def run():
    voronoi = create_voronoi_diagram(create_points())
    print(voronoi.point_region)
    fig = voronoi_plot_2d(voronoi)
    plt.show()



if __name__ == "__main__":
    points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                       [2, 0], [2, 1], [2, 2]])
    vor = Voronoi(points)
    print(vor.point_region)