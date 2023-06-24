"""
Using commandline utility `pandoc` to convert markdown files to html files.

Usage:
  python convert.py <path>

"""
import functools
import pathlib
import re
import subprocess
import sys


from typing import Dict, List, Set, Tuple


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
  for rst_path in gen_rst_paths(path):
      convert_file(rst_path.absolute())


def gen_rst_paths(path: pathlib.Path) -> pathlib.Path:
  for rst_path in path.glob("**/*.rst"):
    if not is_ignore(rst_path):
      yield rst_path.absolute()


def convert_file(rst_path: pathlib.Path) -> Tuple[subprocess.CompletedProcess]:
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

  cmd = ("pandoc", "--from=rst", "--to=markdown", "--output="+str(md_path), str(rst_path))
  r0 = subprocess.run(cmd)

  r1 = subprocess.run(
    ('git', 'add', md_path.name),
    cwd=rst_path.parent,
  )

  return r0, r1


@functools.lru_cache(maxsize=1)
def get_rst_ref_re() -> re.Pattern:
  return re.compile(r':ref:`(.+?)`')


def collect_all_refs_in_rst_text(text:str) -> List[pathlib.Path]:
  p = get_rst_ref_re()
  return p.findall(text)


def find_rst_refs(proj_path:pathlib.Path) -> Dict[str, str]:
  result = {}

  for rst_path in gen_rst_paths(proj_path):
    result[rst_path.relative_to(proj_path)] = tuple(
      collect_all_refs_in_rst_text(rst_path.read_text())
    )

  return result


if "__main__" == __name__:
  main(sys.argv)
