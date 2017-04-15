import numpy as np
from resizeimage import resizeimage
from PIL import Image, ImageChops
from collections import Counter
def compare(filePath):
    currentAr=list()
    im = Image.open(filePath).convert('RGB')
    width, height = im.size
    if width>60 and height>60:
       im = resizeimage.resize_cover(im, [60,60])
    im = trim(im)
    im=resizeimage.resize_cover(im, [38, 50], validate=False)
    iar=np.array(im)
    b=bal(iar)
    iar = threshold(iar,b)
    im.show()    
    matchedAr = []
    loadex = open('testing_data.txt','r').read()
    loadex = loadex.split('\n')
    iarl = iar.tolist()
    inQ = str(iarl)
    for eachExample in loadex:
        if len(eachExample)>3:
            splitEx = eachExample.split('::')
            currentNum = splitEx[0]
            currentAr = splitEx[1]
            eahPixEx = currentAr.split('],')
            eahPixInQ = inQ.split('],')
            x = 0
            while x < len(eahPixInQ):
                if eahPixEx[x] == eahPixInQ[x]:
                     matchedAr.append(currentNum)
                x=x+1
    return  matchedAr    
def createdatabase():
    testcase=open('testing_data.txt','a')
    types=range(1,56)
    a=string.ascii_uppercase
    for i in a:
        for eachtype in types:
            imgpath='testimg/'+i+str(eachtype)+'.png'
            im = Image.open(imgpath).convert('RGB')
            im=resizeimage.resize_cover(im, [38, 50], validate=False)
            im.save('testimg/aka/'+i+str(eachtype)+'1.png')
            iar=np.array(im)
            b=bal(iar)
            iar = threshold(iar,b)
            iarli=str(iar.tolist())
            writes=i+'::'+iarli+'\n'
            testcase.write(writes)   
def bal(imageArray):
    balanceAr = []
    for eahRow in imageArray:
        for eahPix in eahRow:
            avgNum = reduce(lambda x, y: x + y, eahPix[:3])/3
            balanceAr.append(avgNum)
    balance = sum(balanceAr[0:len(balanceAr)]) / len(balanceAr)
    return balance
def threshold(imageArray,balance):
    newAr = imageArray
    for eahRow in newAr:
        for eahPix in eahRow:
            if (reduce(lambda x, y: x + y, eahPix[:3]) / 3) > balance:
                for i in range(3):
                    eahPix[i] = 255
            else:
                for i in range(3):
                    eahPix[i] = 0
    return newAr
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

filepath=raw_input("enter file path::")
arr=compare(filepath)
x=Counter(arr)
print x
val=0
for key,value in x.items():
    if val<value:
        val=value
        k=key
print'input image is::',k
