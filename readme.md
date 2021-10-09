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

## Config
```json
{
  "find": ["PHash", "CNN"],
  "pick": {
    "best": {
      "reference": "size",
      "biggest": true
    },
    "duplicate_symbol": "$"
  },
  "auto_remove": false
}
```

## Reference

[Image Deduplicator (imagededup)](https://github.com/idealo/imagededup#image-deduplicator-imagededup)