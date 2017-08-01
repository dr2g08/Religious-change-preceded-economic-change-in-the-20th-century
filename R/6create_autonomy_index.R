library(psych)

#fit the factor analysis model and extract and save the values of interest
D<-read.table(file="data/combinedVS_withX.csv",sep=',',header=TRUE,row.names=1)[1:69]

D<-D[c("A029", "A039","A042")]
D[D<0]<-NA

fit <- principal(D, nfactors=1,missing=TRUE)#, rotate='oblimin')

x<-fit$values
load<-fit$loadings
scores<-fit$scores

write.table(scores,file='data/autonomy.csv',sep=',')
