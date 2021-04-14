import os

class SingletonConfig(object):
	_instance = {}
	"""docstring for SingletonConfig"""
	def __call__(sngl, *args, **kwargs):
		if sngl not in sngl._instance:
			cls._instance[sngl] = super(SingletonConfig, sngl).__call__(*args, **kwargs)
		return sngl._instance[sngl]
		
	#
	# CLI 
	#
	SCRIPT = '/pipeline.sh'
	LIST_SCRIPT = '/pipeline.sh'


	#
	# DATA PREP
	#
	REPO = 'https://github.com/CSSEGISandData/COVID-19.git'
	TMP_FOLDER = '/tmp/corona/'
	TMP_GIT = os.path.join(TMP_FOLDER, REPO.split('/')[-1].split('.')[0])
	DATA = os.path.join(TMP_GIT, 'csse_covid_19_data', 'csse_covid_19_daily_reports')
	LOG_TOP_N_COUNTRIES = 10


	#
	# FORECASTING
	#
	DAYS_IN_FUTURE = 10 # Amount of days you want to forecast into future
	PERC_SPLIT = 0.95   # Train / test split for forecasting model.

	#
	# DATA VISUALIZATION
	#
	FIG_SIZE = (14,10)


	#Github cols
	KEEP_COLS = ['country',
	             'province', 
	             'confirmed',
	             'deaths',
	             'recovered',
	             'date',
	             'datetime',
	             'file_date']

	NUMERIC_COLS = ['confirmed', 
	                'deaths', 
	                'recovered']

