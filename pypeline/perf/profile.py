import json
import os
from dataclasses import dataclass
from time import time

SAVE_DIR = None


@dataclass
class OperationSpecs:
	duration: float


class Recording:
	def __init__(self, out_dir: str):
		self.start = time()
		self.out_dir = out_dir

	def _meta(self):
		return os.path.join(self.out_dir, "meta.json")

	@property
	def duration(self):
		return time() - self.start

	def dump(self):
		if not os.path.exists(self.out_dir):
			os.makedirs(self.out_dir, exist_ok=True)

		with open(self._meta(), "w") as f:
			json.dump(dict(start=self.start, duration=self.duration), f)

	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.dump()


def benchmark(out_dir=None):
	return Recording(out_dir=out_dir)
