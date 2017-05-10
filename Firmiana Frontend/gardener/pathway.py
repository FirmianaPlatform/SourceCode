import os, zipfile, tempfile, time,json
import string
from rpy2 import robjects as ro
from rpy2.robjects.packages import importr
import commands
import scipy
import numpy as np
import math
from scipy.stats  import pearsonr
import signif
from django.core.serializers.json import DjangoJSONEncoder
from PIL import Image
r = ro.r
tmpdir = '/usr/local/firmiana/leafy/static/images/tmp/'
binRSCRIPT = '/usr/bin/Rscript'
Rscript_location = '/usr/local/firmiana/leafy/gardener/scripts/R/'
leafy_location = '/usr/local/firmiana/leafy'

def kegg_pathview(dataSource, parameters):
    
    temp_speciesName = parameters['species']
    
    #species name
    specedict={'human':'hsa',
               'mouse':'mmu', 
               'rat':'rat', 
               'xenopus':'xla'}
    speciesName=specedict[temp_speciesName]
    
    #species DB in accord (accordance) with species name
    #speciesDb = parameters['speciesDb']
    speciesDbdict = {'human':'org.Hs.eg.db', 
                     'mouse':'org.Mm.eg.db', 
                     'rat':'org.Rn.eg.db', 
                     'xenopus':'org.Xl.eg.db'}
    speciesDb = '"' + speciesDbdict[temp_speciesName] + '"'
    
    #transformational table from gene to geneSymbol
    #egSYMBOL2EG = parameters['egSYMBOL2EG']
    egSYMBOL2EGdict = {'human':'org.Hs.egSYMBOL2EG', 
                       'mouse':'org.Mm.egSYMBOL2EG', 
                       'rat':'org.Rn.egSYMBOL2EG', 
                       'xenopus':'org.Xl.egSYMBOL2EG'}
    egSYMBOL2EG = egSYMBOL2EGdict[temp_speciesName]
    
    #egPATH
    #egPATH = parameters['egPATH']
    egPATHdict = {'human':'org.Hs.egPATH', 
                  'mouse':'org.Mm.egPATH', 
                  'rat':'org.Rn.egPATH', 
                  'xenopus':'org.Xl.egPATH'}
    egPATH = '"' + egPATHdict[temp_speciesName] + '"'
    
    pre = '{0}kegg_tmp/firkegg_{1}/'.format(tmpdir, time.time())
    # pre='/usr/local/firmiana/leafy/static/images/'
    os.mkdir(pre)
    ro.r.setwd(pre)  # create tempfile
    # save tempfile
    tempfileName = "temp" + speciesName + ".txt"
    tempfile = open(tempfileName, "w")
    
    for line in dataSource:
        # print line
        for ele in range(len(line)):
            if ele != len(line) - 1:
                tempfile.write(str(line[ele]) + "\t")
            else:
                tempfile.write(str(line[ele]) + "\n")
    tempfile.close()
    # species_name = "'" +  "mmu" + "'"
    species_name = "'" + speciesName + "'"
  
    # fileAddress = "'" + "/home/galaxy/Documents/liverCells_coagulation.txt" + "'"+',header=T,stringsAsFactors=FALSE,sep="\\t")        #1-6col'
    fileAddress = "'" + pre + tempfileName + "'" + ',header=T,stringsAsFactors=FALSE,sep="\\t")'
  
    # rscript
    rscript1 = """
    #import packages
    library(""" + speciesDb + """) #*speciesDb
    library("GSEABase")
    library("GOstats")
    library("pathview")

    #read datasource
    coagulation = read.table(
    """
    rscript2 = """
    
    #mactch geneSymbol in KEGG-Library
    genes = coagulation[,1]
    entrezIDs <- mget(genes, """ + egSYMBOL2EG + """, ifnotfound=NA)        #Return the value of a named object {base} #**egSYMBOL2EG
    entrezIDs <- as.character(entrezIDs)
    keggAnn <- get(""" + egPATH + """)  #**egPATH                                                                #Return the value of a named object {base}
    universe <- Lkeys(keggAnn)                                                                        #AnnotationDbi
    params <- new("KEGGHyperGParams", geneIds=entrezIDs, universeGeneIds=universe, annotation=""" + speciesDb + """, categoryName="KEGG", pvalueCutoff=0.01,testDirection="over")
                                                                                                                            #
    over <- hyperGTest(params)                                                                        #GOstats
    kegg <- summary(over)                                                                                    #base
    kegg$KEGGID            #pathwayId

    #data normalization
    col_count = ncol(coagulation)
    raw_data = coagulation[,2:col_count]
    #raw_data = coagulation[,2:5]
    result_data = raw_data
    for(i in 1:nrow(raw_data)){
      for(j in 1:ncol(raw_data)){
          result_data[i,j] = -0.99+(raw_data[i,j]-min(raw_data[i,]))*1.98/(max(raw_data[i,])-min(raw_data[i,]))
      }
    }
    row.names(result_data)=coagulation[,1]    #

    #paint
    count = length(kegg$KEGGID)
    pathway_id = kegg$KEGGID

    for(index in 1:count){
        pv.out <- pathview(gene.data = result_data, pathway.id = as.character(pathway_id[index]), species =
        
    """
    rscript3 = """
    , out.suffix = as.character(pathway_id[index]), gene.idtype="SYMBOL",keys.align = "y",kegg.native = T,match.data = F, multi.state = T, same.layer = T)
    }
    
    pathwayId = as.character(pathway_id)
    
    """
    
    rscript = rscript1 + fileAddress + rscript2 + species_name + rscript3
    f=open('/usr/local/firmiana/leafy/static/images/tmp/heatmap_tmp/kegg.R','wb')
    f.write(rscript)
    f.close()
    # print rscript
    pId = r(rscript)    
    
    # show
    out = ""
    dot = "."
    suffix = ".multi.png"
    doubleMark = '"'
    # species_name1 = "mmu"
    species_name1 = speciesName
    count = len(pId)
  
  
    for i in range(count):
        pngname = species_name1 + pId[i] + dot + pId[i] + suffix
        pngsrc = pre + pngname
        pngsrc = pngsrc.replace(leafy_location, '')
        out = out + pId[i] + ':' + pngsrc + ';'
        if i == count - 1:
            out = out.strip(';')
    # process string
    return out

def heatmap(dataSource):
    
    pre = '{0}heatmap_tmp/firheatmap_{1}/'.format(tmpdir, time.time())
    os.mkdir(pre)
    ro.r.setwd(pre)
    # save tempfile
    tempfileName = "temp-heatmap" + ".txt"
    tempfile = open(tempfileName, "w")
    
    for line in dataSource:
        # print line
        for ele in range(len(line)):
            if ele != len(line) - 1:
                tempfile.write(str(line[ele]) + "\t")
            else:
                tempfile.write(str(line[ele]) + "\n")
    
    tempfile.close();
    
    
    out = ''
    rs1 = """
    #import packages
    library("gplots")
    
    #read datasource
    coagulation = read.table(
    """
    
    fileAddress = "'" + pre + tempfileName + "'" + ',header=T,stringsAsFactors=FALSE,sep="\\t")'
    
    rs2 = """
    col_count = ncol(coagulation)
    raw_data = coagulation[,2:col_count]
    result_data = raw_data
    for(i in 1:nrow(raw_data)){
      for(j in 1:ncol(raw_data)){
          #result_data[i,j] = -0.99+(raw_data[i,j]-min(raw_data[i,]))*1.98/(max(raw_data[i,])-min(raw_data[i,]))
          colmean = rowMeans(raw_data[i,])
          colsd = sd(raw_data[i,])
          result_data[i,j] = (raw_data[i,j] - colmean)/colsd
      }
    }
    data = as.matrix(result_data)
    
    #paint
    png(file=
    """
    
    tempPngName = '"' + "temp-heatmap" + ".png" + '"'
    
    rs3 = """
    , bg="transparent")
    heatmap.2(data, col=redgreen(75), scale="row",key=TRUE, symkey=FALSE, density.info="none", trace="none", cexRow=0.5, cexCol=1)
    dev.off()
    """
    
    rscript = rs1 + fileAddress + rs2 + tempPngName + rs3
    # print rscript
    ro.r(rscript)
    
    pngsrc = pre + "temp-heatmap.png" 
    pngsrc = pngsrc.replace(leafy_location, '')
    out = out + '<h2>' + "heatmap:" + '</h2>' + '<img  height=400px width=400px src="' + pngsrc + '" /><br/><br/>'
    
    return out

#===============================================================================
# def distribution(dataSource):
#     #pre = '{0}kegg_tmp/firkegg_{1}/'.format(tmpdir, time.time())
#     #print pre
#     pre='/usr/local/firmiana/leafy/static/images/tmp/heatmap_tmp/firheatmap_1419316226.5/'
#     #os.mkdir(pre)
#     #===========================================================================
#     # tempfileName = "temp"+"distribution.txt"
#     # tempfile = open(tempfileName, "w")
#     # for line in dataSource:
#     #     for ele in range(len(line)):
#     #         if ele!= len(line)-1:
#     #             tempfile.write(str(line[ele]) + "\t")
#     #         else:
#     #             tempfile.write(str(line[ele]) + "\n")
#     # tempfile.close()
#     #===========================================================================
#     #fileAddress = "'" + pre + tempfileName + "'"+',header=T,stringsAsFactors=FALSE,sep="\\t")'
#     out = ""
#     dot = "."
#     #suffix = ".distribution.png"
#     suffix='.png'
#     
#     #header=dataSource[0]  
#     header=['distribution-all','distribution-all','distribution-all']
#     count=len(header)
#     for i in range(count):
#         pngname = header[i] + suffix
#         pngsrc = pre + pngname
#         pngsrc=pngsrc.replace(leafy_location, '')
#         out = out + '<h2>' +header[i] + ':</h2>' + '<img src="' + pngsrc + '" /><br/><br/>'
#     return out
#===============================================================================

