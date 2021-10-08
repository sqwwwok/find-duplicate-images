import json
from imagededup.methods import PHash
from imagededup.utils import plot_duplicates
from json import *


def writeIntoFile(str):
  file = open(r'output/main.json','w')
  file.write(str)
  file.close()

def findTwins():
  phasher = PHash()

  # Generate encodings for all images in an image directory
  encodings = phasher.encode_images(image_dir='E:/images/iw233/2021-10-07/images')

  # Find duplicates using the generated encodings
  duplicates = phasher.find_duplicates(encoding_map=encodings)

  return duplicates

  # # plot duplicates obtained for a given file using the duplicates dictionary
  # plot_duplicates(image_dir='path/to/image/directory',
  #                 duplicate_map=duplicates,
  #                 filename='ukbench00120.jpg')
  
  
if __name__ == "__main__":
  duplicates = findTwins()
  writeIntoFile(json.dumps(duplicates)) 
  
