import sys
import json
from urllib.request import urlopen
try:
    import dicttoxml
except ImportError:
    print("Please install dicttoxml using pip install dicttoxml")
    sys.exit()
from xml.dom.minidom import parseString

def usage():
    print("""
    Code snippet to demonstrate the conversion of a DALiuGE logical graph into a
    Python XML data structure.

    It should best be run interactively by using

    python -i [<path-to-logical-graph-file>]

    or (better)

    ipython -i [<path-to-logical-graph-file>]

    If no filename (or URL) is provided, the code will try to open one of the test graphs
    from the daliuge GIT repository.
    It will print the top level nodes of the logical graph and then you can explore
    the XML object called xg. The XML root element has been set to 'LogicalGraph'. 
    It is a standard xml.dom.minidom structure. Traversal is prety straight forward:

    xg.firstChild.childNodes[0].childNodes

    returns a list of nodes like:

    [<DOM Element: fileType at 0x109e75340>,
    <DOM Element: repoService at 0x109e752a8>,
    <DOM Element: repoBranch at 0x109e75210>,
    <DOM Element: repo at 0x109e75178>,
    <DOM Element: filePath at 0x109e750e0>,
    <DOM Element: sha at 0x109e75048>,
    <DOM Element: git_url at 0x109e75638>]

    NOTE: The graph loaded by default is 
    """)
    sys.exit()


def main(fname):

    try:
        f = urlopen(fname)
    except:
        print("Can't open file '{0}'! Please check filename.".format(fname))
        raise
        sys.exit()
    jg = json.load(f)
    f.close()
    xml_data = dicttoxml.dicttoxml(jg, custom_root="LogicalGraph")
    xg = parseString(xml_data)
    return xg

if __name__ == "__main__":
    if len(sys.argv) != 2:
        fname = 'https://raw.githubusercontent.com/ICRAR/daliuge/master/daliuge-translator/test/dropmake/logical_graphs/chiles_simple.json'
    else:
        fname = sys.argv[1].strip()
        if fname in ['-h', '--help']:
            usage()
        if fname.find('//:') == -1:
            fname = 'file://' + fname
    xg = main(fname)
    print([x.nodeName for x in xg.firstChild.childNodes])