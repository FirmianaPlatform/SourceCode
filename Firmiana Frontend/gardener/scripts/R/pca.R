# TODO: Add comment
# 
# Author: Wbflame
###############################################################################
setwd('/usr/local/firmiana/leafy/static/images/tmp/pca_tmp')
args<-commandArgs(TRUE) 
for (e in commandArgs()) {
	ta = strsplit(e,"=",fixed=TRUE)
	if(! is.na(ta[[1]][2])) {
		temp = ta[[1]][2]
		if(ta[[1]][1] == "input0") {
			input0=temp
		}
		
		if(ta[[1]][1] == "output") {
			output=temp
		}
		
		if(ta[[1]][1] == "jobid") {
			jobid=temp
		}
	} 
	
}

output_0=paste(output,"line1.png")
print(output_0)

data(iris)
head(iris)
round(cor(iris[,1:4]), 2)
pc <- princomp(iris[,1:4], cor=TRUE, scores=TRUE)
summary(pc)

png(output_0,width=500,height=500)
plot(pc,type="lines")
biplot(pc)
dev.off()


