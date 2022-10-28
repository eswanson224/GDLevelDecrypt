import base64
from lxml import etree
import os
import zlib


class GetLevel:
    def __init__(self, lvl):
        self.name: str = getk(lvl, 2, '')
        self.desc: str = base64.b64decode(getk(lvl, 3, '')).decode()
        self.data: str = decrypt(getk(lvl, 4, ''))
        self.attempts: int = int(getk(lvl, 18, 0))
        self.length: int = int(getk(lvl, 23, 0))
        self.jumps: int = int(getk(lvl, 36, 0))
        self.copy: int = int(getk(lvl, 42, 0))
        self.song: int = int(getk(lvl, 45, 0))
        self.objCount: int = int(getk(lvl, 48, 0))


def getk(element, num, default):
    if element.find(f"k[.='k{num}']") is None:
        return default
    else:
        return element.find(f"k[.='k{num}']").getnext().text

    '''
    2 = title
    3 = description(base64)
    4 = level data(base64 + gzip)
    18 = attempts
    23 = length
    34 = ???(Only on user made levels)
    36 = jumps
    42 = copied id
    45 = newground song id
    48 = object count
    '''


def decrypt(text) -> str:
    text = text.replace('-', '+').replace('_', '/')
    textbytes = zlib.decompress(base64.b64decode(text)[10:], -zlib.MAX_WBITS)
    return str(textbytes, 'utf8')


def xor(path, key) -> str:
    fr = open(path, 'rb')
    data = fr.read()
    fr.close()

    res = []
    for i in data:
        res.append(i ^ key)
    return bytearray(res).decode()


if __name__ == '__main__':
    LocalLevels = f"{os.getenv('LOCALAPPDATA')}\\GeometryDash\\CCLocalLevels.dat"
    GameManager = f"{os.getenv('LOCALAPPDATA')}\\GeometryDash\\CCGameManager.dat"
    save = decrypt(xor(LocalLevels, 11))
    root = etree.fromstring(save)
    
    levels = root[0][1].findall('d')
    
    print("1,8,2,285,3,15") # something, blockID, something, xPos, something, something
    print(GetLevel(levels[7]).data.split(';')[1])

'''
fw = open('files/save.txt', 'wb')
fw.write(etree.tostring(root, pretty_print=True))
fw.close()



for lvl in levels:
    l = GetLevel(lvl)
    print(l.name)
'''