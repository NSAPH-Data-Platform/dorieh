Shapefiles downloader
=====================

Python API to download shapefiles from US Census website.
Files to be downloaded are selected based on a desired year and
shapefiles collection.

If the desired year is not present in the requested collection,
the most recent prior year is used.

.. autoclass:: dorieh.gis.downloader.CensusShapeCollection
   :members:
   :undoc-members:


If HTTP Proxy is used the environment variable
`HTTPS_PROXY` must be defined.

Class GISDownloader
^^^^^^^^^^^^^^^^^^^

.. autoclass:: dorieh.gis.downloader.GISDownloader
   :members:
   :undoc-members:

