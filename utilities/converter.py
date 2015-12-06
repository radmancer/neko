from PIL import Image
step = 10

def imageCopier(img):
        img.save(temp)

def copyCheck():
    for i in range(1, 361):
        img = Image.open("test" + str(i) + ".png")
    print "all good"

#Main
Input = raw_input("type all numbers found in the first image: ")
imgNumber = int(Input)

for i in range(1, 361, step):
    img = Image.open("DSC00" + str(imgNumber) + ".jpg")
    imgNumber = imgNumber + 1
    img.save("test" + str(i) + ".jpg")
