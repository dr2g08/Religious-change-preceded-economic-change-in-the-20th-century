import numpy as np
import string
import pandas as pd

#load the value based questions for WVS and EVS

#1981 or 1990 start?
startE = 1 
startW = 1

# the interesting question types
cate=list(string.ascii_uppercase)[:9]
cate.extend('S')
cate.extend('X')

Eq=pd.read_csv('data/EVS_question_lookup.csv',index_col=0).iloc[:,startE+3:5]
index=[i for i in Eq.index.values if i[0] in cate]
Eq=Eq.loc[index,:]

Eq=Eq.where((~pd.notnull(Eq)), '                             ')
Eq=Eq.where((pd.notnull(Eq)), '')


Wq=pd.read_csv('data/WVS_question_lookup.csv',index_col=1).iloc[4:,startW+2:]
index=Wq.index.values
index=[i for i in index if isinstance(i, basestring)]
index=[i for i in index if i[0] in cate]
Wq=Wq.loc[index,:]


ii=np.intersect1d(Eq.index.values,Wq.index.values)

Eq=Eq.loc[ii,:]
Wq=Wq.loc[ii,:]

EW=pd.concat([Eq,Wq],axis=1)


for i in EW.index.values:
    xx=EW.loc[i,:]

    xx=xx.str.len()
    xx[xx<5]=0
    xx[xx>=5]=1

    EW.loc[i,:]=xx

lookup=pd.read_csv('data/EVS_question_lookup.csv',index_col=0).loc[EW.index.values,:].iloc[:,0]

cnt=EW.sum(axis=1)

ii=cnt[cnt>=EW.shape[1]]

ii=lookup.loc[ii.index.values]


WVS=pd.read_stata('data/WVS.dta',convert_categoricals=False)
kk=WVS.loc[:,'S020'] # remove wave 1
WVS=WVS[kk>1988]


EVS=pd.read_stata('data/EVS.dta',convert_categoricals=False)
kk=EVS.loc[:,'S020'] # remove wave 1
EVS=EVS[kk>1988]


E=EVS.loc[:,ii.index.values]
W=WVS.loc[:,ii.index.values]

withX=pd.concat([W,E],axis=0)

withX.index=range(len(withX))

withX.to_csv('data/combinedVS_withX.csv')
