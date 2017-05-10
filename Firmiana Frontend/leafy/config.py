import ConfigParser
import sys, os, tempfile
import logging, logging.config

log = logging.getLogger(__name__)


def resolve_path(path, root):
    """If 'path' is relative make absolute by prepending 'root'"""
    if not(os.path.isabs(path)):
        path = os.path.join(root, path)   
    return path


config = ConfigParser.ConfigParser()
path = os.path.dirname(__file__)
config.readfp(open( path + '/config.ini'))
#config.readfp(open('/var/www/html/firmianaMS/firmiana/config.ini'))

#print config.sections()


def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
