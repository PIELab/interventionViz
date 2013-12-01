This is a set of python scripts designed to visualize data recorded with USF PIE-Lab's Android avatar wallpaper.

## Data ##
Some sample data is included in the /data directory; this should be pretty similar to the data coming in. First, let's discuss the raw data:

### GPS ###
GPS location is generally stored in the /GPSLogger folder. Here we should have .txt files with comma-separated date and long/lat values. There may be just one file with a full week of data or there may be on file for each day; it just depends on how the app was set up.

### Physical Activity ###
Physical activity data comes in two forms: mMonitor data (generally in the /miles folder) or fitbit data. 

*For mMonitor:*
Daily totals from mMonitor should be available for each day the app was run. Additionally, minute-level data should be recorded. There will also be second-level data files, but these should be empty. The file name corresponds to the day that the file was made, but files from later days also contain the previous days. This means that the simplest way to look at all of the data is to just load up the largest file (this is almost always the one with the latest date). 

*For Fitbit:*
Images of the fitbit website may be included, but raw data will not be available until the study is complete and the database(s) are downloaded. 

### Avatar-Influence Data ###
This file is almost always named dataLog.txt, and it contains a comma-separated description of when the avatar was shown on the phone. Included should be a starttime, endtime, and elapsed time as well as the name of the avatar animation that was displayed. 

## Script Organization ##

Scripts should be placed in packages named according to their vizualization goal. Subpackages with modules containing different interations or approaches of a type (such as time-series) are then defined.

Sample package organization:

```
src/				Top-level package
	__init__.py		Initialize the package
	settings.py 		Global Settings
	Utils/			Subpackage for internal use
		__init__.py
		iobuffer.py
		errors.py
		...
	interaction/		Subpackage for looking at interaction
		__init__.py
		timeSeries/	Sub-subpackage for interaction T.S.
			simple.py
			multicolorBars.py
			...
		dosage/
			dailyActiveOrPassive.py
			dailyPerActivity.py
			...
		...
	PA/			Subpack. for Physical Activity
		__init__.py
		timeSeries/
			line.py
			...
		heatMap/
			simple.py
			...
	Location/
		pathMap.py
		...
	...
```

To run a particular script, start from the top-level and do something like ```import src.interaction.timeSeries.simple```
