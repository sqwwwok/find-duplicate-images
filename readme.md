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

# add path 
vi config.json
# {
#   "all_images_dir": "demo",
#   "duplicate_images_dir": "twins"
# }

python src/main.py
```

## Reference

[Image Deduplicator (imagededup)](https://github.com/idealo/imagededup#image-deduplicator-imagededup)