library('lme4')
library('lmtest')

options(warn=-1)

dir<-'data/secularization/'

files<-list.files(dir)

data<-data.frame(matrix(NA, nrow = length(files), ncol = 3))

cnt<-1
for (f in files) {

    fn<-paste(dir,f,sep='')

    df<-read.table(fn,sep=',',row.names=1,header=TRUE)


    df$p <- as.factor(df$p) #set two variables as categorical variables 

    fit <- lm(S ~ t + p, data=df, REML=FALSE)
    nulla <- lm(S ~ t + p + t*p, data=df, REML=FALSE)
    
    LR<-lrtest(nulla,fit)
    
    #print(LR)
    
    LL<-LR$LogLik
    ll<-(LL[1]/LL[2])

    p_value<-LR$'Pr(>Chisq)'[2]
    
    r1<-summary(fit)$r.squared
    r2<-summary(nulla)$r.squared
    
    r<-(r2-r1)/r2
    
    
    #print(c(f,r,ll,p_value))
 
    
    
    data[cnt,] <- c(r,ll,p_value)
    
    
    cnt<-cnt+1
    
    }

colnames(data)=c('R2','lik ratio','p')
rownames(data)=files
write.table(data,'data/period_indep_secularization.csv',sep=',')

dir<-'data/personal_norms/'

files<-list.files(dir)

data<-data.frame(matrix(NA, nrow = length(files), ncol = 3))

cnt<-1
for (f in files) {

    fn<-paste(dir,f,sep='')

    df<-read.table(fn,sep=',',row.names=1,header=TRUE)


    df$p <- as.factor(df$p) #set two variables as categorical variables 

    fit <- lm(S ~ t + p, data=df, REML=FALSE)
    nulla <- lm(S ~ t + p + t*p, data=df, REML=FALSE)
    
    LR<-lrtest(nulla,fit)
    
    LL<-LR$LogLik
    ll<-(LL[1]/LL[2])

    p_value<-LR$'Pr(>Chisq)'[2]
    
    r1<-summary(fit)$r.squared
    r2<-summary(nulla)$r.squared
    
    r<-(r2-r1)/r2
    
    
    #print(c(f,r,ll,p_value))
 
    
    
    data[cnt,] <- c(r,ll,p_value)
    
    
    cnt<-cnt+1
    
    }

colnames(data)=c('R2','lik ratio','p')
rownames(data)=files
write.table(data,'data/period_indep_personal_norms.csv',sep=',')

dir<-'data/individualism/'

files<-list.files(dir)

data<-data.frame(matrix(NA, nrow = length(files), ncol = 3))

cnt<-1
for (f in files) {

    fn<-paste(dir,f,sep='')

    df<-read.table(fn,sep=',',row.names=1,header=TRUE)


    df$p <- as.factor(df$p) #set two variables as categorical variables 

    fit <- lm(S ~ t + p, data=df, REML=FALSE)
    nulla <- lm(S ~ t + p + t*p, data=df, REML=FALSE)
    
    LR<-lrtest(nulla,fit)
    
    LL<-LR$LogLik
    ll<-(LL[1]/LL[2])

    p_value<-LR$'Pr(>Chisq)'[2]
    
    r1<-summary(fit)$r.squared
    r2<-summary(nulla)$r.squared
    
    r<-(r2-r1)/r2
    
    
    #print(c(f,r,ll,p_value))
 
    
    
    data[cnt,] <- c(r,ll,p_value)
    
    
    cnt<-cnt+1
    
    }

colnames(data)=c('R2','lik ratio','p')
rownames(data)=files
write.table(data,'data/period_indep_individualism.csv',sep=',')
