import pandas as pd
import numpy as np
import string
import os

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

#recode serbia and montenegro
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

survey[survey<1990]=1990
survey=np.floor(survey/5)*5

cu=country.unique()

z=Z.iloc[:,0]

T=pd.DataFrame([survey.values,year.values,country.values,z.values],index=['survey','time','country','value']).T

for c in cu:
    
    T1=T[T.loc[:,'country']==c]

    ts1=pd.DataFrame(index=sorted(year.unique()),columns=sorted(survey.unique()))                  

    for s in survey.unique():
        T2=T1[T1.loc[:,'survey']==s]

        for t in sorted(year.unique()):
            T3=T2[T2.loc[:,'time']==t]
            vals=T3.loc[:,'value'].values

            if len(vals) > 100:   
                ts1.loc[t,s]=vals.mean()
    

                
    directory='autonomy_tvp/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    ts1.to_csv(directory+c+'.csv')
