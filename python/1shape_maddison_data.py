import pandas as pd
import numpy as np
import string

X=pd.read_excel('data/mpd_2013-01.xlsx',index_col=0)
columns=X.iloc[1,:].values

X=X.iloc[2:,:]
X.columns=columns
X=X.T

#only include years from 1900 onwards
X=X.iloc[:,88:]
countryN=X.index.values

countryN[122] = 'Turkey'

#remove headers that = nan
ii=[]
for i,c in enumerate(countryN):
    b=type(c) == np.float64
    if b == False:
        ii.append(i)

X=X.iloc[ii,:]

countryN=X.index.values

#change country names to convential strings
J=[]
for cn in countryN:
    cn=cn.rstrip()
    try:
        cn=cn.decode('utf-8')
        J.append(str(cn))
    except UnicodeError:
        J.append(cn)
        
X.index=J

countryN=X.index.values

country=pd.read_csv('data/mean.csv',index_col=0).index.values

#change country names and include only WVS countries

real=['Ethiopia', 'Great Britain', 'Indonesia', 'Italy',
       'Netherlands', 'New Zealand', 'Palestine',
       'Serbia and Montenegro', 'South Africa', 'South Korea',
       'Trinidad and Tobago', 'United States', 'Viet Nam']

old=['Eritrea & Ethiopia','England/GB/UK','Indonesia (Java before 1880)','(Centre-   North)           Italy',
    'Holland/     Netherlands','N. Zealand','W. Bank & Gaza','Serbia','Cape Colony/ South Africa',
    'S. Korea','T. & Tobago','USA','Vietnam']


for r,o in zip(real,old): countryN[countryN==o] = r
    
X.index=countryN


GDP=X.loc[country,:] # include only WVS questions

#shift the values down 10 years to test the scaricity hypothesis

window=10

GDP_c=pd.DataFrame(index=GDP.index.values,columns=np.linspace(1870,2000,14))

for i in range(14):
    start=i*window
    end=(i*window)+window
    
    
    x=GDP.iloc[:,start:end].mean(axis=1).values
    
    GDP_c.iloc[:,i] = x
 
GDP_c.to_csv('data/historic_GDP_TS_compressed.csv')