def htmlGenerator(out, pngsrc, pdfsrc, title, code='No code'):
    out += '<div class = tool_center>'
    out += '<a target="_blank" href="%s"> Download as PNG</a> or ' % pngsrc
    out += '<a target="_blank" href="%s"> Download as PDF</a>' % pdfsrc
    out += '<h3> %s : </h3> <img width=550px src="%s"/>' %(title, pngsrc)
    out += '</div>'
    out += '<div style="display:none">' + code + '</div>'
    return out
# plot correlation,stack,heatmap
def Rplot(dataSource, parameters):
    type = parameters['rType']
    tryNormalize=parameters['tryNormalize']
    pre = '{0}heatmap_tmp/firheatmap_{1}/'.format(tmpdir, time.time())
    pre_static = pre.replace(leafy_location, '')
            
    output_name = pre + type
    output_png = pre + type + ".png"
    output_txt = pre + type + "result.txt"
    output_pdf = pre + type + ".pdf"
    pngsrc = pre_static + type + ".png"
    pdfsrc = pre_static + type + ".pdf"    
    os.mkdir(pre)
    # save tempfile

    out = ''
    
    if type == 'correlation':
        outJsonDict = {'img':'','table':''}
        tempfileName = pre + "temp-heatmap" + ".txt"
        tempfile = open(tempfileName, "w")
        for line in dataSource:
            for ele in range(len(line)):
                if ele != len(line) - 1:
                    tempfile.write(str(line[ele]) + ",")
                else:
                    tempfile.write(str(line[ele]) + "\n")
        tempfile.close();
        
        
        
        out = out + '<h2>' + type + ":" + '</h2>' 
        titles = dataSource[0]
        ans = []
        names = {}
        for title in titles:
            names[title] = []
        for j in range(1, len(dataSource)):
            for i in range(len(titles)):
                # print titles[i]
                # print names[titles[i]]
                names[titles[i]].append(dataSource[j][i])
                # print names[titles[i]]
        '''
        titles[0] -> 'Symbol'
        '''
        for title1 in titles[1:]:
            temp = []
            tmp = ''
            for title2 in titles[1:]:
                if title1 != 'Symbol' and title2 != 'Symbol':
                    tmpNamePNG = pre + title1 + '-' + title2
                    output = os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary.jar -' + type + ' ' + tempfileName + ' ' + title1 + ' ' + title2 + ' ' + tmpNamePNG + ' F')
                    # print 'java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary.jar -'+type+' '+tempfileName+' '+pre+type+' F'
                    # return 'java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary.jar -'+type+' '+tempfileName+' '+pre+' F'
                    temp.append(pearsonr(names[title1], names[title2])[0])
                    tmp_pngsrc = pre_static + title1 + '-' + title2 + ".png"
                    #thumb(tmpNamePNG+'.png')
                    tmp += '<a href="' + tmp_pngsrc + '" target="_blank"/>' + '<img height=100px width=100px src="' + tmp_pngsrc + '" /></a>'
            out += tmp + '<br/>'
            ans.append(temp)
        ansName = pre + "heatmap" + ".txt"
        ansFile = open(ansName, "w")
        ansFile.write(','.join(titles)+'\n')
        i=0
        for line in ans:
            i+=1
            tmp = [titles[i]]
            for ele in range(len(line)):
                tmp.append(str(line[ele]))
            ansFile.write( ','.join(tmp) + '\n')
        ansFile.close();
        output_png = pre + 'correlationHeatmap.png'
        output_pdf = pre_static + 'correlationHeatmap.pdf'
        col1, col2 = parameters['minValue'], parameters['maxValue']
        no_cluster_heatmap(ansName, pre + 'correlationHeatmap', 'Correlation Heat-map',col1,col2)
        
        pngsrc = pre_static + 'correlationHeatmap.png' if os.path.isfile(output_png) else '/static/images/bkg_red_big.png'
        
        out = '<div class = tool_center><a target=_blank href=' +output_pdf + '> click to view PDF correlation Heatmap </a></div>' + '<br/>'+'<img height=400px width=400px src="' + pngsrc + '" /><br/><br/>' + out
        table = ''
        
        table += '<div class = tool_center>'
        table += '<table border="1">'
        table += '<caption>Correlation</caption>'
        table += '<tr><th align="left">Correlation</th>'
        for title in titles[1:]:
            table += '<th align="right">' + title + '</th>'
        table += '</tr>'
        #print ans
        for i in range(len(ans)):
            table += '<tr>'
            table += '<th align="left">' + titles[i+1] + '</th>'
            for j in range(len(ans[i])):
                pngsrc_tmp = pre_static + titles[i+1] + '-' + titles[j + 1] + ".png"
                table += '<td align="right">' + '<a href="' + pngsrc_tmp + '" target="_blank"/>' + '%.3f' % ans[i][j] + '</a></td>'
            table += '</tr>'
        table += '</table>'
        #out = out+table 
        out += '</div>'
        outJsonDict = {'img':out,'table':table}
        outJsonDict = json.dumps(outJsonDict, cls=DjangoJSONEncoder)
        return outJsonDict
        #return out
    
    elif type == 'stack': 
        outJsonDict = {'tempFile':'', 'img':''}
        removeTable=[]
        for line in dataSource:
            if 0 in line or -1.0 in line:
                removeTable.append(line)
        for line in removeTable:
            dataSource.remove(line)
        if tryNormalize=='1':
            tempfileName = pre + type + ".txt"
            tempfile = open(tempfileName, "w")
            for line in dataSource:
                for ele in range(len(line)):
                    if ele != len(line) - 1:
                        tempfile.write(str(line[ele]) + ",")
                    else:
                        tempfile.write(str(line[ele]) + "\n")
            tempfile.close();
            # output=os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary.jar -'+type+' '+tempfileName+' '+pre+type+' F')
            plot_stack(tempfileName, output_name)
            out += '<div class = tool_center>'
            out = out + '<h2>' + type + ":" + '</h2>' + '<img height=400px width=400px src="' + pngsrc + '" />' 
            out += '</div>'
            outJsonDict['img']=pngsrc
            outJsonDict = json.dumps(outJsonDict, cls=DjangoJSONEncoder)
            return outJsonDict
        elif tryNormalize=='2':
            tempfileNameBefore = pre + type+ ".txt"
            tempfile = open(tempfileNameBefore, "w")
            for line in dataSource:
                for ele in range(len(line)):
                    if ele != len(line) - 1:
                        tempfile.write(str(line[ele]) + ",")
                    else:
                        tempfile.write(str(line[ele]) + "\n")
            tempfile.close();
            # output=os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary.jar -'+type+' '+tempfileName+' '+pre+type+' F')
            plot_stack(tempfileNameBefore, output_name)
            
            tempfileNameAfter = pre + type+ "-after.txt"
            tempfile = open(tempfileNameAfter, "w")
            tempMatrix=[[] for i in range(len(dataSource[0])-1)]
            for line in dataSource:
                if line==dataSource[0]:
                    continue
                for ele in range(len(line)):
                    if ele==0:
                        continue
                    else:
                        tempMatrix[ele-1].append(float(line[ele]))
            minMedian=0
            selectMedian=0
