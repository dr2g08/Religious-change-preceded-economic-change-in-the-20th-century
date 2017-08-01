import pandas as pd
import numpy as np
import string
import os
import matplotlib.pyplot as plt
from scipy import stats

X=pd.read_csv('data/combinedVS_withX.csv',index_col=0)

# obtain metadata for individuals
cols=[i for i in X.columns.values if i[0] == 'S']
cols.extend([i for i in X.columns.values if i[0] == 'X'])

x=X.loc[:,cols]

# remove wave 1 from time series
xx=x.loc[:,'S020']
ii=np.where(xx >= 1987)[0]
x=x.iloc[ii,:]

country=x.loc[:,'S003']

country[country==688]=891
country[country==499]=891


year=x.loc[:,'X002']
age=x.loc[:,'X003']
survey=x.loc[:,'S020']

year[year.isnull()] = -5
age[age.isnull()] = -5
survey[survey.isnull()] = -5


#remove the individuals which don't have dob's
remove = np.where(year<0)[0]

print remove.shape

for r in remove:
    A=age.iloc[r]
    if A>0: year.iloc[r]=survey.iloc[r]-A


remove = np.where(year>0)[0]

jj=country.unique()

C=pd.read_csv('data/country_code.csv',index_col=0).iloc[:,0]
C=C.loc[jj]

country = C.loc[country]

Z=pd.read_csv('data/autonomy.csv',index_col=0)

# take out individuals that don't have dob
country=country.iloc[remove]
survey=survey.iloc[remove]
year=year.iloc[remove]
Z=Z.iloc[remove]

year=np.floor(year*0.1)*10

# make survey categories
survey[survey<1990]=1990
survey = np.floor(survey*0.2)*5



z=Z.iloc[:,0]
T=pd.DataFrame([survey.values,year.values,country.values,z.values],index=['survey','time','country','value']).T

generation=pd.DataFrame(index=country.unique(),columns=sorted(year.unique()))

for c in country.unique(): # for each country obtain a matrix informing us where we have available data 
    T1=T[T.loc[:,'country']==c]

    ts1=pd.DataFrame(index=sorted(year.unique()),columns=sorted(survey.unique()))
    err1=pd.DataFrame(index=sorted(year.unique()),columns=sorted(survey.unique()))

    for s in survey.unique():
        T2=T1[T1.loc[:,'survey']==s]

        for t in sorted(year.unique()):
            T3=T2[T2.loc[:,'time']==t]

            vals=T3.loc[:,'value'].values

            if len(vals) > 50:   
                ts1.loc[t,s]=vals.mean()
                #err1.loc[t,s]=alpha*vals.std()/(float(len(vals))**0.5)

    # only include the generations that appear in all the measured waves
    ii=ts1.isnull().sum(axis=1)
    ii=ii[ii<5].index.values

    jj=ts1.isnull().sum(axis=0)
    jj=jj[jj<11].index.values 

    #impute missing values to ensure unbiased descriptions of 
    for ssss in jj:
        g=ts1.loc[:,ssss]
        g2=g.loc[ii]

        time=np.where(~g2.isnull())[0]
        dep=g2.iloc[time]


        slope, intercept, r_value, p_value, std_err = stats.linregress(time,dep)

        time_fit=np.arange(len(g2))
        fit=slope*time_fit + intercept

        miss=np.where(g2.isnull())[0]
        g2.iloc[miss] = fit[miss]


        g.loc[ii]=g2
        ts1.loc[:,ssss]=g

    generation.loc[c,:]=ts1.mean(axis=1).values


directory='time_series/'
if not os.path.exists(directory):
    os.makedirs(directory)

generation.iloc[:,1:].to_csv(directory+'autonomy_dob.csv')
