from datetime import datetime, date, time 
import pandas as pd
from dataclasses import dataclass
import os
import numpy as np

@dataclass
class Case:
  name: str
  values: list

class Country:
  def __init__(self, name: str, cases) -> None:
    self.name = name
    self.cases = []
    self.dataframe = pd.DataFrame([])

  def can_add(self):
    return True

  def add(self, case):
    if self.can_add():
      self.cases.append(case)
  
  def combine(self):
    for c in self.cases:
      print(c.name)
      self.dataframe[c.name] = c.values
    self.dataframe = self.dataframe.sort_values('date')
    self.dataframe['cumulative_cases'] = self.dataframe.new_confirmed_cases.cumsum()
    self.dataframe.insert(loc=0, column='day', value=np.arange(0, len(self.dataframe)))

class Report:
  def __init__(self, date, type) -> None:
    self.date = date
    self.type = type
    self.countries = []
    self.dataframe = pd.DataFrame([])

  def add(self, country: Country) -> None:
    self.countries.append(country)

  def combine(self):
    data = []
    for c in self.countries:
      c.combine()
      data.append(c.dataframe)
    self.dataframe = pd.concat(data)
      
  def save(self, out):
    data_folder = os.path.join('data', str(datetime.date(datetime.now())))
    save_dir = os.path.join(out, data_folder)
    if not os.path.exists(save_dir):
      os.system('mkdir -p ' + save_dir)

    print('Creating subdirectory for data...')
    print('...', save_dir)

    print('Saving...')
    csv_file_name = '{}_{}.csv'.format(self.type, datetime.date(datetime.now()))
    self.dataframe.astype(str).to_csv(os.path.join(save_dir, csv_file_name))
    print('...', csv_file_name)
    print('Done!')