#             for i in range(1,len(dataSource[0])):
#                 if minMedian<np.median(tempMatrix[i]):
#                     minMedian=np.median(tempMatrix[i])
#                     selectMedian=i
            preprocessCore = importr('preprocessCore')
            matrix = tempMatrix
            v = ro.FloatVector([ element for col in matrix for element in col ])
            m = ro.r['matrix'](v, ncol = len(matrix), byrow=False)
            Rnormalized_matrix = preprocessCore.normalize_quantiles(m)
            normalized_matrix = np.array( Rnormalized_matrix)
            #macaca()
            for line in range(len(dataSource)):
                if line==0:
                    continue
                for ele in range(len(dataSource[line])):
                    if ele==selectMedian or ele==0:
                        continue
                    else:
                        #dataSource[line][ele]=float(dataSource[line][ele])/np.median(tempMatrix[ele])* np.median(tempMatrix[selectMedian])
                        dataSource[line][ele]=normalized_matrix[line-1][ele-1]
            for line in dataSource:
                for ele in range(len(line)):
                    if ele != len(line) - 1:
                        tempfile.write(str(line[ele]) + ",")
                    else:
                        tempfile.write(str(line[ele]) + "\n")
            tempfile.close();
            # output=os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary.jar -'+type+' '+tempfileName+' '+pre+type+' F')
            plot_stack(tempfileNameAfter, output_name+'-after')
            out += '<div class = tool_center>'
            out +=  '<img height=400px width=400px src="' + pngsrc + '" />' 
            out +=  '<img height=400px width=400px src="' + pre_static + type+'-after' + ".png" + '" />' 
            out += '</div>'
            outJsonDict['img']=out
            outJsonDict = json.dumps(outJsonDict, cls=DjangoJSONEncoder)
            return outJsonDict
        elif tryNormalize=='3':
            #===================================================================
            # tempfileNameBefore = pre + "temp-heatmap" + ".txt"
            # tempfile = open(tempfileNameBefore, "w")
            # for line in dataSource:
            #     for ele in range(len(line)):
            #         if ele != len(line) - 1:
            #             tempfile.write(str(line[ele]) + ",")
            #         else:
            #             tempfile.write(str(line[ele]) + "\n")
            # tempfile.close();
            # # output=os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary.jar -'+type+' '+tempfileName+' '+pre+type+' F')
            # plot_stack(tempfileNameBefore, output_name)
            #===================================================================
            
            tempfileNameAfter = pre + type + "-after.txt"
            tempfile = open(tempfileNameAfter, "w")
            tempMatrix=[[] for i in range(len(dataSource))]
            for line in dataSource:
                if line==dataSource[0]:
                    continue
                for ele in range(len(line)):
                    if ele==0:
                        tempMatrix[ele].append(line[ele])
                    else:
                        tempMatrix[ele].append(float(line[ele]))
            minMedian=0
            selectMedian=0
            for i in range(1,len(dataSource[0])):
                if minMedian<np.median(tempMatrix[i]):
                    minMedian=np.median(tempMatrix[i])
                    selectMedian=i
            for line in range(len(dataSource)):
                if line==0:
                    continue
                for ele in range(len(dataSource[line])):
                    if ele==selectMedian or ele==0:
                        continue
                    else:
                        dataSource[line][ele]=float(dataSource[line][ele])/np.median(tempMatrix[ele])*np.median(tempMatrix[selectMedian])
            for line in dataSource:
                for ele in range(len(line)):
                    if ele != len(line) - 1:
                        tempfile.write(str(line[ele]) + ",")
                    else:
                        tempfile.write(str(line[ele]) + "\n")
            tempfile.close();
            # output=os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary.jar -'+type+' '+tempfileName+' '+pre+type+' F')
            plot_stack(tempfileNameAfter, output_name+'-after')
            out += '<div class = tool_center>'
            #out +=  '<img height=400px width=400px src="' + pngsrc + '" />' 
            out +=  '<img height=400px width=400px src="' + pre_static + type+'-after' + ".png" + '" />' 
            out += '</div>'
            pngsrc = pre_static + type + "-after.png"
            outJsonDict = {'tempFile':'123.txt', 'img':pngsrc}
            outJsonDict = json.dumps(outJsonDict, cls=DjangoJSONEncoder)
            return outJsonDict
    elif type == 'heatmap':
        tempfileName = pre + "temp-heatmap" + ".txt"
        tempfile = open(tempfileName, "w")
        minValue=1e900
        
        clusterType = 'Bilateral'
        clusterRow = clusterCol = 'T'
        if 'clusterType' in parameters: clusterType=parameters['clusterType']
        if clusterType!='Bilateral': clusterCol = 'F'
           
        fontsize=8
        if 'fontsize' in parameters: fontsize=int(parameters['fontsize'])
            
        cutoff=0
        if 'cutoff' in parameters: cutoff=float(parameters['cutoff'])
        
        zscore='No'
        if 'zscore' in parameters: zscore=parameters['zscore']
        
        log='No'
        if 'log' in parameters: log=parameters['log']  
          
        for line in dataSource[1:]:
            for pp in line[1:]:
                if pp>cutoff and pp<minValue:
                    minValue=pp
        #print minValue       
        for line in dataSource:
            if line==dataSource[0]:
                newLine=[str(p) for p in line]
                tempfile.write(','.join(newLine)+'\n')
                continue
            newLine=line[1:]
            if log=='Yes':
                newLine=[np.log(p) if p>minValue else np.log(minValue) for p in newLine]
            average=np.average(newLine)
            std=np.std(newLine)
            if zscore=='Yes':
                newLine=[(p-average)/std for p in newLine]
            newLine=[line[0]]+newLine
            newLine=[str(p) for p in newLine ]
            if 'nan' in newLine:
                continue
            tempfile.write(','.join(newLine)+'\n')
        tempfile.close()
        
        code = cluster_heatmap(tempfileName, output_name, '""', parameters['minValue'],parameters['maxValue'], "png",fontsize,clusterRow,clusterCol)
        cluster_heatmap(tempfileName, output_name, '""', parameters['minValue'],parameters['maxValue'], "pdf",fontsize,clusterRow,clusterCol)
        pngsrc = pngsrc if os.path.isfile(output_png) else '/static/images/bkg_red_big.png'
        pdfsrc = pdfsrc if os.path.isfile(output_pdf) else '/static/images/bkg_red_big.png'
        txtsrc = txtsrc if os.path.isfile(output_txt) else '/static/images/bkg_red_big.png'
        
        out += '<div class = tool_center>'
        out += '<a target="_blank" href=' + pngsrc + '> Download as PNG</a> or '
        out += '<a target="_blank" href=' + pdfsrc + '> Download as PDF</a> or '
        out += '<a target="_blank" href=' + txtsrc + '> Download as TXT</a> '
        
        out = out + '<h2>' + type + ":" + '</h2>' + '<img width=500px src="' + pngsrc + '" />' 
        out += '</div>'
        
        out += '<div style="display:none">'+ code + '</div>'
        #outJsonDict['code'] = code 
        return out
    else:
        outJsonDict = {'tempFile':'', 'img':''}
        out += '<div class = tool_center>'
        removeTable=[]
        for line in dataSource:
            if 0 in line or -1.0 in line:
                removeTable.append(line)
        for line in removeTable:
            dataSource.remove(line)
        if tryNormalize=='1':
            tempfileName = pre + type+ ".txt"
            tempfile = open(tempfileName, "w")
            for line in dataSource:
                for ele in range(len(line)):
                    if ele != len(line) - 1:
                        tempfile.write(str(line[ele]) + ",")
                    else:
                        tempfile.write(str(line[ele]) + "\n")
            tempfile.close();
            output = os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary_v1.4.1ContainTmpRscript.jar -' + type + ' ' + tempfileName + ' ' + pre + type + ' F')
            pngsrc = pre + type + ".png"
            pngsrc = pngsrc.replace(leafy_location, '')
            out = out + '<h2>' + type + ":" + '</h2>' + '<img height=400px width=400px src="' + pngsrc + '" />' 
            outJsonDict['img']=pngsrc
        elif tryNormalize=='2':
            tempfileName = pre + type+ ".txt"
            tempfile = open(tempfileName, "w")
            for line in dataSource:
                for ele in range(len(line)):
                    if ele != len(line) - 1:
                        tempfile.write(str(line[ele]) + ",")
                    else:
                        tempfile.write(str(line[ele]) + "\n")
            tempfile.close();
            output = os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary_v1.4.1ContainTmpRscript.jar -' + type + ' ' + tempfileName + ' ' + pre + type + ' F')
            pngsrc = pre + type + ".png"
            pngsrc = pngsrc.replace(leafy_location, '')
            out = out + '<img height=300px width=300px src="' + pngsrc + '" />' 
            tempfileName = pre + type+ "-after.txt"
            tempfile = open(tempfileName, "w")
            tempMatrix=[[] for i in range(len(dataSource))]
            for line in dataSource:
                if line==dataSource[0]:
                    continue
                for ele in range(len(line)):
                    if ele==0:
                        tempMatrix[ele].append(line[ele])
                    else:
                        tempMatrix[ele].append(float(line[ele]))
            minMedian=0
            selectMedian=0
            for i in range(1,len(dataSource[0])):
                if minMedian<np.median(tempMatrix[i]):
                    minMedian=np.median(tempMatrix[i])
                    selectMedian=i
            for line in range(len(dataSource)):
                if line==0:
                    continue
                for ele in range(len(dataSource[line])):
                    if ele==selectMedian or ele==0:
                        continue
                    else:
                        dataSource[line][ele]=float(dataSource[line][ele])/np.median(tempMatrix[ele])*np.median(tempMatrix[selectMedian])
            for line in dataSource:
                for ele in range(len(line)):
                    if ele != len(line) - 1:
                        tempfile.write(str(line[ele]) + ",")
                    else:
                        tempfile.write(str(line[ele]) + "\n")
            tempfile.close();
            output = os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary_v1.4.1ContainTmpRscript.jar -' + type + ' ' + tempfileName + ' ' + pre + type + '-after F')
            pngsrc = pre + type + "-after.png"
            pngsrc = pngsrc.replace(leafy_location, '')
            #out = out + '<h2>' + type + ":" + '</h2>' + '<img height=400px width=400px src="' + pngsrc + '" /><br/><br/>' 
            out = out + '<img height=300px width=300px src="' + pngsrc + '" />' 
            outJsonDict['img']=out
            
        elif tryNormalize=='3':
            tempfileName = pre + type+ "-after.txt"
            tempfile = open(tempfileName, "w")
            tempMatrix=[[] for i in range(len(dataSource))]
            for line in dataSource:
                if line==dataSource[0]:
                    continue
                for ele in range(len(line)):
                    if ele==0:
                        tempMatrix[ele].append(line[ele])
                    else:
                        if float(line[ele])>0:
                            tempMatrix[ele].append(float(line[ele]))
            for line in range(len(dataSource)):
                if line==0:
                    continue
                for ele in range(len(dataSource[line])):
                    if ele<2:
                        continue
                    else:
                        if dataSource[line][ele]>0:
                            dataSource[line][ele]=float(dataSource[line][ele])/np.median(tempMatrix[ele])*np.median(tempMatrix[1])
            for line in dataSource:
                for ele in range(len(line)):
                    if ele != len(line) - 1:
                        tempfile.write(str(line[ele]) + ",")
                    else:
                        tempfile.write(str(line[ele]) + "\n")
            tempfile.close();
            output = os.popen('java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary_v1.4.1ContainTmpRscript.jar -' + type + ' ' + tempfileName + ' ' + pre + type + '-after F')
            pngsrc = pre + type + "-after.png"
            pngsrc = pngsrc.replace(leafy_location, '')
            #out = out + '<h2>' + type + ":" + '</h2>' + '<img height=400px width=400px src="' + pngsrc + '" /><br/><br/>' 
            out = out + '<img height=300px width=300px src="' + pngsrc + '" />' 
        
            outJsonDict = {'tempFile':'123.txt', 'img':pngsrc}
        out += '</div>'
        outJsonDict = json.dumps(outJsonDict, cls=DjangoJSONEncoder)
        return outJsonDict

#def Rplot1(gi_lst, geneSymbol_lst, datasource, parameters):
def Rplot1(datasource, parameters):
    #print "ppi"
    outJsonDict = {}
    type = parameters['rType']
    expLength = parameters['expLength']
    cutoff = parameters['cutoff']
    pre = '{0}ppi_tmp/firppi_{1}/'.format(tmpdir, time.time())
    pre_static = pre.replace(leafy_location, '')
    output_name = pre + type
    os.mkdir(pre)
    
    #gi_list in 
    
    #pre1 = '{0}ppi_tmp/firppi_1437881595.48/'.format(tmpdir)
    pre1 = pre
    output_name1 = pre1 + type
    #tempfileName1 = pre1 + "2015-07-23-22-38-25.txt"
    tempfileName1 = pre1 + "temp-ppi.txt"
    
    #20%
    percent = 0.2
    zero_count_cutoff = math.ceil(expLength*percent)
