################################################################################
#                               3D Scanning Program                            #
#                                  James McDowell                              #
#                                 Requires: Python                             #
#                                 Imaging Library,                             #
#                                    Python 2.6,                               #
#                                   Blender 2.49                               #
################################################################################
from PIL import Image
import ImageDraw
import math

################################################################################
#                               Global Variables                               #
################################################################################

#Resolution adjustment
vertStep = 1 #Number of vertical pixels to step by
step = 10  #Degrees to step by

#Image object and data
img = Image.open("test1.jpg")
ImgWidth = img.size[0]
ImgHeight = img.size[1]

#Data structure that holds all of the pixel
#values of every image
pointCloud = []
for i in range(360):
    pointCloud.append(i)

#Data structure that holds all of the
#coordinates in a 3D object
finalObject = []
for i in range(360):
    finalObject.append(i)

#cordinates and faces
coords = []
faces = []

################################################################################
#                                   Functions                                  #
################################################################################

#cloudInit() initializes the point cloud,
#pointCloud[] holds all the scanned values
def cloudInit(rotateAngle):
    print "processing test" + str(rotateAngle + 1) + ".jpg"
    img = Image.open("test" + str(rotateAngle + 1) + ".jpg")

    #loaded image object
    pix = img.load()
    
    draw = ImageDraw.Draw(img)
    vertStripe = []
    vertStripe2 = []
    node = firstNode()

    #This loop ensures continuity
    #through a scanned image
    for i in range(node[1]):
        vertStripe.append((node[0], i))

    #Maximum allowable red value;
    #Minimum allowable red value;
    #Last encountered red pixel x average
    redMax = (255, 0, 0)
    redMin = (155, 0, 0)
    LastX = None
    LastY = None
    
    for y in range(ImgHeight):
        xSum = 0
        count = 0
            
        for x in range(ImgWidth):
            #pixelColor = img.getpixel((x, y))
            pixelColor = pix[x, y]
            
            #Pixel must be within the range of red rgb values
            if((pixelColor > redMin) and (pixelColor <= redMax)):
                xSum = x + xSum
                count = count + 1
                
        #The case that a red pixel average is found     
        if((xSum  != 0) and (count != 0)):
            LastX = xSum/count
            LastY = y
            vertStripe.append((LastX, y))

    #This loop ensures a continuous line
    #down the height of the image.
    for y in range(LastY, ImgHeight):
        vertStripe.append((LastX, y))

    #This loop draws a line over the laser stripe
    for i in range(len(vertStripe) - 1):
        if(vertStripe[i][0] != None):
            draw.line(vertStripe[i] + vertStripe[i + 1], (0, 255, 0))

    #Saving the newly drawn image as a .png ensures
    #that the reading loops always get a color value
    #img2 is the modified image, used in the reading loops
    img.save("test" + str(rotateAngle + 1) + ".png")
    img2 = Image.open("test" + str(rotateAngle + 1) + ".png")

    #loaded image object
    pix2 = img2.load()

    #Reading loops, as soon as the desired color is
    #found for a given fixed y, the inner loop breaks
    for y in range(ImgHeight):            
        for x in range(ImgWidth):
            #pixelColor = img2.getpixel((x, y))
            pixelColor = pix2[x, y]
            
            if(pixelColor  == (0, 255, 0)):
                vertStripe2.append((x, y))
                break
    pointCloud[rotateAngle] = vertStripe2
    print len(vertStripe2)

#firstNode() seeks out the critical node,
#The critical node is essential
#for a continous set of points. (see diagram)
def firstNode():
    #loaded image object
    pix = img.load()
    
    #minimum and maximum red pixel
    #values to be tested for.
    redMax = (255, 0, 0)
    redMin = (155, 0, 0)
    
    for y in range(ImgHeight):
        xSum = 0
        count = 0
        
        for x in range(ImgWidth):
            #pixelColor = img.getpixel((x, y))
            pixelColor = pix[x, y]

            #Pixel must be within the range of red rgb values            
            if((pixelColor > redMin) and (pixelColor <= redMax)):
                xSum = x + xSum
                count = count + 1

        if((xSum  != 0) and (count != 0)):
            firstNode = ((xSum/count), y)
            return firstNode
        
    #The case when no red pixels are found
    return (-1, -1)

