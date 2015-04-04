### congress-education 

This repository contains data and statistical analysis on the education levels of members of U.S. congress from 1967 - 2015. They are organized as:

	/analysis : scripts for statistical analysis
	/data : raw data files
	/graphs : graphs and charts
	/scrape : tools for scraping and wrangling data
	/visual : scripts for building graphs and charts
	codebook.txt : data codebook

## Build

To build the data set, run:

	cd scrape &&  make

#### License

The data, which is acquired from [bioguide.congress.gov](http://bioguide.congress.gov), is in the public domain.

The code is under the [GNU General Public License, Version 3](https://www.gnu.org/copyleft/gpl.html).
