Developing with MPilot
======================

This documentation covers using MPilot as a Python library, in order to: parse, run, create, and modify MPilot models;
implement custom MPilot commands and parameter types; and integrate MPilot functionality into other software. It
assumes that you are familiar with writing Python code and installing Python packages using pip.

Installing MPilot
-----------------

Install MPilot using pip::

  pip install mpilot

If you plan to use NetCDF data in your MPilot models, you should install the NetCDF extra::

  pip install mpilot[netcdf]

.. note::

  Installing MPilot with NetCDF will require the NetCDF C library to already be installed on your computer. Installing
  the NetCDF C library is out of the scope of this document, but you can find more information about doing this in the
  `NetCDF documentation`_.

.. toctree::
   :hidden:
   :includehidden:

   reference/parser
   reference/program

.. _NetCDF documentation: https://www.unidata.ucar.edu/software/netcdf/docs/getting_and_building_netcdf.html