#objectMaker() creates the 3D model
#given a set of measured distances
#(see diagram 1 for all the math)
def objectMaker():
    alpha = 46.8 #degrees
    L1 = 9.53 #cm
    L2 = 25.4 #cm
    L3 = 24.1 #cm
    A = 90 #degrees
    C = arcsin((L1 * sin(A))/L2)
    B = 180 - (A + C)
    thetaPrime = B - (alpha/2)

    for rotateAngle in range(0, 360, step):
        vertStripe = []
        
        for height in range(ImgHeight):
            theta = pointCloud[rotateAngle][height][0] * (alpha/ImgWidth)
            Bvirtual = thetaPrime + theta
            rPrime = L1 * tan(Bvirtual)
            r = L3 - rPrime
            x = r * cos(rotateAngle)
            y = r * sin(rotateAngle)
            z = height
            vertStripe.append([x, y, z])
        finalObject[rotateAngle] = vertStripe

def arcsin(n):
    #converts n from degrees to radians
    n = n * math.pi/180
    return math.asin(n) * 180/math.pi

def sin(n):
    #converts n from degrees to radians
    n = n * math.pi/180
    return math.sin(n)

def cos(n):
    #converts n from degrees to radians
    n = n * math.pi/180
    return math.cos(n)

def tan(n):
    #converts n from degrees to radians
    n = n * math.pi/180
    return math.tan(n)    

#writeToFile() writes the entire
#blender script (including all
#the necessary points)
def writeToFile():
    #File object
    filename = "createObject.py"
    FILE = open(filename,"w")

    #FILE.writelines("")
    #FILE.writelines('\n')

    #script setup
    FILE.writelines("#!BPY")
    FILE.writelines('\n')
    FILE.writelines('\n')
    FILE.writelines('"""')
    FILE.writelines('\n')
    FILE.writelines("Name: 'createObject'")
    FILE.writelines('\n')
    FILE.writelines("Blender: 244")
    FILE.writelines('\n')
    FILE.writelines("Group: 'Export'")
    FILE.writelines('\n')
    FILE.writelines("Tooltip: 'Wikibooks sample exporter'")
    FILE.writelines('\n')
    FILE.writelines('"""')
    FILE.writelines('\n')
    FILE.writelines('\n')
    FILE.writelines("from Blender import *")
    FILE.writelines('\n')
    FILE.writelines("import bpy")
    FILE.writelines('\n')
    FILE.writelines("#Original author's code")
    FILE.writelines('\n')
    FILE.writelines("editmode = Window.EditMode()")
    FILE.writelines('\n')
    FILE.writelines("if editmode: Window.EditMode(0)")
    FILE.writelines('\n')
    FILE.writelines("#coordinates and faces")
    FILE.writelines('\n')

    #coords and faces
    FILE.writelines("coords = " + str(coords))
    FILE.writelines('\n')
    FILE.writelines("faces = " + str(faces))
    FILE.writelines('\n')

    FILE.writelines("#Mesh object")
    FILE.writelines('\n')
    FILE.writelines("me = bpy.data.meshes.new('myMesh')")
    FILE.writelines('\n')
    FILE.writelines("me.verts.extend(coords)")
    FILE.writelines('\n')
    FILE.writelines("me.faces.extend(faces)")
    FILE.writelines('\n')
    FILE.writelines("#scene object")
    FILE.writelines('\n')
    FILE.writelines("scn = bpy.data.scenes.active")
    FILE.writelines('\n')
    FILE.writelines("ob = scn.objects.new(me, 'myObj')")
    FILE.writelines('\n')
    FILE.writelines("if editmode: Window.EditMode(1)  # optional, just being nice")

    #closing info
    FILE.writelines('Blender.Window.FileSelector(write, "Export")')
    FILE.close()

#coordsInit() Initializes all the coordinates
#to be printed in blender
def coordsInit():
    for height in range(0, ImgHeight, vertStep):
        for rotateAngle in range(0, 360, step):
            coords.append(finalObject[rotateAngle][height])

def facesInit():
    vertLimit = ImgHeight/vertStep
    cap = 360/step #8
    origin = 0
    p1 = 0
    p2 = cap
    p3 = cap + 1
    p4 = p1 + 1

    for i in range(vertLimit - 1):
        for j in range(cap - 1):
            faces.append([p1, p2, p3, p4])
            if(j == cap - 2):
                break
            p1 = p1 + 1
            p2 = p2 + 1
            p3 = p3 + 1
            p4 = p4 + 1
        faces.append([p3, p4, origin, p4 + 1])
        origin = origin + cap
        p1 = p1 + 2
        p2 = p2 + 2
        p3 = p3 + 2
        p4 = p4 + 2
      
################################################################################
#                                   Main                                       #
################################################################################

#Main loop, traverses through all captured images
for rotateAngle in range(0, 360, step):
    cloudInit(rotateAngle)

objectMaker()
coordsInit()
facesInit()
writeToFile()
print "done"
    