#     zero_count = 0
#     satify_zero_count_flag = True
    #tempfileName1 = pre1 + "temp-ppi" + ".txt"
    with open(tempfileName1, 'w') as f:
        #print ""
#         for line in datasource:
#             if not 1e-06 in line:
#                 tmp = []
#                 for element in line:
#                     tmp.append(str(element))
#                 f.write( "\t".join(tmp) + "\n")
        for line in datasource:
            #test zero_count
            zero_count = 0
            satisfy_zero_count_flag = True
            for ele in line:
                if ele == 0:
                    zero_count = zero_count + 1
            if zero_count > zero_count_cutoff:
                satisfy_zero_count_flag = False
            if satisfy_zero_count_flag:
                tmp = []
                for element in line:
                    tmp.append(str(element))
                f.write( "\t".join(tmp) + "\n")
            #print s
    #gi_list in 2015-07-23-22-38-25.txt
    gi_lst = []
    with open(tempfileName1, "r") as f:
        for line in f.readlines():
            element = line.split("\t")
            gi_lst.append(element[0] + ";" + element[1])
    gi_lst_str = ""
    gi_lst_str = ",".join(gi_lst)
  
    #code, grn_list, grn_list_three = ppi(tempfileName, output_name, expLength)
    code, grn_list, grn_list_three, GRNListString, resultString = ppi(tempfileName1, output_name1, expLength, pre1, cutoff)
    #print s
    outJsonDict["code"] = code
    outJsonDict["grn_list"] = grn_list
    outJsonDict["grn_list_three"] = grn_list_three
    outJsonDict["GRNListString"] = GRNListString
    outJsonDict["resultString"] = resultString
    outJsonDict["gi_lst_str"] = gi_lst_str
    
    
    return outJsonDict
    

def Rplot2(dataSource, parameters):
    type = parameters['rType']
    pre = '{0}{1}_tmp/{1}_{2}/'.format(tmpdir,type, time.time())
    pre_static = pre.replace(leafy_location, '')
        
    output_name = pre + type
    output_png = pre + type + ".png"
    pngsrc = pre_static + type + ".png"
    pdfsrc = pre_static + type + ".pdf"
        
    os.mkdir(pre)
    # ro.r.setwd(pre)
    # save tempfile
    out = ''
    outJsonDict = {}
    
    if type == 'motif':
        tempfileName = pre + "temp-motif" + ".txt"
#         tempfile = open(tempfileName, "w")
#         for line in dataSource:
#             for ele in range(len(line)):
#                 if ele != len(line) - 1:
#                     tempfile.write(str(line[ele]) + ",")
#                 else:
#                     tempfile.write(str(line[ele]) + "\n")
#         tempfile.close()
        code,status, output = firmianaMotif(pre, tempfileName, output_name)
        
        out = htmlGenerator(out, pngsrc, pdfsrc, 'Motif', code=str(status))
                
    elif type == 'venn':
        # tempfileName = pre + "temp-heatmap" + ".txt"
        titles = dataSource[0]
        ans = []
        names = {}
        for title in titles:
            names[title] = []
        for j in range(1, len(dataSource)):
            for i in range(len(titles)):
                if dataSource[j][i] > 0 and dataSource[j][0]!='':
                    names[titles[i]].append(dataSource[j][0])
                    
        vennExp = parameters['vennExp']
        vennExpReadable = []
        
        lenVennExp = len(vennExp)
        if lenVennExp < 2:
            out = 'Not enough dimensions.'
            return out
        if lenVennExp > 5:
            out = 'Too many selected.'
            return out
        
        for i in range( lenVennExp ):
            vennExpReadable.append( vennExp[i].replace('<br/>','') )
           
        tmpProList  = [ set(names[vennExp[i]]) for i in range( lenVennExp ) ]
        tmpNameList = [ vennExpReadable[i][:9] for i in range( lenVennExp ) ]
        
        outJsonDict = eval( 'venn%sD'%lenVennExp )(tmpProList, tmpNameList, output_name)
        
        out = ''
        out += '<div class = tool_center>'
        out += '<a target="_blank" href="%s"> Download as PNG</a> or ' % pngsrc
        out += '<a target="_blank" href="%s"> Download as PDF</a><br/>' % pdfsrc
        out += '<h3> %s : </h3> <img width=550px src="%s"/>' %('Venn', pngsrc)
        out += '<img width=400px src="/static/images/regionVenn%s.png"/>' %( lenVennExp)
        out += '</div>'
        out += '<div style="display:none">' + '' + '</div>'
    
        #out = htmlGenerator(out, pngsrc, pdfsrc, 'Venn')
        
    elif type == 'volcano':
        controlExp = parameters['controlExp']
        caseExp = parameters['caseExp']
        xlim = parameters['xlim']
        ylim = parameters['ylim']
        
        # tempfileName = pre + "temp-heatmap" + ".txt"
        titles = dataSource[0]
        ans = []
        names = {}
        for title in titles:
            names[title] = []
        for j in range(1, len(dataSource)):
            for i in range(len(titles)):
                names[titles[i]].append(dataSource[j][i])

        # ctrl_list = list(names[controlExp])
        ctrl_list = [float(i) for i in names[controlExp]]
        # expr_list = list(names[caseExp])
        expr_list = [float(i) for i in names[caseExp]]
        ratio_list, inten_list = signif.refine_data(ctrl_list, expr_list)
        pvalue_list = signif.signif(ratio_list, inten_list)
        tempfileName = pre + "temp_volcano" + ".txt"
        
        ratioPvalueList = []
        with open(tempfileName, "w") as tempfile: 
            tempfile.write('\t'.join(['Symbol', "log2(ratio)", "-log10(pvalue)" ]) + '\n')
            
            for i in range(len(pvalue_list)):
                symbol = dataSource[i+1][0]
                if not symbol:symbol = "-"
                ratio  = ratio_list[i]
                pvalue = pvalue_list[i]
                
                if ratio_list[i] > math.pow(2, 10) :
                    ratio = math.pow(2, 10) 
                elif ratio_list[i] < math.pow(2, -10) :
                    ratio = math.pow(2, -10)
                    
                pvalue = 1e-6 if pvalue_list[i] < 1e-6 else pvalue_list[i]
                    
                ratioLog2   = math.log(ratio, 2) if ratio != 0 else -10
                pvalueLog10 = -math.log(pvalue, 10) if pvalue != 0 else 6
                
                ratioPvalueList.append( {'symbol':symbol,'ratio':ratioLog2, 'pvalue':pvalueLog10 } )
                
                tempfile.write('\t'.join([symbol, str(ratioLog2), str(pvalueLog10)] ) + '\n')
                
        code = plot_volcano(tempfileName, output_name, xlim, ylim)
        #out = out + '<h2>' + type + ":" + '</h2>' + '<img height=400px width=400px src="' + pngsrc + '" /><br/><br/>' 
        output_R = pre + type + ".sh"
        with open(output_R,'w') as f:
            f.write(code)
            
        out = htmlGenerator(out, pngsrc, pdfsrc, 'Volcano',code)
        outJsonDict['dataTxt'] = pre_static + "temp_volcano" + ".txt"
        outJsonDict['ratioPvalueList'] = ratioPvalueList  
        outJsonDict['code'] = code 
    elif type == 'tf-tg':

        tempfileName = pre + "temp_tftg.txt"
        tempfile = open(tempfileName, "w")
        tempfile.write( "\t".join( dataSource[0] ) + '\n' )
        for line in dataSource[1:]:
            if not line[0]:
                continue
            
            tmpStringList = [ line[0].upper() ]
            for idx in range( 1, len(line) ):
                if line[idx] > 0 :
                    tmpStringList.append( str(math.log10(line[idx])) )
                    #tmpStringList.append( str(line[idx]) )
                else:
                    tmpStringList.append( '0' )
    
            tmpString = "\t".join( tmpStringList ) + '\n'
            tempfile.write( tmpString )
            
        tempfile.close();
        
        TFTG_DB = 'kinaseSubstrate_DB'      
        code = firmianaTFTG(tempfileName, TFTG_DB, output_name)
        #out = out + '<h2>' + type + ":" + '</h2>' + '<img height=400px width=400px src="' + pngsrc + '" /><br/><br/>' 
        output_R = pre + type + ".sh"
        with open(output_R,'w') as f:
            f.write(code)
            
        txtDesc = pre_static + type + '_Desc.txt'
        txtAsc  = pre_static + type + '_Asc.txt'
        out += '<div class = tool_center>'
        out += '<a target="_blank" href=' + pngsrc + '> Download as PNG</a> or '
        out += '<a target="_blank" href=' + pdfsrc + '> Download as PDF</a><br/>'
        
        out += '<a target="_blank" href=' + txtDesc + '> decreasing</a> or '
        out += '<a target="_blank" href=' + txtAsc + '> increasing</a>'
        
        out += '<h2>Kinase Substrate : </h2>' + '<img width=500px src="' + pngsrc + '" />' 
        out += '</div>'
        out += '<div style="display:none">' + code + '</div>'
        outJsonDict['code'] = code  
    
    elif type == 'kinaseSubstrate':

        tempfileName = pre + "temp_kinaseSubstrate.txt"
        tempfile = open(tempfileName, "w")
        i = 0
        for line in dataSource:
            if i == 0:
                tempfile.write( "\t".join( line ) + '\n' )
                i+=1
                continue
            if not line[0]:
                continue
            
            tmpStringList = [ line[0].upper() ]
            for idx in range( 1, len(line) ):
                if line[idx] > 0 :
                    tmpStringList.append( str(math.log10(line[idx])) )
                else:
                    tmpStringList.append( '0' )
    
            tmpString = "\t".join( tmpStringList ) + '\n'
            tempfile.write( tmpString )
            
        tempfile.close();
        
        TFTG_DB = 'kinaseSubstrate_DB'      
        code = firmianaKinaseSubstrate(tempfileName, TFTG_DB, output_name)
        #out = out + '<h2>' + type + ":" + '</h2>' + '<img height=400px width=400px src="' + pngsrc + '" /><br/><br/>' 
    
        output_R = pre + type + ".sh"
        with open(output_R,'w') as f:
            f.write(code)
            
        txtDesc = pre_static + type + '_Desc.txt'
        txtAsc  = pre_static + type + '_Asc.txt'
        out += '<div class = tool_center>'
        out += '<a target="_blank" href=' + pngsrc + '> Download as PNG</a> or '
        out += '<a target="_blank" href=' + pdfsrc + '> Download as PDF</a><br/>'
        
        out += '<a target="_blank" href=' + txtDesc + '> decreasing</a> or '
        out += '<a target="_blank" href=' + txtAsc + '> increasing</a>'
        
        out += '<h2>Kinase Substrate : </h2>' + '<img width=500px src="' + pngsrc + '" />' 
        out += '</div>'
        out += '<div style="display:none">' + code + '</div>'
        outJsonDict['code'] = code 
    outJsonDict['tmpHtml'] = out  
    return outJsonDict

