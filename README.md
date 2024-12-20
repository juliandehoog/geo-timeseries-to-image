# geo-timeseries-to-image


## Summary

This python package provides some simple tools to process and visualise
sets of time series data that have a geospatial relationship with one another.

Example of such datasets could include:
- temperature measurements at different weather stations, or
- solar power generation at different homes having rooftop solar PV

This package uses existing interpolation packages to interpolate between individual
point sources in 2D space (such as weather stations).  Currently supported:
-  `scipy.interpolate.griddata`
-  `scipy.interpolate.RBFInterpolator`   

It also provides an ability to add boundary points, which means that values can be estimated for 
entire rectangular regions, even with only a small number of time series data sources within the region.

The 2D data that is generated from interpolation can either be accessed as a 2D numpy array
of float values, or it can be displayed as a visual image.  There is basic support to
generate a sequence of images from time series data.

---

## Install

```bash
pip install geots2img
```

Or if you prefer to install this locally (in development mode), run:
```bash
git clone git@github.com:juliandehoog/geo-timeseries-to-image.git
make local-install
```

---

## Description

The core functionality is provided within the `ImageGenerator` class.  When creating 
an instance of ImageGenerator, you must pass the range of x and y values (max, min for each)
that you are interested in, as well as the resolution of the image (the spatial discretisation interval).

You must also pass the coordinates of the source points, in other words the locations where
the time series data is being generated.  To use the example of weather stations, this would be
the longitude / latitude of each weather station.

The `ImageGenerator` can subsequently be passed the instantaneous values of all source points
and generate an image (or 2D array of float values) for the whole area of interest.   The accompanying 
jupyter notebook [`example_usage.ipynb`](examples/example_usage.ipynb) provides
detailed examples of how this package may be used.

In short:

**Input**:

- [x_min, x_max], [y_min, y_max], defining a region of interest
- target resolution of region of interest (spatial discretisation)
- (x, y) coordinates for all points that generate data within the region
- values at each of these points for one or more intervals

**Output**:

Any of the following:

- A 2D numpy array of values for the entire region
- A list of values for a set of points of interest within the region (do not have to be the same as the source points)
- An image that visualises data across the whole region
- A sequence of images or a video that visualises the time series data in the region over multiple time intervals

---

## Example

Consider if we have temperature time series data like this (each time series
correponds to temperature measurements at one postcode in Western Australia):

![](examples/example_data.png)

We can choose one interval, say 2-Nov-2020 12:00, and convert it to an image like this:

![](examples/example_image_annotated.png)

In the figure above, green circles indicates locations of source data (where temperature was measured),
while red circles indicate boundary points that are synthetically added to ensure that we
can interpolate reasonably well across the whole region of interest.

After converting each interval to an image, we can represent the full period of interest
as a video, like this:

![](examples/example_video.gif)

In this particular example (one day of temperature data), the visualisation is not that 
interesting in the end -- although it does indicate that one postcode seems to have either 
faulty sensors or unique characteristics. However, for other types of time series data 
(like solar PV generation, for example), these types of visualisation can be very helpful.


---

## Release History

- **0.2.1** - Type hints and other small code improvements
- **0.2.0** - Added RBFInterpolator support, multiple small improvements to structure
- **0.1.3** - Fixed minor issue with nans at edge of fitted values
- **0.1.2** - Fixed makefile, setup, etc. for deployment to pypi
- **0.1.1** - Multiple minor fixed, improved README, thanks to [Peter Ilfrich](https://github.com/ilfrich) 
  for the suggestions
- **0.1.0** - First fully functional release.

---
