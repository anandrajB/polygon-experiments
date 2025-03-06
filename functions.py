import numpy as np


def extract_x_y(line_pts):
    line_pts = np.array(line_pts)
    return line_pts[:, :1].flatten(), line_pts[:, 1:].flatten()


# show the fireset back as diagram
def calc_poi(line_1, line_2):
    line_1 = np.array(line_1)
    line_2_x, line_2_y = extract_x_y(line_2)

    line_2 = np.array(line_2)
    line_1_x, line_1_y = extract_x_y(line_1)

    line_2_dx = line_2_x[1] - line_2_x[0]
    line_2_dy = line_2_y[1] - line_2_y[0]

    line_1_dx = line_1_x[1] - line_1_x[0]
    line_1_dy = line_1_y[1] - line_1_y[0]

    line_2_slope = line_2_dy / line_2_dx
    line_1_slope = line_1_dy / line_1_dx

    line_1_c = line_1_y[0] - (line_1_slope * line_1_x[0])
    line_2_c = line_2_y[0] - (line_2_slope * line_2_x[0])

    x = (line_1_c - line_2_c) / (line_2_slope - line_1_slope)
    y = (line_2_slope*x) + line_2_c

    return x, y


def calc_distance_bwn_2_pts(line_pts: list) -> int:
    """Takes input of points [[x1,y1], [x2,y2] ]"""
    dist = ( (line_pts[1][0] - line_pts[0][0])**2 + (line_pts[1][1] - line_pts[0][1])**2 )**0.5
    return dist



def calc_ratio(short_distance, len_of_line):
    return short_distance / len_of_line


def get_points_at_eq_distance(st_line_pts, distance_bwn_pts_px):
    POINTS = []

    len_of_ridge = calc_distance_bwn_2_pts(st_line_pts)
    no_of_points = int(len_of_ridge // distance_bwn_pts_px)
    initial_distance = distance_bwn_pts_px

    for i in range(no_of_points):
        ratio_i = calc_ratio(initial_distance, len_of_ridge)
        u = st_line_pts[0][0] + ratio_i * (st_line_pts[1][0] - st_line_pts[0][0])
        v = st_line_pts[0][1] + ratio_i * (st_line_pts[1][1] - st_line_pts[0][1])
        initial_distance += distance_bwn_pts_px
        POINTS.append((u, v))

    return {"points": POINTS, "count": no_of_points}


def calc_perpendicular(ridge_pts, rafter_pt, D):
    x1, y1 = ridge_pts[0][0], ridge_pts[0][1]
    x2, y2 = ridge_pts[1][0], ridge_pts[1][1]
    Px1, Py1 = rafter_pt[0], rafter_pt[1]

    ABx = x2 - x1
    ABy = y2 - y1

    # Normalize the direction vector
    length_AB = (ABx**2 + ABy**2)**0.5
    ux = ABx / length_AB
    uy = ABy / length_AB

    # Perpendicular vector
    vx = -uy
    vy = ux

    # Calculate the coordinates of point Q at distance D from P
    Qx1 = Px1 + D * vx
    Qy1 = Py1 + D * vy

    return Qx1, Qy1

