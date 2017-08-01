#load the dataframe to be compressed
library(psych)

D<-read.table(file="data/combinedVS_withX.csv",sep=',',header=TRUE,row.names=1)[,1:70]
D[D<0] <- NA # set missing values (negatives) to nas

#fit the factor analysis model and extract and save the values of interest
fit <- fa(D, nfactors=9, rotate='oblimin',fm='ml',missing=TRUE)

x<-fit$values
load<-fit$loadings
scores<-fit$scores

write.table(load,file='data/loadings.csv',sep=',')
write.table(scores,file='data/values_PCA.csv',sep=',')
write.table(x,file='data/eigen_v_comp.csv',sep=',')
