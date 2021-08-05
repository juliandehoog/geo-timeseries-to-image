# geo-timeseries-to-image


This python package provides some simple tools to process and visualise
sets of time series data that have a geospatial relationship with one another.

Example of such datasets could include:
- temperature measurements at different weather stations, or
- solar power generation at different homes having rooftop solar PV

This package uses `scipy.interpolate.griddata` to interpolate between individual
point sources (such as weather stations).  It also provides an ability to add
boundary points, which means that values can be estimated for entire rectangular
regions, even with only a small number of time series data sources.

The 2D data that is generated from interpolation can either be accessed as a 2D numpy array
of float values, or it can be displayed as a visual image.  There is basic support to
generate a sequence of images from time series data, convert these into a video.

---

## Install

To install this locally, run:

```bash
git clone git@github.com:juliandehoog/geo-timeseries-to-image.git
make local-install
```

---

## Usage

Typical usage is described in the accompanying jupyter notebook [`example_usage.ipynb`](examples/example_usage.ipynb).

---

## Release History

- **0.1.0** - First fully functional release.

---
