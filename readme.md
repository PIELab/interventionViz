This is a set of python scripts designed to visualize data recorded with USF PIE-Lab's Android avatar wallpaper.

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
