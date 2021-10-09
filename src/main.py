import json
import os
from imagededup.methods import PHash
from progressbar import printProgressBar

def parseJsonFile(jsonFile):
  f = open(jsonFile)
  data = json.load(f)
  f.close()
  return data


def findTwins(allImagesDir, similarImagesDir):

  print('All images in {}, Duplicates in {}'.format(allImagesDir, similarImagesDir))

  phasher = PHash()

  encodings = phasher.encode_images(image_dir=allImagesDir)
  duplicates = phasher.find_duplicates(encoding_map=encodings)

  return duplicates

  
def moveDuplicates(allImagesDir, similarImagesDir, duplicates):
  if not os.path.exists(similarImagesDir):
    os.makedirs(similarImagesDir)

  allBaseFileNames = os.listdir(allImagesDir)

  l = len(allBaseFileNames)
  printProgressBar(0, l, prefix = 'Move duplicate files:', suffix = 'Complete', length = 50)

  for idx, baseFileName in enumerate(allBaseFileNames):
    similarFileNameList = duplicates[baseFileName]
    if len(similarFileNameList) != 0:
      os.replace("{}/{}".format(allImagesDir, baseFileName), "{}/{}".format(similarImagesDir, baseFileName))
      for similarFileName in similarFileNameList:
        basename, _ = os.path.splitext(baseFileName)
        similarname, extension = os.path.splitext(similarFileName)
        similarFileNewName = "{}_{}{}".format(basename, similarname, extension)
        os.replace("{}/{}".format(allImagesDir, similarFileName), "{}/{}".format(similarImagesDir, similarFileNewName))
        duplicates[similarFileName] = []
  
    printProgressBar(idx + 1, l, prefix = 'Move duplicate files:', suffix = 'Complete', length = 50)


if __name__ == '__main__':
  config = parseJsonFile('config.json')
  allImagesDir=config["all_images_dir"]
  similarImagesDir=config['duplicate_images_dir']

  duplicates = findTwins(allImagesDir, similarImagesDir)
  moveDuplicates(allImagesDir, similarImagesDir, duplicates)
  
