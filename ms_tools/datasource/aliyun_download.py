import os
import oss
from lxml import etree as ET
from oss.oss_api import *
import datetime 
def aliyun_download(exp_info):
    
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
    instru_folder = exp_info['instru_folder'] 
    exp_name = exp_info['e_name']
    DIR = 'xxx'
    dir_instru = os.path.join(DIR,instru_folder)
    if not os.path.exists(dir_instru): 
        print dir_instru,' not exists'
        exit(1)
    
    dir_instru_expname = os.path.join(dir_instru,exp_name[3:])
    #print dir_instru_expname
    if not os.path.exists(dir_instru_expname): 
        print dir_instru_expname,' not exists'
        os.makedirs(dir_instru_expname)
        
    ID='xxx'
    KEY = 'xxx'
    #oss = OssAPI("oss.aliyuncs.com", ID, KEY)
    #file_on_cloud = 'Exp000974_250ug_24N_WTE_susion_20150111_F1_R1.raw'
    #save_as = "/home/galaxy/Aliyun_Exp000322_F1_R1_Lab0001.raw"
    #bucket = 'bprc'
    
    oss = OssAPI("oss-cn-beijing.aliyuncs.com", ID, KEY)
    
    bucket = 'china-data-bucket'
    
    #res = oss.get_object_to_file(bucket, file_on_cloud, save_as)
    #print res.read()
    res = oss.list_bucket(bucket, prefix=exp_name, marker='', delimiter='', maxkeys='', headers=None)
    (status, result_xml) = res.status, res.read()
    if not result_xml:
        return 'no file'
    
    if status != 200:
        return 'return code = %s'%status
        
    list_file = parse_xml(result_xml)
    print list_file
    for file in list_file:
        filename = file[0]
        etag = file[1]
        size = file[2]
        
        save_as = os.path.join( dir_instru_expname, filename)
        print save_as
        #continue
        
    
        if os.path.isfile( save_as ):
            local_size = os.path.getsize( save_as )
            print 'server_size=',size
            print 'local_size =',local_size
            if str(size) == str(local_size):
                print filename,' existed '
                continue
            else:
                if exp_info['check_flag']:
                    return 'undone'
                os.remove(save_as)
                
        print 'start  download %s [%s]'%(filename,time_now())
        oss = OssAPI("oss.aliyuncs.com", ID, KEY)
        res = oss.get_object_to_file(bucket, filename, save_as)
        print 'finish download %s [%s]'%(filename,time_now())
        download_status, download_result = res.status, res.read()
        print 'download_status=',download_status
        
    return 'ok'
            
def __main__():
    exp_info = {}
    exp_info['instru_folder'] = 'Fusion'
    exp_info['instru'] = 'Fusion'
    exp_info['e_name'] = 'Exp001421'
    exp_info['check_flag'] = 0
    res = aliyun_download(exp_info)
    print res
    
if __name__ == '__main__':
    __main__()
    