const fs = require('fs')

const duplicatesData = require('../output/main.json')



Object.keys(duplicatesData).forEach((baseImage, index) => {
  if(duplicatesData[baseImage].length) {
    fs.copyFileSync(`E:/images/iw233/2021-10-07/images/${baseImage}`, `duplicates/${baseImage}`)
    duplicatesData[baseImage].forEach((duplicateImage, index) => {
      const duplicateImageNewName = baseImage.replace('.jpg', `(${index+1}).jpg`)
      fs.copyFileSync(`E:/images/iw233/2021-10-07/images/${duplicateImage}`, `duplicates/${duplicateImageNewName}`)
      duplicatesData[duplicateImage] = []
    })
  }
  console.log(`${index} done`)
})