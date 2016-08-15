#orgrinAddr = "/usr/local/firmiana/leafy/static/images/tmp/ppi_tmp/firppi_1437880108.6/temp-ppi.txt"
#targetAddr = "/usr/local/firmiana/leafy/static/images/tmp/firppi_1437831961.42/temp-ppi"
#program-load-infomap = "/usr/local/firmiana/leafy/gardener/scripts/R/load-infomap.R"

library(parmigene)
Args <- commandArgs(TRUE)

input_file = Args[1]
out_file = Args[2]
expLen =  Args[3]

outfile_ppi_matrix = paste(out_file,"-matrix.txt",sep = "")
outfile_ppi_mat = paste(out_file,"-mat.txt",sep = "")
outfile_ppi_mi = paste(out_file,"-mi.txt",sep = "")
outfile_ppi_grn = paste(out_file,"-grn.txt",sep = "")
outfile_ppi_grn1 = paste(out_file,"-grn1.txt",sep = "")
outfile_ppi_result = paste(out_file,"-rank.txt",sep = "")

outfile_ppi_grn_flag = paste(out_file,"-grn-flag.txt",sep = "")

dataMatrix = read.table(input_file)

searchOrder = c('SMC1A','SMC3','RAD21','HDAC1','HDAC2','RBBP4','RBBP7')
searchLength = 5
#indexOfSearchOrder = c()
#for(i in 1:length(searchLength)){
#tempIndex = which(dataMatrix[,2]==searchOrder[i])
#if(length(tempIndex)==0)
#tempIndex = -1
#indexOfSearchOrder = append(indexOfSearchOrder,tempIndex)
#}

indexOfSMC1A    = which(dataMatrix[,2]=="SMC1A")
indexOfSMC3     = which(dataMatrix[,2]=="SMC3")
indexOfRAD21    = which(dataMatrix[,2]=="RAD21")
indexOfHDAC1  = which(dataMatrix[,2]=="HDAC1")
indexOfHDAC2  = which(dataMatrix[,2]=="HDAC2")
indexOfRBBP4  = which(dataMatrix[,2]=="RBBP4")
indexOfRBBP7  = which(dataMatrix[,2]=="RBBP7")
if(length(indexOfSMC1A)==0){indexOfSMC1A = -1}
if(length(indexOfSMC3)==0){indexOfSMC3 = -1}
if(length(indexOfRAD21)==0){indexOfRAD21 = -1}
if(length(indexOfHDAC1)==0){indexOfHDAC1 = -1}
if(length(indexOfHDAC2)==0){indexOfHDAC2 = -1}
if(length(indexOfRBBP4)==0){indexOfRBBP4 = -1}
if(length(indexOfRBBP7)==0){indexOfRBBP7 = -1}

mat = dataMatrix[ , -1:-2]
dimension = dim(mat)
n_row = dimension[1]
n_col = dimension[2]
#k = n_col-2
k = 3

mat = as.matrix(mat)
mat1 = mat
if(FALSE){
mat1[,] = 0
for(i in 1:n_row){
	row_sum = sum(mat[i])
	if(row_sum==0){
		row_sum=1
	}
	for(j in 1:n_col){
		mat1[i,j] = mat[i,j]/row_sum
	}
}
}

mi = knnmi.all(mat1, k=k, noise=1e-12)
grn = clr(mi)

#print rank result "SMC1A_SMC3__SMC1A"+"\t"+"SMC1A_RAD21__RAD21"+"\t"+"SMC3_RAD21__RAD21"+"\t"+"HDAC1_HDAC2__HDAC1"+"\t"+"RBBP4_RBBP7__RBBP4"+"\n"
if((indexOfSMC1A == -1)||(indexOfSMC3 == -1)){SMC1A_SMC3__SMC1A = -1}else{SMC1A_SMC3__SMC1A = which(sort(grn[indexOfSMC1A,])==grn[indexOfSMC1A,indexOfSMC3])/length(grn[indexOfSMC1A,])}
if((indexOfSMC1A == -1)||(indexOfRAD21 == -1)){SMC1A_RAD21__RAD21 = -1}else{SMC1A_RAD21__RAD21 = which(sort(grn[indexOfRAD21,])==grn[indexOfSMC1A,indexOfRAD21])/length(grn[indexOfRAD21,])}
if((indexOfSMC3 == -1)||(indexOfRAD21 == -1)){SMC3_RAD21__RAD21 = -1}else{SMC3_RAD21__RAD21 = which(sort(grn[indexOfRAD21,])==grn[indexOfSMC3,indexOfRAD21])/length(grn[indexOfRAD21,])}
if((indexOfHDAC1 == -1)||(indexOfHDAC2 == -1)){HDAC1_HDAC2__HDAC1 = -1}else{HDAC1_HDAC2__HDAC1 = which(sort(grn[indexOfHDAC1,])==grn[indexOfHDAC1,indexOfHDAC2])/length(grn[indexOfHDAC1,])}
if((indexOfRBBP4 == -1)||(indexOfRBBP7 == -1)){RBBP4_RBBP7__RBBP4 = -1}else{RBBP4_RBBP7__RBBP4 = which(sort(grn[indexOfRBBP4,])==grn[indexOfRBBP4,indexOfRBBP7])/length(grn[indexOfRBBP4,])}

ratioColumn = c()
ratioColumn = append(ratioColumn,SMC1A_SMC3__SMC1A)
ratioColumn = append(ratioColumn,SMC1A_RAD21__RAD21)
ratioColumn = append(ratioColumn,SMC3_RAD21__RAD21)
ratioColumn = append(ratioColumn,HDAC1_HDAC2__HDAC1)
ratioColumn = append(ratioColumn,RBBP4_RBBP7__RBBP4)

ratioMatrix = matrix(ratioColumn,searchLength,1,byrow = TRUE)
write.table(ratioMatrix,file = outfile_ppi_result,sep = "\t",row.names = F,col.names = F)

write.table(grn, file=outfile_ppi_grn, sep="\t", row.names=F, col.names=F)

flagData = matrix(data = 0, ncol = 3, byrow = TRUE, dimnames = NULL)
write.table(flagData, file=outfile_ppi_grn_flag, sep="\t", row.names=F, col.names=F)


if(FALSE){
dimension = dim(grn)
n_row = dimension[1]
n_col = 3
total = n_row*n_row*n_col
initData = runif(total,min=0,max=0)
n_row_new =  n_row*n_row
initMatrix = matrix(initData, nrow=n_row_new, ncol=n_col)
for(i in 1:n_row ){
	for(j in 1:n_row){
		if(i!=j){
			initMatrix[i][1] = i
			initMatrix[i][2] = j
			initMatrix[i][j] = grn[i][j]
		}
	}
}
write.table(initMatrix, file=outfile_ppi_grn1, sep="\t", row.names=F, col.names=F)
}








