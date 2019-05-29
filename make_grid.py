# GeoPy can be used to interface to map box https://pypi.org/project/geopy/
from pygeodesy.ellipsoidalVincenty import LatLon
from geojson import Polygon, Feature, FeatureCollection, dump
import sys
import random

BEARING_SOUTH = 180.0
BEARING_EAST = 90.0


class Cell(object):
    def __init__(self, cellId, top_left_cell, top_right_cell, bottom_right_cell, bottom_left_cell):
        self.cellId = cellId
        self.top_left_cell = top_left_cell
        self.top_right_cell = top_right_cell
        self.bottom_right_cell = bottom_right_cell
        self.bottom_left_cell = bottom_left_cell

    def __repr__(self):
        return str(self.__dict__)


def generate_cell(current_cell_id, top_left_cell, top_right_cell, bottom_right_cell, bottom_left_cell):
    c = Cell(current_cell_id, top_left_cell, top_right_cell, bottom_right_cell, bottom_left_cell)
    # Expect other data to be inserted into the cell here
    return c


def generate_cell_grid(top_left, east_extent, south_extent, cell_lat_size_meters, cell_long_size_meters):
    south_distance = 0
    current_cell_id = 0

    list_of_cells = []

    left_edge = top_left

    while south_distance < south_extent:
        south_distance = south_distance + cell_lat_size_meters
        point_south_of_left_edge = left_edge.destination(cell_lat_size_meters, BEARING_SOUTH)

        top_left_cell = left_edge
        bottom_left_cell = point_south_of_left_edge
        east_distance = 0

        while east_distance < east_extent:
            top_right_cell = top_left_cell.destination(cell_long_size_meters, BEARING_EAST)
            bottom_right_cell = bottom_left_cell.destination(cell_long_size_meters, BEARING_EAST)

            cell = generate_cell(current_cell_id, top_left_cell, top_right_cell, bottom_right_cell, bottom_left_cell)
            current_cell_id = current_cell_id + 1

            list_of_cells.append(cell)

            # Increments
            top_left_cell = top_right_cell
            bottom_left_cell = bottom_right_cell
            east_distance = east_distance + cell_long_size_meters

        left_edge = point_south_of_left_edge

    return list_of_cells


def grid_to_geojson(grid):
    features = []

    for cell in grid:
        rect_points = [
            [
            (cell.top_left_cell.lon, cell.top_left_cell.lat),
            (cell.top_right_cell.lon, cell.top_right_cell.lat),
            (cell.bottom_right_cell.lon, cell.bottom_right_cell.lat),
            (cell.bottom_left_cell.lon, cell.bottom_left_cell.lat),
            (cell.top_left_cell.lon, cell.top_left_cell.lat) #Because first and last points have to match
            ]
        ]
        properties = {
            'capacity': random.randint(0, 5)
        } # TODO this is just an example

        polygon = Polygon(rect_points)
        feature = Feature(geometry=polygon, id=cell.cellId, properties=properties)

        features.append(feature)

    return FeatureCollection(features)


def main():
    TOP_LEFT = LatLon(-37.721874, 144.966859)
    EAST_EXTENT = 1000.0
    SOUT_EXTENT = 1000.0

    CELL_LONG_SIZE_METERS = 100.0
    CELL_LAT_SIZE_METERS = 100.0

    grid = generate_cell_grid(TOP_LEFT, EAST_EXTENT, SOUT_EXTENT, CELL_LAT_SIZE_METERS, CELL_LONG_SIZE_METERS)

    geojson_feature_collection = grid_to_geojson(grid)
    dump(geojson_feature_collection, sys.stdout, indent=4)

    json_file = open('grid.geojson', 'w')
    dump(geojson_feature_collection, json_file, indent=4)




if __name__ == '__main__':
    main()
