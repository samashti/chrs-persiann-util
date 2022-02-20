# chrs-persiann-util

A utility to search, download global level PERSIANN precipitation data from [CHRS Data Portal](https://chrsdata.eng.uci.edu/)

## Overview

Center for Hydrometeorology and Remote Sensing (CHRS) at the University of California, Irvine (UCI) provides several
precipitation(rainfall) related datasets at a global scale that can be utilised for rainfall data analysis.

---

### PERSIANN

CHRS developed a system called Precipitation Estimation from Remotely Sensed Information using Artificial Neural
Networks (PERSIANN) to compute an estimate of rainfall data at each 0.25° x 0.25° pixel of the infrared brightness
temperature image provided by geostationary satellites useing neural network function classification/approximation
procedures.

**Data Period**: March 2000 - Present

**Coverage**: 60°S to 60°N

**Resolution**: 0.25° x 0.25°

**HTTP Download (full globe)**: [hourly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN/hrly/),
[3-hourly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN/3hrly/),
[6-hourly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN/6hrly/),
[daily](https://persiann.eng.uci.edu/CHRSdata/PERSIANN/daily/),
[monthly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN/monthly/),
[yearly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN/yearly/)

**FTP also available**: ftp://persiann.eng.uci.edu/CHRSdata/PERSIANN

**Latest Update**: Near real-time with 2 day delay

---

### PERSIAN-CCS

PERSIANN-Cloud Classification System (PERSIANN-CCS) is a real-time global high resolution (0.04° x 0.04° or 4km x 4km;)
satellite precipitation product. PERSIANN-CCS system enables the categorization of cloud-patch features based on
cloud height, areal extent, and variability of texture estimated from satellite imagery.

**Data Period**: January 2003 - Present

**Coverage**: 60°S to 60°N

**Resolution**: 0.04° x 0.04°

**HTTP Download (full globe)**: [hourly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN-CCS/hrly/),
[3-hourly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN-CCS/3hrly/),
[6-hourly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN-CCS/6hrly/),
[daily](https://persiann.eng.uci.edu/CHRSdata/PERSIANN-CCS/daily/),
[monthly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN-CCS/mthly/),
[yearly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN-CCS/yearly/)

**FTP also available**: ftp://persiann.eng.uci.edu/CHRSdata/PERSIANN-CCS

**Latest Update**: Real-time

---

### PERSIANN-CDR

PERSIANN-CDR (Precipitation Estimation from Remotely Sensed Information using Artificial Neural Networks - Climate
Data Record) provides daily rainfall estimates (near-global 37+ year high-resolution precipitation) at 0.25 deg for the latitude band 60N-60S over the period of 01/01/1983
to 12/31/2015 (delayed present). PERSIANN-CDR is aimed at addressing the need for a consistent, long-term,
high-resolution and global precipitation dataset for studying the changes and trends in daily precipitation,
especially extreme precipitation events, due to climate change and natural variability. PERSIANN-CDR is generated from
the PERSIANN algorithm using GridSat-B1 infrared data and adjusted using the Global Precipitation Climatology Project
(GPCP) monthly product to maintain consistency of the two datasets at 2.5 deg monthly scale throughout the entire
record.

**Data Period**: January 1983 - Present

**Coverage**: 60°S to 60°N

**Resolution**: 0.25° x 0.25°

**HTTP Download (full globe)**:
[daily](https://persiann.eng.uci.edu/CHRSdata/PERSIANN-CDR/daily/),
[monthly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN-CDR/mthly/),
[yearly](https://persiann.eng.uci.edu/CHRSdata/PERSIANN-CDR/yearly/)

**FTP also available**: ftp://persiann.eng.uci.edu/CHRSdata/PERSIANN-CDR

**Latest Update**: September 2020

---

### PDIR-Now

The Precipitation Estimation from Remotely Sensed Information using Artificial Neural Networks - Dynamic Infrared Rain
Rate near real-time (PDIR-Now) is a real-time global high resolution (0.04° x 0.04° or = 4km x 4km;) satellite
precipitation product. PDIR-Now has been implemented on the UCI CHRS global real-time satellite precipitation
monitoring system - [iRain](http://irain.eng.uci.edu).

PDIR-Now relies on the high frequency sampled IR imagery; consequently, the latency of PDIR-Now from the time of
rainfall occurrence is very short (15-60 mins). Additionally, PDIR-Now accounts for the errors and uncertainties that
result from the use of IR imagery by adopting a variety of techniques most notable is the dynamic shifting of (Tb-R)
curves using rainfall climatology. The short latency of PDIR-Now renders the dataset well-suited for near-real time
hydrologic applications such as flood forecasting and developing flood inundation maps.

**Data Period**: March 1st 2000 - Present

**Coverage**: 60°S to 60°N

**Resolution**: 0.04° x 0.04°

**HTTP Download (full globe)**: [hourly](https://persiann.eng.uci.edu/CHRSdata/PDIRNow/PDIRNow1hourly/),
[3-hourly](https://persiann.eng.uci.edu/CHRSdata/PDIRNow/PDIRNow2hourly/),
[6-hourly](https://persiann.eng.uci.edu/CHRSdata/PDIRNow/PDIRNow6hourly/),
[daily](https://persiann.eng.uci.edu/CHRSdata/PDIRNow/PDIRNowdaily/),
[monthly](https://persiann.eng.uci.edu/CHRSdata/PDIRNow/PDIRNowmonthly/),
[yearly](https://persiann.eng.uci.edu/CHRSdata/PDIRNow/PDIRNowyearly//)

**FTP also available**: ftp://persiann.eng.uci.edu/CHRSdata/PDIRNow

## Installation

You can install this module using the following methods;

```bash
python setup.py install
```

or, you could go the project directory that contains the setup.py and run the pip command as below.

```bash
pip install .
```

If you encounter a bug, please file an issue with steps to reproduce it on [Github](https://github.com/samashti/chrs-persiann-util/issues).
Please use the same for any feature requests, enhancements or suggestions.

## Example

Instructions for Parameters:

```python
"""
start (str): start date in 'yyyymmddHH' format
            HH for 1hrly - 00, 01, ---, 23

            HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

            HH for 6hrly - 00, 06, 12, 18

end (str): end date in 'yyyymmddHH' format
            HH for 1hrly - 00, 01, ---, 23

            HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

            HH for 6hrly - 00, 06, 12, 18

mailid (str): Mail Id of the user, requesting/placing an order for
            the CHRS Persiann Data

download_path (str): local path on the system where the file is
            downloaded.

file_format (str, optional): File format for the data to be downloaded.
            options:
                ArcGrid,
                Tif,
                NetCDF
            Defaults to 'Tif'.

timestep (str, optional): Time step/interval for the subsequent data
            files in the time period.
            options:
                1hrly,
                3hrly,
                6hrly,
                daily,
                monthly,
                yearly,
            Defaults to 'monthly'.

compression (str, optional): Download file format.
            options:
                zip,
                tar (in development)
            Defaults to 'zip'.
"""

```

Example Usage -

```python
from chrs_persiann import CHRS

params = {
    'start': '2021010100',
    'end': '2021010300',
    'mailid': 'test@gmail.com',
    'download_path': '~/Downloads',
    'file_format': 'Tif',
    'timestep': 'daily',
    'compression': 'zip'
}

dl = CHRS()

# PERSIANN
dl.get_persiann(**params)

# PERSIANN CCS
dl.get_persiann_ccs(**params)

# PERSIANN CDR
dl.get_persiann_cdr(**params)

# PDIR-Now
dl.get_pdir(**params)
```

You could alternatively, try running the `test_run.py` in the project root directory as
an example run.

```bash
python ./test_run.py
Querying data & Placing the order...
Query Params:

start date - 2021010100
end date - 2021010300
time step - daily
data type - PERSIANN
file format - Tif
compression format - zip
download path - ~/Downloads

Query complete.
Order Details - User IP: 12345678, File: 2022-02-19111423pm
Generating Data url...
File url Generated - https://chrsdata.eng.uci.edu/userFile/12345678/temp/PERSIANN/PERSIANN_2022-02-19111423pm.zip
Downloading compressed data file - /Users/user-name/Downloads/PERSIANN_2022-02-19111423pm.zip
Download Complete ------------------------------------------
```

## Author

Nikhil S Hubballi

[Mail](mailto:nikhil@samashti.tech) | [LinkedIn](https://www.linkedin.com/in/nikhilhubballi/) | [Twitter](https://twitter.com/samashti_)
