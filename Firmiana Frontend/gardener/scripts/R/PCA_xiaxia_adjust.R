# pca(input, input_metadata, output_pc, output_name)

Args <- commandArgs()
input_file = Args[6]
sampleInfo_file = Args[7]
cor_matrix_file = Args[8]
image_file = Args[9]
out_file_png   = paste(Args[9],".png",sep="")
out_file_pdf   = paste(Args[9],".pdf",sep="")


metadataList = unlist(strsplit(Args[11],";"))

data = read.table(input_file,header=T,stringsAsFactors=FALSE,sep="\t")
k3.cv=as.matrix(data[,-1])
ncol_data = ncol(k3.cv)
nrow_data = nrow(k3.cv)

k3.cv.t=t(k3.cv) #转置数据
k3.mat=as.numeric(k3.cv.t)#提取54个样本的数据
k3.mat=matrix(k3.mat,ncol_data,nrow_data)#将数据转换成矩阵格式
k3.mat.pr=prcomp(na.omit(k3.mat),cor=TRUE)#PCA分析
k3.mat.predict=predict(k3.mat.pr)#计算每一component的值


#print(dim(k3.mat))

sampleInfo = read.table(sampleInfo_file,header=T,sep="\t")
#rr = which(is.na(sampleInfo[,14])==1)
#sampleInfo = sampleInfo[1:ncol_data,]
# 'expName', 'species', 'instrument', 'dateOfExperiment', 'dateOfOperation', 'method','separation','sex','age','reagent','sample','tissueType','strain'
species = sampleInfo[,2]
instrument = sampleInfo[,3]
dateOfExperiment = sampleInfo[,4]
dateOfOperation = sampleInfo[,5]
method = sampleInfo[,6]
separation = sampleInfo[,7]
sex = sampleInfo[,8]
age = sampleInfo[,9]
reagent = sampleInfo[,10]
sample = sampleInfo[,11]
tissueType = sampleInfo[,12]
strain = sampleInfo[,13]

attr = cbind(species,instrument)
attr = cbind(attr,dateOfExperiment)
attr = cbind(attr,dateOfOperation)
attr = cbind(attr,method)
attr = cbind(attr,separation)
attr = cbind(attr,sex)
attr = cbind(attr,age)
attr = cbind(attr,reagent)
attr = cbind(attr,sample)
attr = cbind(attr,tissueType)
attr = cbind(attr,strain)

#print(attr[,c('instrument','dateOfExp')])
attr = attr[,metadataList]

rownames(k3.mat)=colnames(data)[2:ncol_data]

result = lm(k3.mat~as.factor(tumor)+as.factor(sample)+as.factor(DateOfExp))
res = residuals(result)
res2 = cbind(as.character(data[,1]),t(res))#6220Symbols + 54samples
colnames(res2)[1]=colnames(data)[1]
write.table(res2, output_Adjust,row.names=FALSE,sep="\t",quote=FALSE)


