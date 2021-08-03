from setuptools import setup, find_packages

setup(name="geots2img",
      version="0.0.1",
      description="Geo Time Series to Image",
      url="https://github.com/juliandehoog/geo-timeseries-to-image",
      author="Julian de Hoog",
      author_email='julian@dehoog.ca',
      license="Apache-2.0",
      packages=find_packages(),
      install_requires=[
            'pandas'],
      zip_safe=False)