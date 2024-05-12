# Dorieh Utilities (Python package)

[Documentation Home](https://nsaph-data-platform.github.io/nsaph-platform-docs/home.html)

There are open questions about how best to structure this package that we can address
(i.e. do we do multiple modules within this module, 1 single module, etc).

## Overview of Utilities

The nsaph_utils package is intended to hold python 
code that will be useful
across multiple portions of the NSAPH pipelines.

The included utilities are developed to be as independent of
specific infrastructure and execution environment as possible.

Included utilities:

* Interpolation code
* Reading FST files from Python [](members/pyfst)
* Reading FWF files [](members/fwf)
* various I/O wrappers [](members/io_utils)
* An API and CLI framework [](members/context)
* QC Framework
* Documentation utilities to simplify creation of consistent 
 documentation for NSAPH platform 


## Current Development

Updated 2/26/2021, Ben Sabath

- Interpolatation code: We have re-implemented the logic used for the 
  initial moving average interpolation used in the R based pipelines. 
  Developing better metholdologies remains to be done. Based on spot checks
  the results match those from the previous version.
  
## TODO
 
 Updated 2/26/2021, Ben Sabath
 
 - Generic `Data` object that other NSAPH modules can inherit from.
 - Creation of list of other useful general features
 - Review of already done development to see what would make sense to port to this package

(utils-indices)=
## Documentation Indices 

* [](genindex)
* [](modindex)
