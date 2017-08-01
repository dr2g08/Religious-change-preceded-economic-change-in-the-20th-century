import pandas as pd
import numpy as np
import os

source=['autonomy_tvp/','tolerance_tvp/','secular_tvp/']
dest=['individualism','personal_norms','secularization']

for fn,d in zip(source,dest):
    l=os.listdir(fn)

    for f in l:

        X=pd.read_csv(fn+f,index_col=0)

        ii=X.isnull().sum()

        if len(ii[ii<11]) > 1:
            ii=np.where(ii<11)[0]

            X=X.iloc[:,ii]

            ii=X.isnull().sum(axis=1)
            ii=np.where(ii!=X.shape[1])[0]

            X=X.iloc[ii,:]

            X.index=range(1,X.shape[0]+1)
            X.columns=range(1,X.shape[1]+1)

            X=X.unstack()
            p=X.index.labels[0]+1
            t=X.index.labels[1]+1
            ii=np.where(~X.isnull())[0]
            X=X.values
            X=pd.DataFrame([X,t,p],index=['S','t','p']).T
            X=X.iloc[ii,:]
            
            directory='data/'+d+'/'
            if not os.path.exists(directory):
                os.makedirs(directory)

            X.to_csv('data/'+d+'/'+f)
