import os

def join(*arguments):
  return os.path.join(*locals()["arguments"]).replace('\\', '/')