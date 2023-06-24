import pathlib
import re
import sys

import pytest

test_file_path = pathlib.Path(__file__)
test_folder_path = test_file_path.parent.absolute()
proj_folder_path = test_folder_path.parent.absolute()

sys.path.insert(0, str(proj_folder_path))

import convert

@pytest.fixture
def link_sample_0() -> str:
    return ('''.. _Multi-process QEMU:

Multi-process QEMU
==================

This document describes how to configure and use multi-process qemu.
For the design document refer to docs/devel/multi-process.rst.

1) Configuration
----------------

multi-process is enabled by default for targets that enable KVM

''', '_Multi-process QEMU')


def test_get_rst_ref_re(link_sample_0):
    pattern = convert.get_rst_ref_re()
    m = re.compile(pattern)
    found = m.findall(link_sample_0[0])
    assert found[0] == link_sample_0[1]


def test_collect_all_refs_in_rst_files(link_sample_0):
    refs = convert.collect_all_refs_in_rst_files(link_sample_0[0])
    assert refs == [link_sample_0[1]]