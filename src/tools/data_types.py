# https://github.com/stevenkfirth/crossproduct/blob/2d28e3bb1edc80a2e45c348b8dc9a7311bd0a661/crossproduct/point.py

import collections.abc
import itertools
import math
import time

import cv2
import colorsys
import random

import numpy as np





# from mighty_tools.SegmentAnything import SAM


class Point(collections.abc.Sequence):
    """A point, as described by xy or xyz coordinates.

    :param coordinates: Argument list of two (xy) or three (xyz) coordinates.
        Coordinates should be of type int, float or similar numeric. These values
        are converted to float.

    :raises ValueError: If less than 2 or more than 3 arguments are supplied.

    """

    def __add__(self, vector):
        """The addition of this point and a vector.

        :param vector: The vector to be added to the point.
        :type vector: Vector

        :rtype: Point

        """
        zipped = itertools.zip_longest(self, vector)  # missing values filled with None
        try:
            coordinates = [a + b for a, b in zipped]
        except TypeError:  # occurs if, say, a or b is None
            raise ValueError("Point and vector to add must be of the same length.")
        return Point(*coordinates)

    def __eq__(self, point):
        """Tests if this point and the supplied point have the same coordinates.

        A tolerance value is used so coordinates with very small difference
        are considered equal.

        :param point: The point to be tested.
        :type point: Point

        :raises ValueError: If points are not of the same length.

        :return: True if the point coordinates are the same, otherwise False.
        :rtype: bool

        """
        zipped = itertools.zip_longest(self, point)  # missing values filled with None
        try:
            result = [self._coordinates_equal(a, b) for a, b in zipped]
        except TypeError:  # occurs if, say, a or b is None
            raise ValueError("Points to compare must be of the same length.")
        return all(result)

    def __getitem__(self, index):
        return self._coordinates[index]

    def __init__(self, *coordinates):
        if len(coordinates) == 2 or len(coordinates) == 3:
            self._coordinates = tuple(float(c) for c in coordinates)
        else:
            raise ValueError("Point coordinates must have a length of 2 or 3")

    def __len__(self):
        return len(self._coordinates)

    def __lt__(self, point):
        """Tests if the coordinates of this point are lower than the supplied point.

        A tolerance value is used so coordinates with very small difference
        are considered equal.

        :param point: The point to be tested.
        :type point: Point

        :raises ValueError: If points are not of the same length.

        :return: True if the x coordinate of this point is lower than the
            supplied point, otherwise False. If both x coordinates are equal, then
            True if the y coordinate of this point is lower than the
            supplied point, otherwise False. For 3D points -> if both x and y coordinates
            are equal, then
            True if the z coordinate of this point is lower than the
            supplied point, otherwise False.
        :rtype: bool

        """
        zipped = itertools.zip_longest(self, point)  # missing values filled with None
        try:
            for a, b in zipped:
                if self._coordinates_equal(a, b):
                    continue
                return a < b
        except TypeError:  # occurs if, say, a or b is None
            raise ValueError("Points to compare must be of the same length.")

    def __repr__(self):
        return "Point(%s)" % ",".join([str(c) for c in self])

    # def __sub__(self, point_or_vector):
    #     """Subtraction of supplied object from this point.
    #
    #     :param point_or_vector: Either a point or a vector.
    #     :type point_or_vector: Point or Vector
    #
    #     :return: If a point is supplied, then a vector is returned (i.e. v=P1-P0).
    #         If a vector is supplied, then a point is returned (i.e. P1=P0-v).
    #     :rtype: Point2D or Vector2D
    #
    #     """
    #     zipped = itertools.zip_longest(self, point_or_vector)  # missing values filled with None
    #     try:
    #         coordinates = [a - b for a, b in zipped]
    #     except TypeError:  # occurs if, say, a or b is None
    #         raise ValueError(r'Point and point/vector to subtract must be of the same length.')
    #     if isinstance(point_or_vector, Point):
    #         return Vector(*coordinates)
    #     else:
    #         return Point(*coordinates)

    def _coordinates_equal(self, a, b):
        """Return True if a and b are equal within the tolerance value."""
        return math.isclose(a, b, abs_tol=1e-7)

    def project_2D(self, coordinate_index):
        """Projection of a 3D point as a 2D point.

        :param coordinate_index: The index of the coordinate to ignore.
            Use coordinate_index=0 to ignore the x-coordinate, coordinate_index=1
            for the y-coordinate and coordinate_index=2 for the z-coordinate.
        :type coordinate_index: int

        :raises ValueError: If coordinate_index is not between 0 and 2.

        :return: A 2D point based on the projection of the 3D point.
        :rtype: Point2D

        """

        if coordinate_index == 0:
            return Point(self.y, self.z)
        elif coordinate_index == 1:
            return Point(self.z, self.x)
        elif coordinate_index == 2:
            return Point(self.x, self.y)
        else:
            raise ValueError("coordinate_index must be between 0 and 2")

    def project_3D(self, plane, coordinate_index):
        """Projection of the point on a 3D plane.

        :param plane: The plane for the projection
        :type plane: Plane
        :param coordinate_index: The index of the coordinate which was ignored
            to create the 2D projection. For example, coordinate_index=0
            means that the x-coordinate was ignored and this point
            was originally projected onto the yz plane.
        :type coordinate_index: int

        :raises ValueError: If coordinate_index is not between 0 and 2.

        :return: The 3D point as projected onto the plane.
        :rtype: Point

        """

        if coordinate_index == 0:
            point = plane.point_yz(self.x, self.y)
        elif coordinate_index == 1:
            point = plane.point_zx(self.x, self.y)
        elif coordinate_index == 2:
            point = plane.point_xy(self.x, self.y)
        else:
            raise ValueError("coordinate_index must be between 0 and 2")

        return point

    @property
    def x(self):
        """The x coordinate of the point.

        :rtype: int, float

        """
        return self[0]

    @property
    def y(self):
        """The y coordinate of the point.

        :rtype: int, float

        """
        return self[1]

    @property
    def z(self):
        """The z coordinate of the point.

        :raises IndexError: If point is a 2D point.

        :rtype: int, float

        """
        return self[2]


