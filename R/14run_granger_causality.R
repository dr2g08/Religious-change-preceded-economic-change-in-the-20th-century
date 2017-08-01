library('lme4')

dir='data/autoregression/'

files=list.files(dir)

for (l in files) {
    
    fn=paste(dir,l,sep='')

    ts2<-read.table(fn,sep=',',header=TRUE,row.names=1)
    ts2$country<-as.factor(ts2$country)


    fit<-lmer(dep~dep_lag+pred_lag+(1|country),data=ts2,REML=TRUE)

    print(l)

    print(summary(fit))

    null<-lmer(dep~ dep_lag + (1|country),data=ts2,REML=TRUE)
    print(anova(fit,null))

    null<-lm(dep~dep_lag+pred_lag,data=ts2)
    print(anova(fit,null))

    print('--------------------------------------------------------------------')
    print('endendendendendendendendendendendendendendendendendendendendendendendendend')
    print('--------------------------------------------------------------------')
    

}
