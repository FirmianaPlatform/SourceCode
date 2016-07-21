import os, sys
from bioblend.galaxy import GalaxyInstance

ms_tools_path = os.path.join( os.path.dirname( __file__ ), '..')
GALAXY_ROOT = os.path.join( ms_tools_path, '..', '..' )

sys.path.insert(1, ms_tools_path)
from models.gardener_control import *

print time_now()

def get_filename(conn, meta, eid):
    t = Table('gardener_search', meta, autoload=True, autoload_with=engine)
    s = select([t.c.name]).where(and_(t.c.exp_id == eid,
                                    t.c.rank == 1,
                                    t.c.type == 'fraction'))
    res = conn.execute(s)
    file_name_list = []
    for row in res:
        fn = row['name']
        file_name_list.append(fn)
    return sorted(file_name_list)

exp_name = 'Exp000683'
eid = get_exp_id(conn, meta, exp_name)
file_name_list = get_filename(conn, meta, eid)


apikey='xxx'
url="192.168.12.88:8080"
gi = GalaxyInstance(url, key=apikey)

hist_name_list = [ file_name + '.raw - General Workflow' for file_name in file_name_list]


for hname in hist_name_list:
    print '# '+hname
    #continue
    for history in gi.histories.get_histories(name=hname):
        hkey = history['id']
        #print 'hkey=',hkey
        #print history
        #exit(0)
        continue
        hist = gi.histories.show_history(hkey)
        for error_key in hist['state_ids']['error']:
            print 'error_key: '+error_key
            #tool_id = 'ms_identification_mascot'
            #res = gi.tools.run_tool(hid, tool_id, {'src':'hda','id':'c46c005a5dfa3261','store_to_db':'yes'})
            #print res
            #exit(0)
            
print time_now()
