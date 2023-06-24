import pathlib
import subprocess
import sys

import pytest


test_file_path = pathlib.Path(__file__)
test_folder_path = test_file_path.parent.absolute()
proj_folder_path = test_folder_path.parent.absolute()

sys.path.insert(0, str(proj_folder_path))


import convert


@pytest.fixture
def link_sample_0() -> str:
    return (
        (
            'System emulation provides a wide range of device models to emulate '
            'various hardware components you may want to add to your machine. This '
            'includes a wide number of VirtIO devices which are specifically tuned '
            'for efficient operation under virtualisation. Some of the device '
            'emulation can be offloaded from the main QEMU process using either '
            'vhost-user (for VirtIO) or :ref:`Multi-process QEMU`. If the platform '
            'supports it QEMU also supports directly passing devices through to '
            'guest VMs to eliminate the device emulation overhead. See '
            ':ref:`device-emulation` for more details. '
        ),
        ['Multi-process QEMU', 'device-emulation']
    )


def test_get_rst_ref_re(link_sample_0):

    m = convert.get_rst_ref_re()

    assert m.findall(link_sample_0[0]) == link_sample_0[1]


def test_collect_all_refs_in_rst_files(link_sample_0):
    refs = convert.collect_all_refs_in_rst_text(link_sample_0[0])
    assert refs == link_sample_0[1]