# k-heatmap
def Rplot3(dataSource, parameters):
    type = parameters['rType']
    k_num = parameters['kNum']
    pre = '{0}heatmap_tmp/firheatmap_{1}/'.format(tmpdir, time.time())
    pre_static = pre.replace(leafy_location, '')

    output_name    = pre + type
    output_nameSrc = pre_static + type 
    
    output_png = pre + type + ".png"
    pngsrc = pre_static + type + ".png"
    
    os.mkdir(pre)
    # ro.r.setwd(pre)
    # save tempfile
    out = ''
    cutoff=0
    if 'cutoff' in parameters:
        cutoff=float(parameters['cutoff'])
    zscore='No'
    if 'zscore' in parameters:
        zscore=parameters['zscore']
    log='No'
    if 'log' in parameters:
        log=parameters['log']
    if type == 'k-heatmap':
        outJsonDict = {'kmean':[], 'heatmap':'/static/images/bkg_red_big.png'}
        tempfileName = pre + "temp-heatmap" + ".txt"
        tempfile = open(tempfileName, "w")
        i = 0
        minValue=1e900
        for line in dataSource[1:]:
            for pp in line[1:]:
                if pp>cutoff and pp<minValue:
                    minValue=pp
        for line in dataSource:
            if i == 0:
                tempfile.write( ",".join( line ) + '\n' )
                i+=1
                continue
            if not line[0]:
                continue
            newLine=line[1:]
            if log=='Yes':
                newLine=[np.log(p) if p>cutoff else np.log(minValue) for p in newLine]
            average=np.average(newLine)
            std=np.std(newLine)
            if zscore=='Yes':
                newLine=[(p-average)/std for p in newLine]
#             newLine=[p if p>0 else 0 for p in newLine]
            newLine=[str(p) for p in newLine ]
            if 'nan' in newLine:
                continue
            tmpStringList = [ line[0] ]
            #===================================================================
            # for idx in range( 1, len(line) ):
            #     if line[idx] > 0 :
            #         tmpStringList.append( str(math.log10(line[idx])) )
            #     else:
            #         tmpStringList.append( '0' )
            #===================================================================
            tmpStringList.extend(newLine)
            tmpString = ",".join( tmpStringList ) + '\n'
            tempfile.write( tmpString )
            
        tempfile.close();
        
        kmeans_cluster_heatmap(tempfileName, output_name, k_num, parameters['minValue'], parameters['maxValue'])
        
        if os.path.isfile(output_png):
            outJsonDict['heatmap'] = pngsrc 
        else:
            return outJsonDict
        #out += '<div class = tool_center>'
        #out += '<h2>' + type + ":" + '</h2>' + '<img height=400px width=400px src="' + pngsrc + '" /><br/><br/>' 
        if not os.path.isfile( output_name + '.kmeanMatrix.txt' ):
            return outJsonDict
        
        k_list = []
        with open(output_name + '.kmeanMatrix.txt', 'r') as f:
            for line in f:
                k_list.extend(line.strip().split(' '))
        # print k_list
        k_list = [int(k_ele) for k_ele in k_list]
        kmeanClusterLists = [ [] for i in range(k_num) ]
        for cID in range(len(k_list)):
            kmeanClusterLists[ k_list[cID]-1 ].append( { 'name':dataSource[cID + 1][0] } )
        for i in range(1, k_num + 1):
            with open( output_name + '.kmeanCluster_' + str(i) + '.txt', 'w' ) as f:
                for sym in kmeanClusterLists[i-1]:
                    f.write(sym['name'] + '\n')
#                 
#         for i in range(1, k_num + 1):
#             f = open( output_name + '.kmeanCluster_' + str(i) + '.txt', 'w' )
#             for ele in range(len(k_list)):
#                 if k_list[ele] == i:
#                     f.write(dataSource[ele + 1][0] + '\n')
#             f.close()

        for i in range(1, k_num + 1):
            showName = 'KmeanCluster-' + str(i)
            kmean_preSrc = output_nameSrc + '.kmeanCluster_' + str(i)
            kmean_txtSrc = kmean_preSrc + '.txt'
            kmean_pngSrc = kmean_preSrc + '.png'
            outJsonDict['kmean'].append({'name':showName, 'list':kmeanClusterLists[i-1], 'txt':kmean_txtSrc, 'url':kmean_pngSrc})
            #out = out + '<a href="' + kmean_txt + '" target="_blank"/>' + '<img height=400px width=400px src="' + kmean_png + '" /></a>'
        
        #out += '</div>'    
    
    return outJsonDict

''' PCA '''    
def Rplot4(dataSource, parameters, metadata_matrix):
    type = parameters['rType']
    pcList = parameters['pcList']
    metadataList = parameters['metadataList']
    
    pre = '{0}pca_tmp/firpca_{1}/'.format(tmpdir, time.time())
    pre_static = pre.replace(leafy_location, '')
    output_name = pre + type
    output_png = pre + type + ".png"
    pngsrc = pre_static + type + ".png"
    
    

    os.mkdir(pre) 
       
    out = ''
    if parameters['adjust']:
        input = parameters['input']
        input_metadata = parameters['tmpMetaFile']
        src_metadata = ''
        
        preInput = parameters['preInput']
        preImage = parameters['preImage'] 
        preCorMatrixFile = ''
        preSrcCorMatrixFile = parameters['preSrcCorMatrixFile'] 
        
        corMatrixFile = pre + 'pca_cor_matrix.txt'
        srcCorMatrixFile = pre_static + 'pca_cor_matrix.txt'
        
        code = plot_pca(input, input_metadata, output_name,pcList,metadataList) 
        
        output_R = pre + type + ".sh"
        with open(output_R,'w') as f:
            f.write(code)
        
        out += '<div width=1020px class = tool_center>'
        
        out += '<div style="float:left">'
        out += '' + 'Initial PCA' + ":" + '<br/>' 
        out += '<a target="_blank" href=' + preInput.replace(leafy_location, '') + '>Download Initial Data Table </a> or '
        out += '<a target="_blank" href=' + preSrcCorMatrixFile + '>Download  Initial Correlation Matrix </a><br/>'
        out += '<img height=500px  src="' + preImage + '"/>'
        out += '</div>'
        
        out += '<div style="float:right">'
        out += '' + 'Adjusted PCA' + ":" + '<br/>' 
        out += '<a target="_blank" href=' + input.replace(leafy_location, '') + '>Download Adjusted Data Table </a> or '
        out += '<a target="_blank" href=' + srcCorMatrixFile + '>Download Adjusted Correlation Matrix </a><br/>'
        out += '<img height=500px  src="' + pngsrc + '"/>'
        out += '</div>'
        
        out += '</div>'
        
        out += '<div style="display:none">'+ code + '</div>'
        #outJsonDict['code'] = code 
        return (out,input,input_metadata,src_metadata,srcCorMatrixFile, pngsrc)
    
    else :
        input = pre + "temp_pca.txt"
        input_metadata = pre + "temp_pca_metadata.txt"
        src_metadata = pre_static + "temp_pca_metadata.txt"
        corMatrixFile = pre + 'pca_cor_matrix.txt'
        srcCorMatrixFile = pre_static + 'pca_cor_matrix.txt'
        
        tempfile = open(input, "w")
        i = 1
        for line in dataSource:
            if i == 1:
                tempfile.write("\t".join(line) + '\n') # write titles
                i += 1
                continue
            toWrite = ""
            for ele in range(len(line)):
                if ele == 0:
                    if not line[ele]:  # GeneSymbol == ''
                        break
                    toWrite += (str(line[ele]) + "\t")
                    continue
                log_value = math.log(float(line[ele]), 2) if float(line[ele]) > 0 else 0
                if ele != len(line) - 1:
                    toWrite += (str(log_value) + "\t")
                else:
                    toWrite += (str(log_value) + "\n")
            tempfile.write(toWrite)
        tempfile.close();
        
        tempfile = open(input_metadata, "w")
        for line in metadata_matrix:
            tempfile.write("\t".join(line) + "\n")
        tempfile.close();
        code = plot_pca(input, input_metadata, output_name,pcList,metadataList) 
        
        output_R = pre + type + ".sh"
        with open(output_R,'w') as f:
            f.write(code)
            
        conditionList = ",".join(dataSource[0][1:])
        #code = plot_pca_zinky(input, input_metadata, output_name, pcList, conditionList)
        
        out += '<div class = tool_center>'
        out += '<h2>' + 'PCA' + ":" + '</h2>' 
        out += '<a target="_blank" href=' + src_metadata + '>Download Metadata Matrix </a> or '
        out += '<a target="_blank" href=' + srcCorMatrixFile + '>Download Correlation Matrix </a><br/>'
        out += '<img height=500px  src="' + pngsrc + '"/>'
        out += '</div>'
        out += '<div style="display:none">'+ code + '</div>'
        #outJsonDict['code'] = code 
        # out = out + '<a href="' + pre_static + 'pca_cor_matrix.txt' + '" target="_blank"/>' + '<img height=400px width=400px src="' + pngsrc + '" /></a>'
        return (out,input,input_metadata,src_metadata,srcCorMatrixFile, pngsrc)

