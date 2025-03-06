"""
we have a roof points and we want to place the modules on the roof. We have fire setback on the roof
The modules are placed in a way that they do not overlap with each other and they do not exceed the fire set back boundary roof boundary.
"""
from shapely.geometry import Polygon
from matplotlib import pyplot as plt
import numpy as np

# internal imports
from functions import extract_x_y


roof = [
    {
        "x": 891.4057295136575,
        "y": 590.6062624916722
    },
    {
        "x": 424.7168554297135,
        "y": 634.5769487008661
    },
    {
        "x": 443.7041972018654,
        "y": 854.4303797468355
    },
    {
        "x": 811.4590273151232,
        "y": 818.454363757495
    },
    {
        "x": 804.4636908727515,
        "y": 701.5323117921386
    },
    {
        "x": 889.4070619586942,
        "y": 693.5376415722851
    },
    {
        "x": 891.4057295136575,
        "y": 590.6062624916722
    }
]

ridge_pts = [[891.4057295136575, 590.6062624916722],
             [424.7168554297135, 634.5769487008661]
            ]

roof_pts = [[pt['x'], pt['y']] for pt in roof]

roof_polygon = Polygon(roof_pts)


# get firesetback at given distance
def get_firesetback(roof_polygon, distance):
    return roof_polygon.buffer(-distance, cap_style='flat', join_style='mitre')


firesetback = get_firesetback(roof_polygon, 10)


def identify_ridge_side(firesetback, ridge_pts):
    adjusted_firesetback = firesetback.buffer(10, cap_style='flat', join_style='mitre')
    adj_firesetback_pts = adjusted_firesetback.boundary.coords.xy
    ridge_arr = np.around(np.array(ridge_pts), decimals=3)

    fsb_lines = []

    for point in range(len(adj_firesetback_pts[0]) - 1):
        start = [adj_firesetback_pts[0][point], adj_firesetback_pts[1][point]]
        end = [adj_firesetback_pts[0][point+1], adj_firesetback_pts[1][point + 1]]

        line = np.around(np.array([start, end]), decimals=3)
        reverse_line = line = np.around(np.array([end, start]), decimals=3)

        match = np.array_equal(ridge_arr, line) or np.array_equal(ridge_arr, reverse_line)

        line_obj = {
            "coords": line,
            "ridge": match
        }
        fsb_lines.append(line_obj)
    return fsb_lines


ridge_identified = identify_ridge_side()

# data required for plotting
firesetback_pts = firesetback.exterior.coords.xy
roof_x, roof_y = extract_x_y(roof_pts)
ridge_x, ridge_y = extract_x_y(ridge_pts)
# adj_firesetback_pts = adjusted_firesetback.boundary.coords.xy





# plotting the outputs
plt.plot(roof_x, roof_y)
plt.plot(ridge_x, ridge_y)
plt.plot(firesetback_pts[0], firesetback_pts[1])
# plt.plot(adj_firesetback_pts[0], adj_firesetback_pts[1])
plt.show()
