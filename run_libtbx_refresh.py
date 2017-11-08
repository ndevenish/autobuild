#!/usr/bin/env python
# coding: utf-8

"""Run a libtbx_refresh.py refresh file.

This wraps the required parts of libtbx so as to remove any dependency on
preconfigured libtbx build environments.
"""

from mock import Mock
import argparse
import imp
import sys
import os
import gzip
import math
import base64
from StringIO import StringIO
# from docopt import docopt
from types import ModuleType
from pathlib2 import Path, PosixPath
import textwrap
from collections import defaultdict

def norm_join(*args):
  return os.path.normpath(os.path.join(*args))

def tail_levels(path, number_of_levels):
  return os.path.join(*path.split(os.path.sep)[-number_of_levels:])

def write_this_is_auto_generated(f, file_name_generator):
  print >> f, """\
/* *****************************************************
   THIS IS AN AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
   *****************************************************
   Generated by:
     {}
 */
""".format(file_name_generator)

def new_module(name, doc=None):
  """Create a new module and inject it into sys.modules"""
  m = ModuleType(name, doc)
  m.__file__ = name + '.py'
  sys.modules[name] = m
  return m

# Explicitly replace the libtbx functionality we need
libtbx = new_module("libtbx")
libtbx.utils = new_module("libtbx.utils")
libtbx.forward_compatibility = new_module("libtbx.forward_compatibility")
# Imported entirely for side effect 
libtbx.load_env = new_module("libtbx.load_env")
libtbx.str_utils = new_module("libtbx.str_utils")
libtbx.str_utils.show_string = str
libtbx.str_utils.line_breaker = textwrap.wrap
libtbx.path = new_module("libtbx.path")
libtbx.math_utils = new_module("libtbx.math_utils")
libtbx.utils.write_this_is_auto_generated = write_this_is_auto_generated
libtbx.path.norm_join = norm_join
libtbx.path.tail_levels = tail_levels
libtbx.utils.warn_if_unexpected_md5_hexdigest = Mock()

# Fable requires a little more of the libtbx API

class group_args(object):
  def __init__(self, **keyword_arguments):
    self.__dict__.update(keyword_arguments)
  def __call__(self):
    return self.__dict__
  def __repr__(self):
    outl = "group_args"
    for attr in sorted(self.__dict__.keys()):
      tmp=getattr(self, attr)
      if str(tmp).find("ext.atom ")>-1:
        outl += "\n  %-30s : %s" % (attr, tmp.quote())
      else:
        outl += "\n  %-30s : %s" % (attr, tmp)
    return outl
  def merge(self, other):
    self.__dict__.update(other.__dict__)

class mutable(object):
  def __init__(self, value):
    self.value = value

class AutoType(object):
  singleton = None
  def __str__(self): return "Auto"
  def __eq__ (self, other) :
    return (type(other) is self.__class__)
  def __new__ (cls) :
    if (cls.singleton is None) :
      cls.singleton = super(AutoType, cls).__new__(cls)
    return cls.singleton


def product(seq):
  result = None
  for val in seq:
    if (result is None):
      result = val
    else:
      result *= val
  return result

def iround(x):
  return int(round(x))

def iceil(x):
  return int(math.ceil(x))

def expandtabs_track_columns(s, tabsize=8):
  result_e = []
  result_j = []
  j = 0
  for i,c in enumerate(s):
    if (c == "\t"):
      if (tabsize > 0):
        n = tabsize - (j % tabsize)
        result_e.extend([" "]*n)
        result_j.append(j)
        j += n
    else:
      result_e.append(c)
      result_j.append(j)
      if (c == "\n" or c == "\r"):
        j = 0
      else:
        j += 1
  return "".join(result_e), result_j

def dict_with_default_0(*args):
  return defaultdict(lambda : 0, *args)

libtbx.group_args = group_args
libtbx.Auto = AutoType()
libtbx.mutable = mutable
libtbx.utils.product = product
libtbx.utils.Sorry = Exception
libtbx.math_utils.iround = iround
libtbx.math_utils.iceil = iceil
libtbx.str_utils.expandtabs_track_columns = expandtabs_track_columns
libtbx.dict_with_default_0 = dict_with_default_0

