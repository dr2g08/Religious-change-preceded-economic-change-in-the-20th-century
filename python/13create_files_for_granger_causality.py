import pandas as pd
import numpy as np
import os

#set up the dataframes for the key variables
old_years=[1870.0,1880.0,1890.0]

SEC=pd.read_csv('time_series/secular_dob.csv',index_col=0)
TRPB=pd.read_csv('time_series/tolerance_dob.csv',index_col=0)
IND=pd.read_csv('time_series/autonomy_dob.csv',index_col=0)


#normalise the standard deviation to 1
SEC=SEC/SEC.unstack().std()
TRPB=TRPB/TRPB.unstack().std()
IND=IND/IND.unstack().std()

#add empty values to 
SEC[2000.0] = np.nan
TRPB[2000.0] = np.nan
IND[2000.0] = np.nan

add=pd.DataFrame(np.nan,columns=old_years,index=SEC.index.values)

SEC=pd.concat([add,SEC],axis=1)
TRPB=pd.concat([add,TRPB],axis=1)
IND=pd.concat([add,IND],axis=1)

GDP=pd.read_csv('data/historic_GDP_TS_compressed.csv',index_col=0)
GDP.columns=[float(a) for a in GDP.columns.values]

#set GDP so it's in $1000's
GDP=GDP/1000.

# function to derive dataframes for the big regressions 
#def autoregression_dataframe(SEC,GDP,dep,pred,lag):

def granger_randomeffect(SEC,GDP,pred,dep,lag):
    start=3

    #get column names
    columns=[dep]
    for v in [pred,dep]: columns.append(v+'_lag')

    Z=pd.DataFrame(columns=columns) # create dataframe

    #add the columns
    cnt=0

    sec=SEC.iloc[:,start:]
    Z.iloc[:,cnt]=sec.values.flatten()
    cnt+=1

    gdp=GDP.iloc[:,start-lag:-lag]
    Z.iloc[:,cnt]=gdp.values.flatten()
    cnt+=1

    sec=SEC.iloc[:,start-lag:-lag]
    Z.iloc[:,cnt]=sec.values.flatten()
    cnt+=1


    country=[]
    for c in GDP.index.values: country.extend([c]*(GDP.shape[1]-start)) 
    Z.loc[:,'country']=country


    #remove missing
    ii=Z.isnull().sum(axis=1)
    ii=np.where(ii==0)[0]
    Z=Z.iloc[ii,:]

    print 'lag = ' + str(lag)
    print 'countries = ' + str(len(Z.loc[:,'country'].unique()))
    print 'data points = ' + str(len(ii))
    print '-------------'

    return Z 


directory='data/autoregression/'
if not os.path.exists(directory):
    os.makedirs(directory)

models=zip(['GDP','SEC','TRPB','SEC','IND','SEC'],
           ['SEC','GDP','SEC','TRPB','SEC','IND'],
           [GDP,SEC,TRPB,SEC,IND,SEC],
           [SEC,GDP,SEC,TRPB,SEC,IND])


for pred,dep,PRED,DEP in models:
    for lag in range(1,4):
        print 'dependent = ' + dep
        print 'predictor = ' + pred
        Z=granger_randomeffect(DEP,PRED,'pred','dep',lag)
        fn=dep + '_' + pred+str(lag*10)+'.csv'
        Z.to_csv('data/autoregression/'+fn)
    


