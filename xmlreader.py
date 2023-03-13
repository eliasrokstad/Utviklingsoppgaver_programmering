from bs4 import BeautifulSoup as bs
import os

def get_reference(obj, tag):
    if len(obj.attrs[tag].split()) > 1:
        return [soup.find_all(id=ref)[0] for ref in obj.attrs[tag].split()]
    return soup.find_all(id=obj.attrs[tag].split()[0])[0]


def get_spatial(spatial):
    curves = get_reference(spatial, 'refcurves')
    curve = get_reference(curves, 'refcurve')
    return [[float(pos.attrs['x']), float(pos.attrs['y'])] for pos in curve.find_all('qdiposition2d')]

def get_pipes(file, shortname):
    # TODO: make global soup local
    global soup
    with open(file, 'r') as xml:
        content = xml.readlines()
    content = "".join(content)
    soup = bs(content, "lxml")
    names = soup.find_all('qdistringattribute', {"value" : shortname})
    pipes = dict()
    for name in names:
        pipe = name.parent
        pipes[pipe['id']] = dict()
        pipes[pipe['id']]['TYPE'] = shortname
        pipes[pipe['id']]['MAT'] = pipe.find('qdistringattribute', {"name": 'ShortMaterial'})['value']
        pipes[pipe['id']]['SN'] = pipe.find('qdistringattribute', {"name": 'PressureRating'})['value']
        pipes[pipe['id']]['DIM'] = pipe.find('qdirealattribute', {"name": 'Dimension'})['value']
        agg = get_reference(pipe, 'refaggregations')
        spatials = get_reference(agg, 'refspatials')
        pipes[pipe['id']]['HOR'] = get_spatial(spatials[0])
        pipes[pipe['id']]['VER'] = get_spatial(spatials[1])
        break

    return pipes




if __name__ == '__main__':
    #project = r'C:\Users\elir\AppData\Local\Qg4\1DF3C7C9AF4E492A9CDFA1131F312C\Job\7\1'
    #guid = '{b8fd5c8e-58bf-4b37-b56e-cb6e815e882a}'
    #task = 'f_va_03_1.xml'
    #path = os.path.join(project, guid)
    #dir_list = os.listdir(path)
    #file = os.path.join(project, guid, task)
    file = 'vaWs.xml'
    shortname = "OV"
    pipes = get_pipes(file, shortname).values()
    for values in pipes:
        print(values)
    pass