# libtbx.topological_sort: Load this explitly here
def generate_topological_sort():
  TOPOLOGICAL_SORT = """H4sICK82RlkCA3RvcG9sb2dpY2FsX3NvcnQucHkArVZNj+M2DL37V7AB
  FrC3rjPJAN3BoDnsoUVPbQ97CwxDseVEjS0ZktwgKPa/l5RlWWkygz3sJbBE8okfj2RarXqoqna0o+
  ZVBaIflLbQiH+EEUomDW/BWHboeForKXlt8dZkrwmAZvJsYAf/fsVDqzRI1fAcGj4YEBIiddIGYMZw
  hCYt/LGk4yCc0H3tSVYiZMdl6m4yFBJgdbhWzvDbn4vNAjBdOikBNGRHN5MBgGghbW58y2bR7GFz51
  6nLlxXBzXKJmSDnqs6YSxe7EsXQwuDVjU3JsUXuWy4tNUUAf36d8gBFya+H+MGNzTHOsmgewsFwsAf
  SvKgHUPc5Db4l3nNcFGwgSCdxiTkneEzoHzLXpAgfu3Ws9KrXU6i45AK+AVklNo5bAe5F+ilq1QEEC
  kDHDRn58UYftzBxh9jZ6lkwnD47HiHxPhVa6XfS424y4aQZJsKX6VALE+lmV/FkdsoZb40hgpCbLop
  SsO7B9z0QqIlMSufw6+vxAWDPcmbdJ/OJMyb7JbCZZShx0TbLWzbLejZtzXTG5AUmIeco58YuqQw8S
  NEK3nsrpVH5g1+4aiRCGVS77kZa3pE6ZCb3EtUL2xlBCJwdx8Z777oMehhVSshWyGF5bvtx4/PTy4t
  q9UquQenZiUhfW9Wr7BfBZ3NKofltF2V+ay4fU/xeVUmX5PkZO3wul5zWVzEWQy8EaxQ+rim0/oL03
  8z+WH7yVTvJqVi3VFpYU/9jHe5XIpOHZm7FHUhuV0P7emnFnvKrA8oWj9ttk8vTy/Pm59f1sSZYrgm
  yZ9aHIVkHc32jvcIzqiykB6u8BcbO/idaS2MklkOvWpEK3gDVgGr0Ru8YJZH2QN7YrgflCM2DQumcb
  IDgzOfqHqX58JXgLhhxi7MRFwr9Xk+YOXm4Ul8oe3jO+rhZHw0EOXY+/FEConnQ2huFLs792w1KOOV
  3TlbRPcTkPojhPVGjPMAyDGc4NwURdDOFpYGr3rh3J3OuRMF/XKZJi623WIZngiEQSw7Yn2nePYhyt
  cyiwbPnTCJJ7B9r9EAY6d8hZsMfsDBG29IV945f4teNNuwL/tpwHjhYk2xkbicVkno42hAPc79BBEx
  ZplCk0fTCEK0phqYPaUP5gy0+D/If1q1rByHiu2wA4MFJmRCiLc6TkR7qlqhDSYOm6E+xbT19gVrvg
  uhqEyLIRIi9jVuCKCp+NDI/7vxjsVbAwOba3dH2bDT/h/ronmzou+98A8MakgnUK/yG8OVnbyJH+oy
  43szAlvqTHso+Q9dwNduywoAAA=="""
  tsF = gzip.GzipFile(mode='rb',fileobj=StringIO(base64.b64decode(TOPOLOGICAL_SORT)))
  ts = imp.new_module('libtbx.topological_sort')
  exec tsF.read() in ts.__dict__
  sys.modules["libtbx.topological_sort"] = ts
  return ts
libtbx.topological_sort = generate_topological_sort()

# End of Fable API

# import pdb
# pdb.set_trace()

class LibTBXPath(type(Path())):
  """Slight variant to PosixPath to behave like a libtbx path"""
  __abs__ = lambda x: str(x)

class FakeEnv(object):
  """Replaces Libtbx.env. Create at runtime to allow explicit build lookups"""
  class build_options(object):
    write_full_flex_fwd_h = False

  def __init__(self, module_root, output_root):
    self.module_root = module_root
    self.output_root = output_root
    self.build_path = LibTBXPath(output_root)

  def is_ready_for_build(self):
    return True

  def under_dist(self, module_name, path=".", test=None):
    """libtbx method to find a path in an existing module"""
    # assert test is os.path.isdir
    module_path = os.path.join(self.module_root, module_name)
    module_path_cctbx = os.path.join(self.module_root, "cctbx_project", module_name)
    if not os.path.isdir(module_path):
      assert os.path.isdir(module_path_cctbx)
      module_path = module_path_cctbx
    path = os.path.normpath(os.path.join(module_path, path))
    # print "Returning module path", path
    if test is not None:
      if not test(path):
        print("Failed test on searched path {}".format(path))
    return path

  def under_build(self, path):
    path = os.path.join(self.output_root, path)
    # print "Returning build path", path
    return path

  def find_in_repositories(self, relative_path, return_relocatable_path=False, test=os.path.isdir, optional=None):
    assert test is os.path.isdir
    # print "find_in_repositories for ", relative_path
    # return LibTBXPath(self.under_dist(relative_path))
    return self.under_dist(relative_path)

  def dist_path(self, module_path):
    return self.under_dist(module_path)

# END OF LIBTBX REPLACEMENTS

class RefreshSelf(object):
  """Class to be passed into a libtbx_refresh script as 'self'"""
  remove_obsolete_pyc_if_possible = Mock()


def inject_script(module_path, globals):
  """Load and run a python script with an injected globals dictionary.
  This is to emulate what it appears libtbx/scons does to run refresh scripts
  """
  path, module_filename = os.path.split(module_path)
  module_name, ext = os.path.splitext(module_filename)
  module = imp.new_module(module_name)
  module.__file__ = module_path
  vars(module).update(globals)
  with open(module_path) as f:
    exec f.read() in vars(module)
  return module

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--root", metavar="<rootpath>", help="The module root", required=True)
  parser.add_argument("--output", metavar="<outpath>", required=True)
  parser.add_argument("file", help="Path to file to process")

  args = parser.parse_args()

  source = args.file
  assert os.path.isdir(ags.root)
  sys.path.insert(0, os.path.join(args.root, "cctbx_project"))
  sys.path.insert(0, args.root)

  if not os.path.isdir(args.output):
    os.makedirs(args.output)

  fakeself = RefreshSelf()
  fakeself.env = FakeEnv(args.root, args.output)
  libtbx.env = fakeself.env

  inject_script(source, {"self": fakeself})





