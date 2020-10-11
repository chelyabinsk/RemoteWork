import pandas as pd
import numpy as np

df = pd.read_csv('Data/2020-08-23.csv')
sub_df = df.loc[(df['live']==True) ,['timestamp','viewers','channel_name']]
sub_df[['timestamp']] = pd.to_datetime(sub_df['timestamp']+60*60*2,unit='s')

tmp = list(sub_df['timestamp'])[0].date()
year = tmp.year
month = str(tmp.month).rjust(2,'0')
day = str(tmp.day).rjust(2,'0')
out_name = '{}-{}-{}.csv'.format(year,month,day)
export_df = sub_df.pivot_table(values='viewers', index=['timestamp'],columns='channel_name', aggfunc=np.sum)
sub_df.to_csv(out_name,index=None)


#import pandas as pd
#

# sample dataframe to match OPs structure
#df = pd.DataFrame({'Date' : [pd.Timestamp('20130102'), pd.Timestamp('20130102'), 
#                    pd.Timestamp('20130103'), pd.Timestamp('20130103'),
#                    pd.Timestamp('20130103'), pd.Timestamp('20130103'),
#                    pd.Timestamp('20130103'), pd.Timestamp('20130103'),
#                    pd.Timestamp('20130104'), pd.Timestamp('20130104'),
#                    pd.Timestamp('20130105'),pd.Timestamp('20130106')],
#                    'ID' : [1, 3, 1, 2, 1 , 3,3,4,4,4,1,2],
#                    'Category' : pd.Categorical(["A","B","C","B","B","A",
#                                                 "A","A","B","C","B","A"  ])})
# data munging to get OPs desired plot
#df = sub_df.pivot_table(values='viewers', index=['timestamp'],columns='channel_name', aggfunc=np.sum)
#df2 = pd.pivot_table(df, values='ID', index=['Date'],columns='Category', aggfunc=np.sum)

