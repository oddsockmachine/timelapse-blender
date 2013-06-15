from PIL import Image
import glob, os
from pprint import pprint
from itertools import islice

#choose a source directory
sourcedir = r"C:\B_Py\Blender\source"
outdir = sourcedir + r"\output"
if not os.path.exists(outdir):
    os.mkdir( outdir )


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
        print ( "Cannot load image '"+str( infile ) )+"'"

# check they are all the same size
temp_size = ( 0,0 )
to_remove = []
for k, v in inputs.iteritems():
    this_size = v.size
    if temp_size == ( 0,0 ):
        temp_size = this_size
    if temp_size != this_size:
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

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result



def save(img, outdir, count):
    try:
        img.save( outdir +"\\"+ str(count) +".jpg" )
        count += 1
    except:
        print "Oops, couldn't save"

    return count


# Keep track of the number of files written so they can all have unique names
file_count = 0

#choose how many blend steps: s
steps = 10.0

#The alpha transitions between each step
alphaStep = 1.0/steps

#sliding window, 2 wide
w = window( sorted(inputs) )
for imgs in w:
    print "Blending between " + str(imgs)

    a = (inputs[imgs[0]])
    b = (inputs[imgs[1]])


    alpha = 0
    while alpha < 1:
        # Don't save b (alpha=1), same as a(alpha=0)
        print "Alpha: " +str(alpha),
        blended = Image.blend(a, b, alpha)
        alpha += alphaStep
        file_count = save(blended, outdir, file_count)
        print " File: " +str(file_count)

# finally, save the last image
file_count = save( (inputs[img_list[-1]]), outdir, file_count )
print "Count: " +str(file_count)
