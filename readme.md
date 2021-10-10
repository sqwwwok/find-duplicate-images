# Find Duplicate Images

## Introduction
Find duplicate images and move into the specific directory sorted by name.
+ All images
```shell
/demo
  a.jpg
  b.jpg
  c.jpg
  d.jpg
  e.jpg
```

+ After duplicate removal
```shell
/demo
  d.jpg

/twins
  a.jpg
  a_c.jpg
  b.jpg
  b_e.jpg
```

## Usage

Python 3.6+

```shell
pip install imagededup

python src/main.py /all/images/dir /duplicate/images/dir 
```

## Configuration
```js
{
  // find duplicate images in specific order
  // 'PHash' | 'CNN'
  "find": ["PHash", "CNN"],
  "pick": {
    // pick images you want to remain
    "best": {
      // 'size' | 'date' | 'name'
      "indicator": "size",
      "biggest": true
    },
    // rename duplicate images
    // {base_img_name}({symbol}{index}){original_name}{extension}
    // e.g. bar.jpg -> foo($1)bar.jpg
    "secondary": {
      "symbol": "$",
      "with_ori_name": false
    },
    // auto remove duplicate images
    "auto_remove_secondary": false
  }
}
```

## Reference

[Image Deduplicator (imagededup)](https://github.com/idealo/imagededup#image-deduplicator-imagededup)