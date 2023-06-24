"""
Using commandline utility `pandoc` to convert markdown files to html files.

Usage:
  python convert.py <path>

"""

import functools
import pathlib
import subprocess
import sys


from typing import List, Set


def main(argv: List[str]):
  if len(argv) != 2:
    print("Usage: python convert.py <path>")
    sys.exit(1)

  path = pathlib.Path(argv[1])
  if not path.exists():
    print("Path does not exist: {}".format(path))
    sys.exit(1)

  if path.is_dir():
    convert_dir(path)
  else:
    convert_file(path)


@functools.lru_cache(maxsize=1)
def get_ignore_set() -> Set[str]:
  return set(('.git', '.github', '.gitlab',))


def is_ignore(path: pathlib.Path) -> bool:
  return set(path.parts).intersection(get_ignore_set())


def convert_dir(path: pathlib.Path):
  for rst_path in path.glob("**/*.rst"):
    if not is_ignore(rst_path):
      convert_file(rst_path)


def convert_file(rst_path: pathlib.Path) -> subprocess.CompletedProcess:
  '''
  Convert a markdown file to html file.

  pandoc -s -o <output> <input>

  ref : 
    https://pandoc.org/MANUAL.html
    https://stackoverflow.com/questions/45633709/how-to-convert-rst-files-to-md
  '''

  assert rst_path.is_file(), rst_path
  assert rst_path.suffix == ".rst", rst_path
  assert not set(rst_path.parts).intersection(get_ignore_set()), rst_path

  md_path = rst_path.with_suffix(".md")
  assert not md_path.exists(), md_path

  cmd = ("pandoc", "--from=rst", "--to=markdown", "--output="+str(md_path), str(rst_path))
  return subprocess.run(cmd)


if "__main__" == __name__:
  main(sys.argv)