def Rplot5(dataSource, type):
    pre = '{0}boxplot_tmp/firboxplot_{1}/'.format(tmpdir, time.time())
    pre_static = pre.replace(leafy_location, '')
    #print dataSource[1:10]  
    output_name = pre + type
    output_png = pre + type + ".png"

    pngsrc = pre_static + type + ".png"
    pdfsrc = pre_static + type + ".pdf"
    os.mkdir(pre) 
    out = ''    
    if type == 'genebox':
        tempfileName = pre + "genebox.txt"
        tempfile = open(tempfileName, "w")
        i = -1
        header = dataSource[0]
        for line in dataSource:    
            i += 1
            if i == 0:
                tempfile.write('Symbol\tGroup\tExpression\n')
                continue
            if i > 15:
                break
            for ele in range(1, len(line)):
                if line[0]:  # Gene Symbol may not exist
                    tempfile.write(line[0] + '\t' + str(header[ele]) + '\t' + str(line[ele]) + '\n')
        tempfile.close();
        
        code = plot_multi_boxplot(tempfileName, output_name)
        
        output_R = pre + type + ".sh"
        with open(output_R,'w') as f:
            f.write(code)
        
        out = htmlGenerator(out, pngsrc, pdfsrc, 'Gene boxplot distribution(First 15 genes limited)')

    return (out,pngsrc,pdfsrc)

''' GO Analysis '''
def Rplot6(dataSource, parameters): 
    '''
    summaryFile  = paste(Args[6],"Summary.txt",sep="")
    
    type = Args[7] # GOClassification/enrich
    
    GroupGO_png  = paste(Args[6],".png",sep="")
    GroupGO_pdf  = paste(Args[6],".pdf",sep="")
    
    EnrichGO_png = paste(Args[6],".png",sep="")
    EnrichGO_pdf = paste(Args[6],".pdf",sep="")
    
    Cnetplot_png = paste(Args[6],"Cnetplot.png",sep="")
    Cnetplot_pdf = paste(Args[6],"Cnetplot.pdf",sep="")
    '''
    type = parameters['rType']
    organism = parameters['organism']
    ont = parameters['ont']  
    
    pre = '{0}go_tmp/go_{1}/'.format(tmpdir, time.time())
    os.mkdir(pre)
    pre_static = pre.replace(leafy_location, '')
    output_name = pre + type
    output_nameSrc = pre_static + type 
    
    output_png = pre + type + ".png"
    pngsrc = pre_static + type + ".png"
    txtSummary = output_name + 'Summary.txt'
    
    tempfileName = pre + "goInputSymbol.txt" 
  
    out = '' 
    if type == 'GOClassification':
        level = parameters['level']
        
        with open(tempfileName, 'w') as f:
            for i in range(1, len(dataSource)):
                f.write(dataSource[i][0] + '\n')
          
        code, status, output = firmianaGO(tempfileName, organism, ont, level, output_name, type)
        
        pngGroup  = output_nameSrc + '.png'
        pdfGroup  = output_nameSrc + '.pdf'
        
        out = htmlGenerator(out, pngGroup, pdfGroup, 'GO Group Analysis',code=code)

        return (out, txtSummary, pngGroup, pdfGroup)
    
    elif type == 'GOEnrich':
        level = 0
                 
        with open(tempfileName, 'w') as f:
            for i in range(1, len(dataSource)):
                f.write(dataSource[i][0] + '\n')
                if i>3000:break
                
        code, status, output  = firmianaGO(tempfileName, organism, ont, level, output_name, type)
        
        pngEnrich = output_nameSrc + '.png'
        pdfEnrich = output_nameSrc + '.pdf'
        pngCnet = output_nameSrc + 'Cnetplot.png'
        
        out = htmlGenerator(out, pngEnrich, pdfEnrich, 'GO Group Analysis',code=code)

        return (out,txtSummary,pngEnrich,pdfEnrich)

def firmianaMotif(tmpWD, input, output_name):
    code = binRSCRIPT + ' ' + Rscript_location + 'motif.R "%s" "%s" "%s"' % ( input, output_name, tmpWD )
    (status, output) = commands.getstatusoutput(code)
    return code,status, output
    
def firmianaKinaseSubstrate(input, DB, output_name):
    code = binRSCRIPT + ' ' + Rscript_location + 'kinaseSubstrate.R "%s" "%s" "%s"' % ( input, DB, output_name )
    (status, output) = commands.getstatusoutput(code)
    return code#,status, output

def firmianaTFTG(input, DB, output_name):
    code = binRSCRIPT + ' ' + Rscript_location + 'TFTG.R "%s" "%s" "%s"' % ( input, DB, output_name )
    (status, output) = commands.getstatusoutput(code)
    return code#,status, output

def firmianaGO(input, organism, ont, level, output_name, type): 
    code = binRSCRIPT + ' ' + Rscript_location + 'GO_firmiana.R %s %s %s %s %s %s' % ( input, organism, ont, level, output_name, type )
    print code
    (status, output) = commands.getstatusoutput(code)
    return code,status, output
    
    
def plot_multi_boxplot(input, output_png):
    code = binRSCRIPT + ' ' + Rscript_location + 'multi_boxplot.R %s %s' % (input, output_png)
    (status, output) = commands.getstatusoutput(code)
    return code

def plot_pca_zinky(input, input_metadata, output_name, pcList, conditionList):
    code = binRSCRIPT + ' ' + Rscript_location + 'PCA_zinky.R %s %s \"%s\" \"%s\"' % (input, output_name, pcList, conditionList)
    # (status, output) = commands.getstatusoutput(code)
    # code = 'java -jar /usr/local/firmiana/data/sources/zsu/RplotGallary.jar -pca %s %s -isText T -PClist %s -outputpath %s'%(input,conditionList,pcList,output_name)
    output = os.popen(code)
    return code

def plot_pca(input, input_metadata, output_name, pcList,metadataList):
    code = binRSCRIPT + ' ' + Rscript_location + 'PCA_xiaxia.R %s %s %s \"%s\" \"%s\"' % (input, input_metadata, output_name, pcList,metadataList)
    (status, output) = commands.getstatusoutput(code)
    return code

def plot_volcano(input, output, xlim, ylim):
    code = binRSCRIPT + ' ' + Rscript_location + 'volcano.R %s %s %s %s' % (input, output,xlim,ylim)
    #print code
    (status, output) = commands.getstatusoutput(code)
    return code

def no_cluster_heatmap(input, output, title,c1,c2):
        
    code = binRSCRIPT + ' ' + Rscript_location + 'non_cluster_heatmap.R "%s" "%s" "%s" "%s" "%s"' % (input, output, title, c1, c2)
    
    output_R = output + ".sh"
    with open(output_R,'w') as f:
        f.write(code)
        
    output = os.popen(code)

def boxplot(input, output):
        
    code = binRSCRIPT + ' ' + Rscript_location + 'boxplot.R "%s" "%s"' % (input, output)
    
    output_R = output + ".sh"
    with open(output_R,'w') as f:
        f.write(code)
        
    output = os.popen(code)
    
def cluster_heatmap(input, output, title, c1, c2, format,fontsize,clusterRow,clusterCol):
    code = binRSCRIPT + ' ' + Rscript_location + 'cluster_heatmap.R %s %s %s "%s" "%s" %s %s %s %s' % (input, output, title, c1, c2, format,fontsize,clusterRow,clusterCol)
    print code
    output = os.popen(code)
    return code

def kmeans_cluster_heatmap(input, output, num, c1, c2):
    code = binRSCRIPT + ' ' + Rscript_location + '/kmean_cluster_heatmap.R "%s" "%s" "%s" "%s" "%s"' % (input, output, num, c1, c2)
    output = os.popen(code)

def ppi(input, output, expLength, outputAddr, var_cutoff):
    grn_list = ["finish"]
    grn_addr = output + "-grn.txt"
    grn_list_addr = output + "-grn-list.txt"
    grn_list_addr2 = output + "-grn-list-cytoscape.txt"
    grn_list_addr_finish = output + "-grn-list-str-start.txt"
    grn_list_addr_finish_str = output + "-grn-list-str-finish.txt"
    grn_list_addr_flag = output + "-grn-flag.txt"
    #GRNListString = ""
    GRNListString = []
    resultString = ""
    #print s
     
    code = binRSCRIPT + ' ' + Rscript_location + '/ppi_clr_infomap.R "%s" "%s" "%s"' % (input, output, expLength)
    out_flag = os.popen(code)
    out_flag_str = out_flag.read()
#     while True:
# 		if os.path.exists(grn_list_addr_flag):
# 			break
    grn_list_three = ppi_read_grn(grn_addr, var_cutoff)
    grn_list_three_length = len(grn_list_three)
    
    gi_lst = []
    with open(input, "r") as f:
        for line in f:
            element = line.split("\t")
            gi_lst.append(element[1])
            
    if grn_list_three_length>0:
        #"-grn-list.txt"
        with open(grn_list_addr, 'w') as f:
            for line in grn_list_three:
                tempStr = " ".join(line)
                f.write(tempStr + "\n")
                #GRNListString = GRNListString + tempStr + ","
        #GRNListString = GRNListString[:-1]
        
        with open(grn_list_addr2, 'w') as f:
            for line in grn_list_three:
                tempStr = gi_lst[int(line[0]) - 1] + ' ' + 'pp' + ' ' + gi_lst[int(line[1]) - 1] + ' ' + line[2]
                f.write(tempStr + "\n")
        
        with open(grn_list_addr_finish, "w") as f1:
            f1.write("PPI-grn-list-finish.txt")
         
        #GRNListString 
        
        for line1 in grn_list_three:
            tempStr1 = " ".join(line1)       
            #GRNListString = GRNListString + tempStr1 + ","
            GRNListString.append(tempStr1)
        #GRNListString = GRNListString[:-1]
        GRNListString = ",".join(GRNListString)
         
        with open(grn_list_addr_finish_str, "w") as f2:
            f2.write("PPI-grn-list-finish-str.txt")
        
    
    #ppi_infomap
    #while os.path.exists(grn_list_addr):
    #print s
    resultString = ppi_infomap(grn_list_addr, outputAddr)
    #print s
    return code, grn_list, grn_list_three, GRNListString, resultString

