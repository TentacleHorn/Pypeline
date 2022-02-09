import json
import os
import time

ROOT = os.path.dirname(__file__)

from pypeline.graph.graph import FutureValue


def constant(v):
	return FutureValue(v)


s = time.time()
with open(f"{ROOT}/../info.json") as f:
	info = json.load(f)

VERSION = info['version']
dur = time.time() - s
print('wtf', dur)
