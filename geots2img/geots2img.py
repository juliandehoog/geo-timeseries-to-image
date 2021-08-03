import numpy as np
import os
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
import fiona
import geopandas as gpd
from shapely.geometry.point import Point
from sat import tools, RegionPlot
import pytz


class ImageGenerator:
    """ Generates an image based on a number of individual data points """

    def __init__(self, lat_range, lon_range, geo_res):
        # Set some defaults for class variables
        self.lat_range = lat_range
        self.lon_range = lon_range
        self.geo_res = geo_res
        self.points = []
        self.values = []
        self.cmap = plt.get_cmap('cividis')
        self.image = None

        # Create grid
        # Note that addition of self.geo_res/2 leads to proper bounds (it handles rounding issues)
        self.grid_x, self.grid_y = np.mgrid[
                                   self.lat_range[0]: self.lat_range[1] + self.geo_res / 2: self.geo_res,
                                   self.lon_range[0]: self.lon_range[1] + self.geo_res / 2: self.geo_res
                                   ]

    def set_points(self, points, values):
        """
        Set the individual points that will be used to generate the image
        @param points: np.array of [lon, lat] pairs
        @param values: np.array of [float] values
        @return: None
        """
        # Leave out any point-value pairs for which value is nan
        valid_points = []
        valid_values = []
        for point, value in zip(points, values):
            if value != value:
                continue
            valid_points.append(point)
            valid_values.append(value)
        self.points = valid_points
        self.values = valid_values

    def add_boundary_points(self, per_boundary=5):
        """
        Generates synthetic points along boundary of image using value of nearest point (for image smoothness)
        @param per_boundary: int representing number of boundary points for each side of image
        @return: None
        """
        boundary_points = []

        boundary_lat = np.linspace(self.lat_range[0], self.lat_range[1], num=per_boundary)
        boundary_lon = np.linspace(self.lon_range[0], self.lon_range[1], num=per_boundary)

        # Add top and bottom edges
        for lon in boundary_lon:
            boundary_points.append([boundary_lat[0], lon])
            boundary_points.append([boundary_lat[-1], lon])
        # Add left and right edges
        for lat in boundary_lat[1:-1]:
            boundary_points.append([lat, boundary_lon[0]])
            boundary_points.append([lat, boundary_lon[-1]])

        all_boundary_lat = [x[0] for x in boundary_points]
        all_boundary_lon = [x[1] for x in boundary_points]

        boundary_values = griddata(self.points, self.values,
                                   (all_boundary_lat, all_boundary_lon),
                                   method='nearest').ravel()

        self.points = np.append(self.points, boundary_points, axis=0)
        self.values = np.append(self.values, boundary_values, axis=0)

    def set_color_map(self, cmap):
        """ Set the color map """
        self.cmap = cmap

    def generate_image(self, flip_y=True):
        """
        Generate an image using existing class data and settings
        @param flip_y: bool (default True), whether to flip image across y-axis
        @return: None
        """

        # Fit surface to the grid using cubic function
        grid_z0 = griddata(self.points, self.values, (self.grid_x, self.grid_y), method='cubic')

        # Flip?
        if flip_y:
            grid_z0 = np.flip(grid_z0, 0)

        # If color map specified, convert to this
        if self.cmap is not None:
            grid_z0 = np.uint8([x * 255 for x in self.cmap(grid_z0)])

        self.image = Image.fromarray(grid_z0)

        return None

    def get_fitted_values(self, points):
        """
        Get values at each of the points after fitting a surface
        @param points: array of (float, float), pairs of lon, lat -- specifying points to return values for
        @return: array of float, indicating values at those points after surface fitting
        """
        lat = []
        lon = []
        for pt in points:
            lon.append(pt[0])
            lat.append(pt[1])
        return griddata(self.points, self.values, (lat, lon), method='cubic')

    def save_image(self, save_path):
        """ Save the image at specified path """

        # Ensure that the directory exists (and create it if it doesn't)
        head, tail = os.path.split(save_path)
        Path(head).mkdir(parents=True, exist_ok=True)

        # Save image
        self.image.convert('RGB').save(save_path)