def ppi_read_grn(filepath, var_cutoff):
	#filepath = "/usr/local/firmiana/leafy/static/images/tmp/ppi_tmp/firppi_1437881595.48/PPI-grn.txt"
    cutoff = var_cutoff
    grn_list = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            templist = line.strip('\n').split('\t')
            grn_list.append(templist)
	length = len(grn_list)
	templist1 = []
	grn_list_three = []
	for i in range(0, length):
		for j in range(i+1, length):
			tempValue = float(grn_list[i][j])
			if tempValue >= cutoff:
				templist1.append(str(i+1)) #can't start from zero
				templist1.append(str(j+1))
				templist1.append(str(tempValue))
				grn_list_three.append(templist1)
				templist1 = []
	
	return grn_list_three

def ppi_infomap(input, output):
    code = "/usr/local/firmiana/leafy/static/Infomap/Infomap " + input + " " + output + " -N 10 --tree"
    #treeAddress = output + "PPI-grn-list.tree"
    treeAddress = output + "ppi-grn-list.tree"
#     filepath = "/usr/local/firmiana/leafy/static/images/tmp/ppi_tmp/firppi_1437881595.48/PPI-grn-list.txt"
#     outfile = "/usr/local/firmiana/leafy/static/images/tmp/ppi_tmp/firppi_1437881595.48/"
#     code = "/usr/local/firmiana/leafy/static/Infomap/Infomap " + filepath + " " + outfile + " -N 10 --tree"
    out_flag = os.popen(code)
    #print bug
    out_flag_str = out_flag.read()
    #print bug
    #"/usr/local/firmiana/leafy/static/images/tmp/ppi_tmp/firppi_1437881595.48/PPI-grn-list.tree"
#     for i in range(10000000):
#         pass
    #print resultString
    resultString = ""
    if out_flag and os.path.exists(treeAddress):
        count = 0
        with open(treeAddress, 'r') as f:
            for line in f.readlines():
                count = count + 1
                if count > 2:
                    temp_line_lst = line.strip("\n").split(" ")
                    moduleNo = temp_line_lst[0].split(":")[0]
                    value = round(float(temp_line_lst[1]), 4)
                    giIndex = int(temp_line_lst[-1])-1
                    #giNo = gi_lst[giIndex]
                    tempStr = moduleNo + " " + str(value) + " " + str(giIndex)
                    resultString = resultString + tempStr + ","
        resultString = resultString[:-1]
        
       
    return resultString
    
    

    

def venn2D(tmpProList, tmpNameList, output_name):
    def myDraw():
        grid_draw(venn2(
                area1=len(pro1),
                area2=len(pro2),
                cross_area=len(n12),
                category=ro.StrVector(['pro_' + name1, 'pro_' + name2]),
                fill=ro.StrVector(['#FF6342', '#ADDE63']),
                cat_col=ro.StrVector(['#000000', '#000000']),
                lty='blank',
                cex=2.5,
                cat_cex=2.5,
                cat_pos=ro.IntVector([-20, 20]),
                cat_dist=0.05,
                ext_pos=30,
                ext_dist=-0.05,
                ext_length=0.85,
                ext_line_lwd=2,
                ext_line_lty="dashed"                        
                ))
        dev_off()
        
    pro1, pro2 = tmpProList
    
    n12= pro1 & pro2
    
    data = {}
    data['regionList'] = [{'name':'A'},{'name':'B'},{'name':'C'}]
    data['vennList'] = {}
    
    vennDict = {}
    vennDict['A'] = pro2 - n12
    vennDict['B'] = n12
    vennDict['C'] = pro1 - n12
    
    for key,value in vennDict.iteritems():
        tmp = []
        i=1
        for p in value:
            tmp.append( {'no':i,'region':key,'name':p} )
            i+=1
        data['vennList'][key] = tmp
        
    
    name1, name2 = tmpNameList
    
    output_png = output_name + '.png'
    output_pdf = output_name + '.pdf'
    
    venng = importr('VennDiagram')
    venn2 = ro.r['draw.pairwise.venn']
    grid_draw = ro.r['grid.draw']
    dev_off = ro.r['dev.off']
    # ro.r.setwd(tmpdir)
    # prooutfile = 'venn_pro' + str(time.time()) + '.png'
    ro.r.png(output_png, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=300)
    myDraw()

    ro.r.pdf(output_pdf)
    myDraw()
    
    return data

def venn3D(tmpProList, tmpNameList, output_name):
    def myDraw():
        grid_draw(venn3(
                        area1=len(pro1),
                        area2=len(pro2),
                        area3=len(pro3),
                        n12=len(n12),
                        n23=len(n23),
                        n13=len(n13),
                        n123=len(n123),
                        category=ro.StrVector(['pro_' + name1, 'pro_' + name2, 'pro_' + name3]),
                        fill=ro.StrVector(['#FF6342', '#ADDE63', '#63C6DE']),
                        cat_col=ro.StrVector(['#000000', '#000000', '#000000']),
                        lty='blank',
                        cex=2.5,
                        cat_pos=ro.IntVector([-20, 20, 180]),
                        cat_cex=2.5,
                        cat_dist=0.05,
                        ext_pos=30,
                        ext_dist=-0.05,
                        ext_length=0.85,
                        ext_line_lwd=2,
                        ext_line_lty="dashed"                        
                        ))
        dev_off()
        
    pro1,pro2,pro3 = tmpProList
    
    n12= pro1 & pro2
    n13= pro1 & pro3
    n23= pro2 & pro3
    n123= pro1 & pro2 & pro3
    
    data = {}
    data['regionList'] = []
    i=0
    for word in string.uppercase:
        if i>6:break
        data['regionList'].append({'name':word})
        i+=1
    data['vennList'] = {}
    
    vennDict = {}
    vennDict['A'] = pro1 - pro2 - pro3
    vennDict['B'] = pro2 - pro1 - pro3
    vennDict['C'] = pro3 - pro1 - pro2
    vennDict['D'] = n12 - n123 
    vennDict['E'] = n23 - n123 
    vennDict['F'] = n13 - n123 
    vennDict['G'] = n123 
    
    for key,value in vennDict.iteritems():
        tmp = []
        i=1
        for p in value:
            tmp.append( {'no':i,'region':key,'name':p} )
            i+=1
        data['vennList'][key] = tmp
        
    name1,name2,name3 = tmpNameList
    
    output_png = output_name + '.png'
    output_pdf = output_name + '.pdf'
    
    venng = importr('VennDiagram')
    venn3 = ro.r['draw.triple.venn']
    grid_draw = ro.r['grid.draw']
    dev_off = ro.r['dev.off']


    # ro.r.setwd(tmpdir)
    # prooutfile = 'venn_pro' + str(time.time()) + '.png'
    ro.r.png(output_png, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=300)
    myDraw()

    ro.r.pdf(output_pdf)
    myDraw()
    
    return data

def venn4D(tmpProList, tmpNameList, output_name):
    def myDraw():
        grid_draw(venn4(
                        area1=len(pro1),
                        area2=len(pro2),
                        area3=len(pro3),
                        area4=len(pro4),
                        n12=len(n12),
                        n13=len(n13),
                        n14=len(n14),
                        n23=len(n23),
                        n24=len(n24),
                        n34=len(n34),
                        n123=len(n123),
                        n124=len(n124),
                        n134=len(n134),
                        n234=len(n234),
                        n1234=len(n1234),
                        category=ro.StrVector([name1, name2, name3, name4]),
                        fill=ro.StrVector(['#FF6342', '#00FF63', '#63C6DE', '#FFFF00']),
                        cat_col=ro.StrVector(['#000000', '#000000', '#000000', '#000000']),
                        lty='blank',
                        cex=2,
                        # cat_pos=ro.IntVector([-45, -20, 20, 45]),
                        cat_cex=2,
                        cat_dist=ro.FloatVector([0.2, 0.2, 0.1, 0.1]),
                        ext_pos=30,
                        ext_dist=-0.05,
                        ext_length=0.85,
                        ext_line_lwd=2,
                        ext_line_lty="dashed"                        
                        ))
        dev_off()
        
    pro1,pro2,pro3,pro4 = tmpProList
    
    n12= pro1 & pro2
    n13= pro1 & pro3
    n14= pro1 & pro4
    n23= pro2 & pro3
    n24= pro2 & pro4
    n34= pro3 & pro4
    n123= pro1 & pro2 & pro3
    n124= pro1 & pro2 & pro4
    n134= pro1 & pro3 & pro4
    n234= pro2 & pro3 & pro4
    n1234= pro1 & pro2 & pro3 & pro4
    
    data = {}
    data['regionList'] = []
    data['vennList'] = {}
    i=0
    for word in string.uppercase:
        if i>14:break
        data['regionList'].append({'name':word})
        i+=1
    
    vennDict = {}
    vennDict['A'] = pro1 - pro2 - pro3 - pro4
    vennDict['B'] = pro3 - pro1 - pro2 - pro4
    vennDict['C'] = pro4 - pro1 - pro2 - pro3
    vennDict['D'] = pro2 - pro1 - pro3 - pro4
    vennDict['E'] = n13 - n123 - n134
    vennDict['F'] = n34 - n134 - n234 
    vennDict['G'] = n24 - n234 - n124 
    vennDict['H'] = n23 - n123 - n234
    vennDict['I'] = n12 - n123 - n124
    vennDict['J'] = n14 - n124 - n134
    vennDict['K'] = n134 - n1234
    vennDict['L'] = n234 - n1234
    vennDict['M'] = n123 - n1234
    vennDict['N'] = n124 - n1234
    vennDict['O'] = n1234
    
    
    for key,value in vennDict.iteritems():
        tmp = []
        i=1
        for p in value:
            tmp.append( {'no':i,'region':key,'name':p} )
            i+=1
        data['vennList'][key] = tmp
        
    name1,name2,name3,name4 = tmpNameList
    
    output_png = output_name + '.png'
    output_pdf = output_name + '.pdf'
    
    venng = importr('VennDiagram')
    venn4 = ro.r['draw.quad.venn']
    grid_draw = ro.r['grid.draw']
    dev_off = ro.r['dev.off']

    # ro.r.setwd(tmpdir)
    # prooutfile = 'venn_pro' + str(time.time()) + '.png'
    ro.r.png(output_png, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=300)
    myDraw()

    ro.r.pdf(output_pdf)
    myDraw()
    
    return data

