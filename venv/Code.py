import pytesseract
import re
from urllib import request
from urllib.request import urlopen
from PIL import Image
import sys,os
from PIL import Image,ImageDraw

codePath = r'D:/GitWorkSpace/pcbway/venv/Code/'
codeImg = 'code.png'
#image = Image.open('https://www.pcbway.com/common/verifyimage.aspx')

#vcode = pytesseract.image_to_string(image)

#print (vcode)

def view_code():
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
    image = Image.open(codePath +codeImg)
    # 将彩色图像转化为灰度图
    image = image.convert('L')
    binaryImage = image.point(initTable(), '1')
    clearNoise(binaryImage,50,4,4)
    binaryImage.show()
    binaryImage.save(codePath+"result.png")
   # vcode = pytesseract.image_to_string(binaryImage)
   # print (vcode)

def save_image(url,saveFileName):
    content = urlopen(url).read()
    with open(codePath +saveFileName, 'wb') as code:
        code.write(content)

#降噪 二值化
def initTable(threshold=140):
 table = []
 for i in range(256):
     if i < threshold:
         table.append(0)
     else:
         table.append(1)

 return table


# 二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
# 该函数也可以改成RGB判断的,具体看需求如何
def getPixel(image, x, y, G, N):
    L = image.getpixel((x, y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x, y - 1))
    else:
        return None

    # 降噪


# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image, G, N, Z):
    draw = ImageDraw.Draw(image)

    for i in range(0, Z):
        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                color = getPixel(image, x, y, G, N)
                if color != None:
                    draw.point((x, y), color)

if __name__ == '__main__':
    # 文件名
    save_image('https://www.pcbway.com/common/verifyimage.aspx',codeImg);
    view_code();