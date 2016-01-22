#=============================================
# Solutions to pandas challenge
# Mark Servantes
#============================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Given data
rng = pd.date_range('1/1/2011', periods=72, freq='H')
ts = pd.Series(np.random.randn(len(rng)),index=rng)

#============Part 1===========================
#Create Data Frame from data
df = pd.DataFrame({'vals':ts})

#Return a Series with absolute difference < 0.5
new_series = ts[abs(ts.diff(1))<0.5]

#Plot and show histogram of the series
ts.hist()
plt.show()

#Rolling Average added as new column to data frame with 5 hour window
rolling_avg = pd.rolling_mean(df,5)
rolling_avg.columns = ['rolling_avg']
df = pd.concat([df,rolling_avg],axis=1)

#Change rolling_avg negatives to 0's
df.rolling_avg[df.rolling_avg<0]= 0

#===========Part 2=============================
#Save to Excel
writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
writer = pd.ExcelWriter('newfile.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

#Format col. width to 20; hide gridlines
worksheet.set_column('A:C', 20)
worksheet.hide_gridlines(2)

writer.save()