def venn5D(tmpProList, tmpNameList, output_name):
    def myDraw():
        grid_draw(venn5(
                        area1=len(pro1),
                        area2=len(pro2),
                        area3=len(pro3),
                        area4=len(pro4),
                        area5=len(pro5),
                        n12=len(n12),
                        n13=len(n13),
                        n14=len(n14),
                        n15=len(n15),
                        n23=len(n23),
                        n24=len(n24),
                        n25=len(n25),
                        n34=len(n34),
                        n35=len(n35),
                        n45=len(n45),
                        n123=len(n123),
                        n124=len(n124),
                        n125=len(n125),
                        n134=len(n134),
                        n135=len(n135),
                        n145=len(n145),
                        n234=len(n234),
                        n235=len(n235),
                        n245=len(n245),
                        n345=len(n345),
                        n1234=len(n1234),
                        n1235=len(n1235),
                        n1245=len(n1245),
                        n1345=len(n1345),
                        n2345=len(n2345),
                        n12345=len(n12345),
                        category=ro.StrVector([name1, name2, name3, name4, name5]),
                        #fill=ro.StrVector(['#FF6342', '#00FF63', '#63C6DE', '#FFFF00','#E6E6FA']),
                        fill = ro.StrVector(["dodgerblue", "goldenrod1", "darkorange1", "seagreen3", "orchid3"]),
                        cat_col = ro.StrVector(['#000000', '#000000', '#000000', '#000000','#000000']),
                        lty='blank',
                        #cex=1.3,
                        cex = ro.StrVector([3, 3, 3, 3, 3, 2, 1.5, 2, 1.5, 2, 1.5, 2, 1.5, 2, 1.5, 2, 1.5, 2, 1.5, 2, 1.5, 2, 1.5, 2, 1.5, 2, 2, 2, 2, 2, 3]),
                        #cat_pos=ro.IntVector([0, -20, 20, 45]),
                        cat_cex=1.5,
                        cat_dist=ro.FloatVector([0.2, 0.15, 0.2, 0.2, 0.15]),
                        ext_pos=30,
                        ext_dist=-0.05,
                        ext_length=0.85,
                        ext_line_lwd=2,
                        ext_line_lty="dashed",
                        margin = 0.05                     
                        ))
        dev_off()
        
    pro1,pro2,pro3,pro4,pro5 = tmpProList
    
    n12= pro1 & pro2
    n13= pro1 & pro3
    n14= pro1 & pro4
    n15= pro1 & pro5
    n23= pro2 & pro3
    n24= pro2 & pro4
    n25= pro2 & pro5
    n34= pro3 & pro4
    n35= pro3 & pro5
    n45= pro4 & pro5
    n123= pro1 & pro2 & pro3
    n124= pro1 & pro2 & pro4
    n125= pro1 & pro2 & pro5
    n134= pro1 & pro3 & pro4
    n135= pro1 & pro3 & pro5
    n145= pro1 & pro4 & pro5
    n234= pro2 & pro3 & pro4
    n235= pro2 & pro3 & pro5
    n245= pro2 & pro4 & pro5
    n345= pro3 & pro4 & pro5
    n1234= pro1 & pro2 & pro3 & pro4
    n1235= pro1 & pro2 & pro3 & pro5
    n1245= pro1 & pro2 & pro4 & pro5
    n1345= pro1 & pro3 & pro4 & pro5
    n2345= pro2 & pro3 & pro4 & pro5
    n12345= pro1 & pro2 & pro3 & pro4 & pro5
    
    data = {}

    data['regionList'] = []
    for word in string.uppercase:
        data['regionList'].append({'name':word})
    data['regionList']+=[{'name':'AA'},{'name':'AB'},{'name':'AC'},{'name':'AD'},{'name':'AE'}]
    data['vennList'] = {}
    

    vennDict = {}
    vennDict['A'] = pro1-pro2-pro3-pro4-pro5
    vennDict['B'] = pro5-pro1-pro2-pro3-pro4
    vennDict['C'] = pro4-pro1-pro2-pro3-pro5
    vennDict['D'] = pro3-pro1-pro2-pro4-pro5
    vennDict['E'] = pro2-pro1-pro3-pro4-pro5
    vennDict['F'] = n14 - n124 - n134 - n145
    vennDict['G'] = n15 - n125 - n135 - n145
    vennDict['H'] = n35 - n345 - n235 - n135
    vennDict['I'] = n45 - n245 - n145 - n345
    vennDict['J'] = n24 - n124 - n234 - n245
    vennDict['K'] = n34 - n134 - n234 - n345
    vennDict['L'] = n13 - n123 - n134 - n135
    vennDict['M'] = n23 - n235 - n234 - n123
    vennDict['N'] = n25 - n125 - n235 - n245
    vennDict['O'] = n12 - n124 - n123 - n125
    vennDict['P'] = n124 - n1245 - n1234
    vennDict['Q'] = n145 - n1245 - n1345
    vennDict['R'] = n135 - n1345 - n1235
    vennDict['S'] = n345 - n1345 - n2345
    vennDict['T'] = n245 - n1245 - n2345
    vennDict['U'] = n234 - n1234 - n2345
    vennDict['V'] = n134 - n1345 - n1234
    vennDict['W'] = n123 - n1235 - n1234
    vennDict['X'] = n235 - n1235 - n2345
    vennDict['Y'] = n125 - n1245 - n1235
    vennDict['Z'] = n1245 - n12345
    vennDict['AA'] = n1345 - n12345
    vennDict['AB'] = n2345 - n12345
    vennDict['AC'] = n1234 - n12345
    vennDict['AD'] = n1235 - n12345
    vennDict['AE'] = n12345
    
    for key,value in vennDict.iteritems():
        tmp = []
        i=1
        for p in value:
            tmp.append( {'no':i,'region':key,'name':p} )
            i+=1
        data['vennList'][key] = tmp
        
    name1,name2,name3,name4,name5 = tmpNameList
    output_png = output_name + '.png'
    output_pdf = output_name + '.pdf'
    
    venng = importr('VennDiagram')
    venn5 = ro.r['draw.quintuple.venn']
    grid_draw = ro.r['grid.draw']
    dev_off = ro.r['dev.off']

    # ro.r.setwd(tmpdir)
    # prooutfile = 'venn_pro' + str(time.time()) + '.png'
    ro.r.png(output_png, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=300)
    #ro.r.png(output_png, bg="transparent")
    myDraw()

    ro.r.pdf(output_pdf,width = 20, height = 20)
    myDraw()


    
    return data
              
def plot_stack(input, output_name):
    code = binRSCRIPT + ' ' + Rscript_location + 'stack_plot.R %s %s' % (input, output_name)
    (status, output) = commands.getstatusoutput(code)

def pcaAdjust(tmpFile, tmpMetaFile, adjustedFile, todo_metalist):
    
    code  = 'input_file = "' + tmpFile + '"'
    code += '''
    '''
    code += 'outFile = "' + adjustedFile +'"'
    code += '''
    '''
    code += 'sampleInfo_file = "' + tmpMetaFile +'"'
    
    code += '''
    data = read.table(input_file,header=T,stringsAsFactors=FALSE,sep="\\t")
    k3.cv=as.matrix(data[,-1])
    ncol_data = ncol(k3.cv)
    nrow_data = nrow(k3.cv)
    
    k3.cv.t=t(k3.cv) #
    k3.mat=as.numeric(k3.cv.t)#
    k3.mat=matrix(k3.mat,ncol_data,nrow_data)#
    
    sampleInfo = read.table(sampleInfo_file,header=T,sep="\\t")
    # 'expName', 'species', 'instrument', 'dateOfExperiment', 'dateOfOperation', 'method','separation','sex','age','reagent','sample','tissueType','strain'
    species = sampleInfo[,3]
    instrument = sampleInfo[,4]
    dateOfExperiment = sampleInfo[,5]
    dateOfOperation = sampleInfo[,6]
    method = sampleInfo[,7]
    separation = sampleInfo[,8]
    sex = sampleInfo[,9]
    age = sampleInfo[,10]
    reagent = sampleInfo[,11]
    sample = sampleInfo[,12]
    tissueType = sampleInfo[,13]
    strain = sampleInfo[,14]
    circ_time = sampleInfo[,15]
    
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

    rownames(k3.mat)=colnames(data)[2:ncol(data)]
    '''
    tmp_metalist = [ 'as.factor(' + m + ')' for m in todo_metalist ]
    code += 'result = lm(k3.mat~' + '+'.join(tmp_metalist) + ')'
    code +='''
    res = residuals(result)
    res2 = cbind(as.character(data[,1]),t(res))#6220Symbols + 54samples
    colnames(res2)[1]=colnames(data)[1]
    write.table(res2, outFile, row.names=FALSE,sep="\\t",quote=FALSE)
    
    '''
    f=open('/tmp/myPCA_AdjustRscript.R','w') 
    f.write(code)
    f.close()
    
    
    r(code)
        
    return ( code, adjustedFile.replace(leafy_location, '') )


def thumb(file,size=(60,60)):
    im=Image.open(file)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(file+ ".thumbnail", "PNG")
