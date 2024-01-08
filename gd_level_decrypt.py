import base64
from lxml import etree
import os
import zlib

class GetLevel:
    def __init__(self, lvl):
        self.name: str = getk(lvl, 2) or ''
        self.desc: str = base64.b64decode(getk(lvl, 3)).decode() or ''
        self.data: str = decrypt(getk(lvl, 4)) or ''
        self.attempts: int = int(getk(lvl, 18)) or 0
        self.length: int = int(getk(lvl, 23)) or 0
        self.jumps: int = int(getk(lvl, 36)) or 0
        self.copy: int = int(getk(lvl, 42)) or 0
        self.song: int = int(getk(lvl, 45)) or 0
        self.objCount: int = int(getk(lvl, 48)) or 0

def getk(element, num):
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
    with open(path, 'rb') as fr:
        data = fr.read()

    res = []
    for i in data:
        res.append(i ^ key)
    return bytearray(res).decode()

if __name__ == '__main__':
    # Windows save path
    LocalLevels = f"{os.getenv('LOCALAPPDATA')}\\GeometryDash\\CCLocalLevels.dat"
    GameManager = f"{os.getenv('LOCALAPPDATA')}\\GeometryDash\\CCGameManager.dat"
    save = decrypt(xor(LocalLevels, 11))
    root = etree.fromstring(save)
    
    levelsXml = root[0][1].findall('d')

    levels = []
    for level in levelsXml:
        levels.append(getLevel(level))

    for level in levels:
        print(level.name)
