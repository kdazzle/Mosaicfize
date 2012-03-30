# To change this template, choose Tools | Templates
# and open the template in the editor.
import sys
import glob, os
import getopt
from PIL import Image
from random import choice
import datetime


__author__="k-dazzle"
__date__ ="$26-Mar-2012 10:29:49 AM$"

def main(argv=None):
    inputDir = None
    targetDir = None
    targetWidth = None
    targetHeight = None

    argList = {'inputDir': inputDir, 'targetDir': targetDir, 'width': targetWidth,
        'height': targetHeight}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:t:w:h", ["inputDir=",
            "help"])
        for opt, arg in opts:
            if opt in ("--help"):
                help = getHelpText()
                print help
            elif opt in ("-h", "--height"):
                argList['height'] = arg
            elif opt in ("-w", "--width"):
                argList['width'] = arg
            elif opt in ("-d", "--inputDir"):
                argList['inputDir'] = arg
                print "From Directory: %s" % (arg)
            elif opt in ("-t"):
                argList['targetDir'] = arg
                print "Saving to: %s" % (arg)
            else:
                print "Incorrect argument '%s', -h for help." % (opt)

    except getopt.GetoptError:
        sys.exit(2)

    mosaicfize(argList)

def mosaicfize(argList):
    argList = setDefaultArguments(argList)
    imagePathList = getImages(argList['inputDir'])

    if (len(imagePathList) == 0):
        print "Error: There are no images in the specified directory"
        sys.exit(2)

    imageSize = (argList['width'], argList['height'])
    backgroundImage = Image.new("RGB", imageSize, "rgb(0, 0, 0)")

    createMosaicBackground(backgroundImage, imagePathList, argList['targetDir'])



def setDefaultArguments(argList):
    """Returns a dict with the None arguments replaced by their defaults"""

    defaultHeight = 200
    defaultWidth = 640
    defaultTargetDir = "../complete"
    defaultInputDir = "../sourceImages"

    if (argList['height'] == None):
        argList['height'] = defaultHeight

    if (argList['width'] == None):
        argList['width'] = defaultWidth

    if (argList['inputDir'] == None):
        argList['inputDir'] = defaultInputDir

    if (argList['targetDir'] == None):
        argList['targetDir'] = defaultTargetDir

    return argList

def getImages(inputDir):
    """Returns a list of all the valid images in the inputDir"""
    import glob
    imageExtensions = "jpg"
    return glob.glob('%s/*.%s' % (inputDir, imageExtensions))

def createMosaicBackground(backgroundImage, imagePathList, targetDir):
    """Goes through the imageList and places them repeatedly in the background"""

    tileWidth = 20
    tileHeight = 25

    backgroundImageWidth = backgroundImage.size[0]
    backgroundImageHeight = backgroundImage.size[1]

    imageList = openAndResizeImages(imagePathList, (tileWidth, tileHeight))

    currentX = 0
    currentY = 0

    imagesAcross = backgroundImageWidth / tileWidth + 1
    imagesUp = backgroundImageHeight / tileHeight + 1

    for yImageCount in xrange(0, imagesUp):
        
        for xImageCount in xrange(0, imagesAcross):
            currentImage = choice(imageList).copy()
            upperLeftCorner = (currentX, currentY)
            backgroundImage.paste(currentImage, upperLeftCorner)
            currentX += tileWidth

        currentY += tileHeight
        currentX = 0

    filename = createFilename(targetDir)
    backgroundImage.save(filename, "JPEG")
    

def openAndResizeImages(imagePathList, size):
    """Goes through the imageList, opens, and resizes them so that they can be
    placed in the backgroundImage. The resizing does not effect the original files."""

    imageList = []

    for imagePath in imagePathList:
        image = Image.open(imagePath)
        image = image.copy()
        image = image.resize(size)
        imageList.append(image)

    return imageList

def createFilename(targetDir):
    """Create a filename for the background image. Uses a timestamp"""

    now = datetime.datetime.now()
    timestamp = "%s-%s-%s %s-%s-%s" % (
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
    
    return "%s/%s.jpg" % (targetDir, timestamp)


if __name__ == "__main__":
    main(sys.argv[1:])