class Point2D(Point):
    """A two-dimensional point, situated on an x, y plane.

    :param x: The x coordinate of the point.
    :type x: float
    :param y: The y coordinate of the point.
    :type y: float

    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self._x = x
        self._y = y

    def __add__(self, vector):
        """The addition of this point and a vector.

        :param vector: The vector to be added to the point.
        :type vector: Vector2D

        :rtype: Point2D

        """
        return Point2D(self.x + vector.x, self.y + vector.y)

    def __lt__(self, point):
        """Tests if the coordinates of this point are lower than the supplied point.

        :param point: The point to be tested.
        :type point: Point2D

        :return: True if the x coordinate of this point is lower than the
            supplied point, otherwise False. If both x coordinates are equal, then
            True if the y coordinate of this point is lower than the
            supplied point, otherwise False.
        :rtype: bool

        """
        if self.x < point.x:
            return True
        else:
            if self.x == point.x and self.y < point.y:
                return True
            else:
                return False

    def __repr__(self):
        """"""
        return "Point2D(%s)" % ",".join([str(round(c, 4)) for c in self.coordinates])

    @property
    def coordinates(self):
        """The coordinates of the point.

        :return: The x and y coordinates as a tuple (x,y)
        :rtype: tuple

        """
        return self.x, self.y

    @property
    def dimension(self):
        """The dimension of the point.

        :return: '2D'
        :rtype: str

        """
        return "2D"

    @property
    def x(self):
        """The x coordinate of the point.

        :rtype: float

        """
        return self._x

    @property
    def y(self):
        """The y coordinate of the point.

        :rtype: float

        """
        return self._y








class Color(object):
    def __init__(self, r=0, g=0, b=0):
        self._r = r
        self._g = g
        self._b = b

    def __repr__(self):
        return "Color components: R {}, G {}, B {}".format(self._r, self._g, self._b)

    def from_uint8_list(self, rgb):
        """Read in a rgb list to initialize the color values.

        Args:
            rgb: list/tuple/ndarray (3,)/(4,) RGB list whose values are in the range [0, 255].
                 The `A` (opacity) value could be given but omitted.

        Returns:
            Color object.

        Raises:
            NotImplementedError
        """
        if (
            isinstance(rgb, list)
            or isinstance(rgb, tuple)
            or isinstance(rgb, np.ndarray)
        ):
            assert len(rgb) >= 3
            self._r = self._regulate(rgb[0])
            self._g = self._regulate(rgb[1])
            self._b = self._regulate(rgb[2])
        else:
            raise NotImplementedError
        return self

    def from_float_list(self, rgb):
        """Initialize the Color object with the RGB list.

        Args:
            rgb: list/tuple/ndarray (3,) A list containing the values in range [0, 1]
                 that represent R, G, B, respectively.

        Returns:
            Color object.
        """
        self.from_uint8_list([c * 255 for c in rgb])
        return self

    @staticmethod
    def _regulate(c):
        c = math.floor(c) if c <= 255 else 255
        c = 0 if c < 0 else c
        return c

    @property
    def rgb(self):
        return [self._r, self._g, self._b]

    @property
    def bgr(self):
        return [self._b, self._g, self._r]

    def get_random_color(self):
        """Generate a random Color object."""
        hsv = (random.random(), 1, 1)
        return self.from_float_list(colorsys.hsv_to_rgb(*hsv))


class BBox(collections.abc.Sequence):
    def __init__(self, coordinates):
        """Construct a bounding box object with 4 values in the order:
        [top_left_x, top_left_y, bottom_right_x, bottom_right_y]

        Args:
            coordinates: (4, ) top_left_x, top_left_y, bottom_right_x, bottom_right_y
                               in either float type or int type.
        """
        if len(coordinates) != 4:
            raise IndexError(
                "The length of the given coordinates {} (type: {}) is not 4 but {}".format(
                    coordinates, type(coordinates), len(coordinates)
                )
            )
        self._bbox = [math.floor(v) for v in coordinates]

    def __getitem__(self, i: int):
        if i < 0 or i >= 4:
            raise IndexError
        return self._bbox[i]

    def __len__(self):
        return len(self._bbox)

    @property
    def width(self):
        """Return the width of the bounding box.

        Returns:
            int: The width of the bounding box.
        """
        return self._bbox[2] - self._bbox[0]

    @property
    def height(self):
        """Return the height of the bounding box.

        Returns:
            int: The height of the bounding box.
        """
        return self._bbox[3] - self._bbox[1]

    @property
    def xywh(self):
        """Return x, y of the top-left corner point in the pixel coordinates system (PCS) with the width and height
        of the bounding box.
        """
        return [
            self._bbox[0],
            self._bbox[1],
            self.width,
            self.height,
        ]

    @property
    def area(self):
        """Return the area of the bounding box.

        Returns:
            int: The area of the bounding box.
        """
        return self.width * self.height

    @property
    def xyxy(self):
        """Returns [top_left_x, top_left_y, bottom_right_x, bottom_right_y] in PCS.

        Returns:
            list[int, int, int, int]: [top_left_x, top_left_y, bottom_right_x, bottom_right_y].
        """
        return self._bbox

    @property
    def top_left_x(self):
        """Returns top_left_x in PCS.

        Returns:
            int: top_left_x.
        """
        return self._bbox[0]

    @property
    def top_left_y(self):
        """Returns top_left_y in PCS.

        Returns:
            int: top_left_y.
        """
        return self._bbox[1]

    @property
    def bottom_right_x(self):
        return self._bbox[2]

    @property
    def bottom_right_y(self):
        return self._bbox[3]

    def _draw_label(self, image, caption):
        """Draw the label caption on the image.

        Args:
            image:
            caption:

        Returns:
            np.ndarray: The painted image.
        """
        ret, baseline = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 1)
        cv2.putText(
            image,
            caption,
            (self.top_left_x, self.top_left_y + ret[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            1,
            lineType=cv2.LINE_AA,
        )
        return image

    def draw_on_image(self, image, color, caption):
        """Draw the bounding box on the image.

        Args:
            image:
            color:
            caption:

        Returns:
            np.ndarray: The painted image.
        """
        cv2.rectangle(
            image,
            (self.top_left_x, self.top_left_y),
            (self.bottom_right_x, self.bottom_right_y),
            color,
            1,
        )
        if caption:
            image = self._draw_label(image, caption)
        return image





class DetectionOutput(object):
    def __init__(
        self,
        bboxes,
        scores,
        labels,
    ):
        """

        Args:
            bboxes:
            scores:
            labels:
        """
        self._labels = labels
        self._bboxes = []
        self._scores = scores
        for bbox in bboxes:
            self._bboxes.append(BBox(bbox))


    def __len__(self):
        """Return the number of detected objects."""
        return len(self._labels)

    def __repr__(self):
        """"""
        return "Detected classes:\n %s" % ", ".join(
            "{} ({})\n".format(label, score)
            for label, score in zip(self._labels, self._scores)
        )

    def __getitem__(self, index):
        """"""
        if index >= self.__len__():
            raise IndexError

        return (
            self._labels[index],
            self._bboxes[index],
            self._scores[index],
        )



