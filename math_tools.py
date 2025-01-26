import numpy as np


def nearest_point(x_param: float,
                  y_param: float,
                  z_param: float,
                  const: float,
                  point: tuple[float, float, float]) -> np.ndarray:
    """
    finds nearest point on a plane to another point
    :param x_param: plane x parameter
    :param y_param: plane y parameter
    :param z_param: plane z parameter
    :param const: plane constant parameter
    :param point: point in 3 space
    :return: closest point on the plane
    """
    a, b, c = point

    vec = np.array([[-2 * x_param],
                    [-2 * y_param],
                    [-2 * z_param],
                    [const]])

    matrix = np.array([[2, 0, 0, a],
                       [0, 2, 0, b],
                       [0, 0, 2, c],
                       [x_param, y_param, z_param, 0]])

    return np.dot(np.linalg.inv(matrix), vec)


if __name__ == '__main__':
    x = -1
    y = 0
    z = 0
    con = 0
    Point = (1, 1, 1)
    pos = nearest_point(x, y, z, con, Point)
    X, Y, Z = pos[:3]
    ans = x * X + y * Y + z * Z
    print(pos)
    print(ans)
