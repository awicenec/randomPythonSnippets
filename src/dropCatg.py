import json
CATEGORIES = """[
        {"name":"Memory",   "class": "STORAGE", "basetype":"MEMORY", "type":"RAM"},
        {"name":"Memory",   "class": "STORAGE", "basetype":"MEMORY", "type":"GPU"},
        {"name":"File",     "class": "STORAGE", "basetype":"FILE",   "type":""},
        {"name":"NGAS",     "class": "STORAGE", "basetype":"NGAS",   "type":""},
        {"name":"S3",       "class": "STORAGE", "basetype":"S3",     "type":""},
        {"name":"Start",    "class": "STORAGE", "basetype":"",       "type":""},
        {"name":"End",      "class": "STORAGE", "basetype":"",       "type":""},
        {"name":"Data",     "class": "STORAGE", "basetype":"",       "type":""},
        {"name":"null",     "class": "STORAGE", "basetype":"NULL",   "type":""},
        {"name":"json",     "class": "STORAGE", "basetype":"",       "type":"json"},
        {"name":"Variables","class": "STORAGE", "basetype":"",       "type":""},

        {"name":"MKN",      "class": "CAPP", "basetype":"MKN",     "type":"mkn"},
        {"name":"Scatter",  "class": "CAPP", "basetype":"MKN",     "type":"scatter"},
        {"name":"Gather",   "class": "CAPP", "basetype":"MKN",     "type":"gather"},
        {"name":"GroupBy",  "class": "CAPP", "basetype":"MKN",     "type":"groupby"},
        {"name":"PLoop",    "class": "CAPP", "basetype":"LOOP",    "type":"ploop"},
        {"name":"SLoop",    "class": "CAPP", "basetype":"LOOP",    "type":"sloop"},
        {"name":"Branch",   "class": "CAPP", "basetype":"BRANCH",  "type":"branch"},
        {"name":"Exit",     "class": "CAPP", "basetype":"CONTROL", "type":"exit"},
        {"name":"Terminate","class": "CAPP", "basetype":"CONTROL", "type":"terminate"},

        {"name":"Component",    "class": "APP", "basetype":"PYTHON", "type":"Component"},
        {"name":"Mpi",          "class": "APP", "basetype":"PYTHON", "type":"Mpi"},
        {"name":"DynlibProcApp","class": "APP", "basetype":"DYNLIB", "type":"DynlibProcApp"},
        {"name":"DynlibApp",    "class": "APP", "basetype":"DYNLIB", "type":"DynlibApp"},
        {"name":"Docker",       "class": "APP", "basetype":"DOCKER", "type":"Docker"},
        {"name":"BashShellApp", "class": "APP", "basetype":"SHELL",  "type":"BashShellApp"},

        {"name":"Comment",     "class": "COMMENT", "basetype":"TEXT","type":"unicode"},
        {"name":"Description", "class": "COMMENT", "basetype":"TEXT","type":"html"}
    ]"""
class Categories():
    """
    Class represents a JSON structure containing a list of dictionaries. This is used by
    DALiuGE to configure a number of pre-defined categories of applications and data nodes
    on the logical graph level. 
    """
    def __init__(self, jcats=CATEGORIES):
        self.categories = json.loads(jcats)
        self.keys = self.categories[0].keys()
        

    def groupBy(self, groupkey, subkey=None, supress=''):
        """
        Method groups entries by one key <groupkey> and allows to
        specify another key <subkey> to appear in the value lists
        of the result. By default the group where <groupkey> has no
        value (groupkey='') is supressed from the result.

        Input:
            groupkey: string, name of the key to group by
            subkey: string, optional name of a key to appear in the result
                    (None by default)
            supress: string, optional value of groupkey to be supressed
                    from the result (default ''). The default will not produce
                    an entry for the group where the groupkey is undefined. In
                    order to get that as well supress needs to be set to an
                    non-existing key value (a good candidate might be ' ').
        
        Output: Dictionary containing the extracted groups. Each dictionary
                contains the list of category entries matching the group key.
        """
        if groupkey not in self.keys:
            return {}
        if subkey not in self.keys:
            subkey = None
        keys = list(set([c[groupkey] for c in self.categories]))
        groups = {key: [] for key in keys if key != supress}
        if subkey:
            _ = [groups[c[groupkey]].append(c[subkey]) for c in self.categories if c[groupkey] != supress]
        else:
            _ = [groups[c[groupkey]].append(c) for c in self.categories if c[groupkey] != supress]

        return groups


# produce the same set and list as in original code:
cats = Categories(jcats=CATEGORIES)
groups = cats.groupBy('class')
st = Categories(json.dumps(groups['STORAGE']))
app = Categories(json.dumps(groups['APP']))

STORAGE_TYPES = set(st.groupBy('basetype').keys())
APP_DROP_TYPES = list(app.groupBy('type').keys())
