from PIL import Image
import glob, os
from pprint import pprint


##
##image1 = Image.open("DSC_6263t.jpg")
##image2 = Image.open("DSC_6262t.jpg")
###comp = Image.composite(image1, image2, mask)
##alpha = 0.5
##blend = Image.blend(image1, image2, alpha)
##blend.save("blend.jpg", "JPEG")

#choose a source directory
sourcedir = r"C:\B_Py\Blender\source"
outdir = sourcedir + r"\output"
if not os.path.exists(outdir):
    os.mkdir( outdir )


#choose how many blend steps: s
steps = 2.0#

#The alpha transitions between each step
alphaStep = 1.0/steps

#get all relevant images in the dir
filelist = glob.iglob(sourcedir+r"\*.jpg")

inputs = {}
# load them
for infile in filelist:
    try:
        im = Image.open(infile)
        name = str(infile).split("\\")[-1]
        #name = str(infile)
        inputs[name] = im
    except IOError:
        print ( "Cannot load image "+str( infile ) )

# check they are all the same size
temp_size = ( 0,0 )
to_remove = []
for k, v in inputs.iteritems():
    this_size = v.size
    #print this_size
    if temp_size == ( 0,0 ):
        temp_size = this_size
    if temp_size != this_size:
        #print "\t\tWARNING!"
        to_remove.append( k )

# remove any that don't match the first one
for rem in to_remove:
    inputs.pop(rem)
    print "removed " + str(rem)

# create a list of keys to the imgs that can be sorted
img_list = []
for k in inputs.iterkeys():
    img_list.append(k)


img_list = sorted( img_list )


def get_img(i):
    return inputs[img_list[i]]

count = 0
for i, img in enumerate( img_list ):
    #print i, img
    if i < len(img_list)-1:
        a = get_img(i)
        b = get_img(i+1)
        print i, a
        print i+1, b
        a.save( outdir +"\\"+ str(count) + ".jpg" )
        count += 1
        blended = Image.blend(a, b, 0.5)
        new_name = str(img_list[i].split(".")[0])+"b."+img_list[i].split(".")[1]
        print new_name
        try:
            blended.save( outdir +"\\"+ str(count) + ".jpg" )
            count += 1
        except:
            print "oops"
        print "\n"
    if i == len(img_list)-1:
        b = get_img(i)
        b.save( outdir +"\\"+ str(count) + ".jpg" )
        count += 1



##
###blend between image[i] and [i+1]...[i+(s-1)]
##
###for each step in the blending
##img1 = imgDict[i]
##img2 = imgDict[i+steps]
##for blend in range(steps):
##    alpha = (float(steps+1))*alphaStep
##    blended = Image.blend(img1, img2, alpha)
##    #insert it into dict[(s*i)+1]...[(s*i)+s]
##    imgDict[(steps*i)+blend] = blended
##
##
###rename all files so they are in numerical order
##
##files = glob.glob("*.jpg")
##for i in range(len(files)-1):
##    print ( str(files[i])+ " + " +(str(files[i+1])) )