**To Do:**
- [X] Script for extracting google sheet data and preprocessing it into a time series dataset
- [X] Do data exploration using tableau
- [ ] Do data exploration using pandas
- [ ] Experiment with OLS and other time series predictive modelling techniques
- [ ] Imapply machine learning to predict the potential confirmed cases in the future. (<i>waiting on more data for the days to come</i>)


### Code
- `data_prep.py` will save 3 files, 2 for the aggregated time series data (in csv and parquet format) and one for the summed confirms, deaths and recoveries by day for trendlining. 
- When the script is run, the files will be saved to a datafolder titled with the current date of extraction.