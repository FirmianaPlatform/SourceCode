import os
import oss
from lxml import etree as ET
from oss.oss_api import *
import datetime 
def aliyun_delete(exp_info):
    
    def time_now():
        return datetime.datetime.now().strftime('%X') 

    def parse_xml(input):
        list_file = []
        #print input
        try:
            #mzxmlfile = ET.parse(input)
            root = ET.fromstring(input)
        except Exception,e:
            #print e
            print 'error ET.parse(input)'
            exit(1)
        
        #root = mzxmlfile.getroot()
        for content in root.iter('Contents'):
            #print '##############'
            filename = content.find('Key').text
            etag = content.find('ETag').text
            size = content.find('Size').text
            #print filename,etag,size
            list_file.append([filename,etag,size])
        
        return list_file
  
    ID='xxx'
    KEY = 'xxx'
    oss = OssAPI("oss.aliyuncs.com", ID, KEY)
    #file_on_cloud = 'Exp000974_250ug_24N_WTE_susion_20150111_F1_R1.raw'
    #save_as = "/home/galaxy/Aliyun_Exp000322_F1_R1_Lab0001.raw"
    bucket = 'bprc'
    #res = oss.get_object_to_file(bucket, file_on_cloud, save_as)
    #print res.read()
    prefix = exp_info['e_name']
    check_again = raw_input('Delete %s ?(y/n) : '%prefix)
    if check_again != 'y':
        exit(0)
    res = oss.list_bucket(bucket, prefix=prefix, marker='', delimiter='', maxkeys='', headers=None)
    (status, result_xml) = res.status, res.read()
    #print result_xml
    if not result_xml:
        return 'no file'
    
    if status != 200:
        return 'return code = %s'%status
        
    list_file = parse_xml(result_xml)

    for file in list_file:
        print  ' Deleting...',file[0]
        res = oss.delete_object(bucket, file[0], headers=None)
        print "%s\n%s" % (res.status, res.read()) 
        
        #break
        
    return 'ok'
            
def __main__():
    exp_info = {}
    exp_info['instru'] = 'Fusion'
    exp_info['e_name'] = 'Exp'+raw_input('Delete what?[000974,000975...] : ')#'Exp000974'
    
    res = aliyun_delete(exp_info)
    print res
    
if __name__ == '__main__':
    __main__()
    