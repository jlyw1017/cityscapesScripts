#!/usr/bin/python
#
# Converts the polygonal annotations of the Cityscapes dataset
# to images, where pixel values encode ground truth classes.
#
# The Cityscapes downloads already include such images
#   a) *color.png             : the class is encoded by its color
#   b) *labelIds.png          : the class is encoded by its ID
#   c) *instanceIds.png       : the class and the instance are encoded by an instance ID
# 
# With this tool, you can generate option
#   d) *labelTrainIds.png     : the class is encoded by its training ID
# This encoding might come handy for training purposes. You can use
# the file labes.py to define the training IDs that suit your needs.
# Note however, that once you submit or evaluate results, the regular
# IDs are needed.
#
# Uses the converter tool in 'json2labelImg.py'
# Uses the mapping defined in 'labels.py'
#

# python imports
from __future__ import print_function, absolute_import, division
import os, glob, sys

# cityscapes imports
from cityscapesscripts.helpers.csHelpers import printError
from cityscapesscripts.preparation.json2labelImg import json2labelImg

# The main method
def main():
    # Where to look for Cityscapes
    '''
     __file__ 得到当前文件路径
     但是若按绝对路径执行该文件，得到绝对路径
     若按相对路径，或者在sys.path下执行，则得到相对路径。
     为了保证得到绝对路径，用os.path.realpath()
     os.path.dirname获得该文件所在的文件夹名称
     os.path.join，组合成 目录/../..表示当前目录网上两次。
    '''
    if 'CITYSCAPES_DATASET' in os.environ:
        cityscapesPath = os.environ['CITYSCAPES_DATASET']#
    else:
        cityscapesPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','..')
    # how to search for all ground truth
    '''
    在文件往上两个的目录，即cityscapes根目录下，找gtFine的目录。
    加上*方便glob
    '''
    searchFine   = os.path.join( cityscapesPath , "gtFine"   , "*" , "*" , "*_gt*_polygons.json" )
    searchCoarse = os.path.join( cityscapesPath , "gtCoarse" , "*" , "*" , "*_gt*_polygons.json" )

    # search files
    filesFine = glob.glob( searchFine )
    filesFine.sort()
    filesCoarse = glob.glob( searchCoarse )
    filesCoarse.sort()

    # concatenate fine and coarse
    files = filesFine + filesCoarse
    # files = filesFine # use this line if fine is enough for now.

    # quit if we did not find anything
    '''
    在python中 None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()都相当于False
    '''
    if not files:
        printError( "Did not find any files. Please consult the README." )

    # a bit verbose
    print("Processing {} annotation files".format(len(files)))

    # iterate through files
    progress = 0
    print("Progress: {:>3} %".format( progress * 100 / len(files) ), end=' ')
    for f in files:
        # create the output filename
        dst = f.replace( "_polygons.json" , "_labelTrainIds.png" )
        '''
        替换并建一个新的list放图片。这里是选其中labelTrainIds这个类型
        '''
        # do the conversion 
        try:
            json2labelImg( f , dst , "trainIds" )
        except:
            print("Failed to convert: {}".format(f))
            raise

        # status 更新进度条
        progress += 1
        print("\rProgress: {:>3} %".format( progress * 100 / len(files) ), end=' ')
        # 输出刷新
        sys.stdout.flush()


# call the main
if __name__ == "__main__":
    main()
