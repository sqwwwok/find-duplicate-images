import json
import os
import sys
from imagededup.methods import CNN, PHash

from joinpath import join
from progressbar import printProgressBar


def findTwins(allImagesDir, findMethod):

  phasher = findMethod()

  encodings = phasher.encode_images(image_dir=allImagesDir)
  duplicates = phasher.find_duplicates(encoding_map=encodings)

  return duplicates

  
def moveDuplicates(allImagesDir, similarImagesDir, duplicates, symbol=''):
  if not os.path.exists(similarImagesDir):
    os.makedirs(similarImagesDir)

  l = len(duplicates)
  printProgressBar(0, l, prefix = 'Move duplicate files:', suffix = 'Complete', length = 50)

  for i, baseFileName in enumerate(duplicates):
    similarFileNameList = duplicates[baseFileName]
    if len(similarFileNameList) != 0:
      os.replace(join(allImagesDir, baseFileName), join(similarImagesDir, baseFileName))
      for index, similarFileName in enumerate(similarFileNameList):
        basename, _ = os.path.splitext(baseFileName)
        _, extension = os.path.splitext(similarFileName)

        # if symbol, add index and symbol in duplicated image
        if not symbol=='':
          similarFileNewName = "{}({}){}{}".format(basename, index+1, symbol, extension)
        else:
          similarFileNewName = similarFileName
        try:
         os.replace(join(allImagesDir, similarFileName), join(similarImagesDir, similarFileNewName))
        except:
          pass
        duplicates[similarFileName] = []
  
    printProgressBar(i + 1, l, prefix = 'Move duplicate files:', suffix = 'Complete', length = 50)


if __name__ == '__main__':
  # with open('config.json') as f:
  #   config = json.load(f)

  symbol = '$'
  
  allImagesDir = sys.argv[1]
  similarImagesDir = sys.argv[2]

  similarImagesDirWithMissDir = join(similarImagesDir, 'PhashMistakes/')

  duplicates = findTwins(allImagesDir, PHash)
  moveDuplicates(allImagesDir, similarImagesDirWithMissDir, duplicates)

  duplicates = findTwins(similarImagesDirWithMissDir, CNN)
  moveDuplicates(similarImagesDirWithMissDir, similarImagesDir, duplicates, symbol=symbol)
  
  # move mistake files into original assets
  file_names = os.listdir(similarImagesDirWithMissDir)
  for file_name in file_names:
    os.replace(join(similarImagesDirWithMissDir, file_name), join(allImagesDir, file_name))
  os.rmdir(similarImagesDirWithMissDir)

