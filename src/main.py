import json
import os
import sys
from imagededup.methods import CNN, PHash

from utils import join, printProgressBar

def findByOneWay(findMethod, allImagesDir, similarImagesDir, symbol='$', withOriName=False, pickBy='', pickBiggest=True, rename=True, autoRemove=False):


  def findTwins(allImagesDir, findMethod):

    phasher = findMethod()

    encodings = phasher.encode_images(image_dir=allImagesDir)
    duplicates = phasher.find_duplicates(encoding_map=encodings)

    return duplicates


  def processData(duplicates):
    res = []

    # convert digraph to undigraph
    duplicateSets = dict([base, set(dups)] for base, dups in duplicates.items())
    for base, dups in duplicateSets.items():
      for dup in dups:
        duplicateSets[dup].add(base)
    duplicateSets = dict([base, list(dups)] for base, dups in duplicateSets.items())

    #  undigraph traversal
    for base in duplicateSets:
      curSet = {base}
      def addTwin(base):
        if(len(duplicateSets[base])==0):
          return
        for twin in duplicateSets[base]:
          curSet.add(twin)
          duplicateSets[base].remove(twin)
          addTwin(twin)
      addTwin(base)

      if len(curSet)>1:
        res.append(list(curSet))

      for b in curSet:
        duplicateSets[b] = []
      
    return res

    
  def moveTwins(allImagesDir, similarImagesDir, duplicatesList):
    
    if not os.path.exists(similarImagesDir):
      os.makedirs(similarImagesDir)

    l = len(duplicatesList)
    printProgressBar(0, l, prefix = 'Move duplicate files:', suffix = 'Complete', length = 50)
    
    for i, duplicates in enumerate(duplicatesList):
      if len(duplicates)<=1:
        continue

      if pickBy=='size':
        duplicates.sort(key=lambda filename: os.path.getsize(join(allImagesDir, filename)), reverse=pickBiggest)

      baseFileName = duplicates.pop(0)

      os.replace(join(allImagesDir, baseFileName), join(similarImagesDir, baseFileName))

      for index,similarFileName in enumerate(duplicates):
        similarFile = join(allImagesDir, similarFileName)
        if autoRemove:
          os.remove(similarFile)
        else:
          basename, _ = os.path.splitext(baseFileName)
          similarname, extension = os.path.splitext(similarFileName)
          similarFileNewName = "{}({}{}){}{}".format(basename, symbol, index+1, similarname if withOriName else '', extension) if rename else similarFileName   
          os.replace(similarFile, join(similarImagesDir, similarFileNewName))

      printProgressBar(i + 1, l, prefix = 'Move duplicate files:', suffix = 'Complete', length = 50)


  oriData = findTwins(allImagesDir, findMethod)
  duplicatesList = processData(oriData)
  moveTwins(allImagesDir, similarImagesDir, duplicatesList)


if __name__ == '__main__':
  with open('config.json') as f:
    config = json.load(f)

  symbol = '$'
  
  allImagesDir = sys.argv[1]
  similarImagesDir = sys.argv[2]

  similarImagesDirWithMissDir = join(similarImagesDir, 'PhashMistakes/')

  findByOneWay(PHash, allImagesDir, similarImagesDirWithMissDir,
    rename=False,
    autoRemove=False
  )

  findByOneWay(CNN, similarImagesDirWithMissDir, similarImagesDir,
    symbol = config['pick']['secondary']['symbol'],
    withOriName=config['pick']['secondary']['with_ori_name'],
    pickBiggest=config['pick']['best']["biggest"],
    pickBy=config['pick']['best']['indicator'],
    autoRemove=config['pick']['auto_remove_secondary']
  )
  
  # move mistake files into original assets
  file_names = os.listdir(similarImagesDirWithMissDir)
  for file_name in file_names:
    os.replace(join(similarImagesDirWithMissDir, file_name), join(allImagesDir, file_name))
  os.rmdir(similarImagesDirWithMissDir)

