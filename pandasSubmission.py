#=============================================
# Solutions to pandas challenge
# Mark Servantes
#============================================
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

def main():

    #Given data
    rng = pd.date_range('1/1/2011', periods=72, freq='H')
    ts = pd.Series(np.random.randn(len(rng)),index=rng)

    #============Part 1===========================
    #Create Data Frame from data
    df = pd.DataFrame({'vals':ts})
    print "\nPart 1: DataFrame of Data:\n"
    wait_for_user()
    print df

    #Return a Series with absolute difference < 0.5
    new_series = ts[abs(ts.diff(1))<0.5]
    print "\nPart 1: Return Series with absolute difference <0.5\n"
    wait_for_user()
    print new_series

    #Plot and show histogram of the series
    print "\nPart 1: Make Histogram of Series and Show Plot\n"
    wait_for_user()
    ts.hist()
    plt.show()

    #Rolling Average added as new column to data frame with 5 hour window
    rolling_avg = pd.rolling_mean(df,5)
    rolling_avg.columns = ['rolling_avg']
    df = pd.concat([df,rolling_avg],axis=1)
    print "\nPart 1: Add Rolling Average column to the DataFrame:\n"
    wait_for_user()
    print df

    #Change rolling_avg negatives to 0's
    df.rolling_avg[df.rolling_avg<0]= 0
    print "\nPart 1: Replace negative rolling average values with 0's:\n"
    wait_for_user()
    print df

    #===========Part 2=============================
    #Save to Excel
    writer = pd.ExcelWriter('newfile.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    #Format col. width to 20; hide gridlines
    worksheet.set_column('A:C', 20)
    worksheet.hide_gridlines(2)

    writer.save()
    print "\nPart 2: Save Data to Excel Files\n"
    print "\nDataFrame saved to Excel file: {0}\n".format('newfile.xlsx')
    wait_for_user()

    return

def wait_for_user():
    raw_input("Press Enter to continue...")

if __name__ == "__main__":
    main()


