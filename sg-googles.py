#!/usr/bin/env python3
#
# savegame-goggles
#

import os
import argparse

from struct import pack, unpack
from collections import namedtuple


def read_aes_cmac_header(file_desc):
    signature = '<16s256s'
    record = pack(signature,
    b'\x00' * 16,   # cmac
    b'\x00' * 256)  # zeroes
    header = namedtuple('aes_cmac_header', 'cmac zeroes')
    header._make(unpack(signature, record))
    return header


def read_disf_header(file_desc):
    fields = ['disf', 'magic', 'hash', 'first_partition_offset',
    'first_partition_size', 'second_partition_offset', 'second_partition_size',
    'save_partition_offset', 'save_partition_size', 'end']
    signature = '<4sL32sQQQQQQ424s'
    record = pack(signature,
    b'DISF',
    0x0400000,      # magic
    b'\x00' * 32,   # hash
    0,              # first partition offset
    0,              # first partition size
    0,              # second partition offset
    0,              # second partition size
    0,              # save partition offset
    0,              # save partition size
    b'\x00' * 424)  # end
    header = namedtuple('disf_header', ' '.join(fields))
    header._make(unpack(signature, record))
    return header


def read_dpfs_header(file_desc):
    fields = ['dpsf', 'magic', 'offset_0', 'size_0', 'blocks_0', 'offset_1',
    'size_1', 'blocks_1', 'offset_2', 'size_2', 'blocks_2']
    signature = '<4sLQQLQQLQQL'
    record = pack(signature,
    b'DPSF',
    0x0100000,      # magic
    0,              # offset 0
    0,              # size 0
    0,              # blocks 0
    0,              # offset 1
    0,              # size 1
    0,              # blocks 1
    0,              # offset 2
    0,              # size 2
    0)              # blocks 2
    header = namedtuple('disf_header', ' '.join(fields))
    header._make(unpack(signature, record))
    return header


def read_ivfc_header(file_desc):
    fields = ['ivfc', 'magic', 'master_hash_size', 'offset_1', 'size_1',
    'blocks_1', 'reserved_1', 'offset_2', 'size_2', 'blocks_2', 'reserved_2',
    'offset_3', 'size_3', 'blocks_3', 'reserved_3', 'unknown', 'hash']
    signature = '<4sLLQQLLQQLLQQLL48s32s'
    record = pack(signature,
    b'IVFC',
    0x0200000,      # magic
    0,              # master hash size?
    0,              # offset, level 1
    0,              # size, level 1
    0,              # blocks, level 1
    0,              # reserved
    0,              # offset, level 2
    0,              # size, level 2
    0,              # blocks, level 2
    0,              # reserved
    0,              # offset, level 3
    0,              # size, level 3
    0,              # blocks, level 3
    0,              # reserved
    b'\x00' * 48,   # unknown
    b'\x00' * 32)   # hash
    header = namedtuple('ivfc_header', ' '.join(fields))
    header._make(unpack(signature, record))
    return header


def read_jngl_header(file_desc):
    fields = ['jngl', 'magic', 'savedata_size', 'unknown_1', 'savedata_blocks',
    'unknown_2', 'unknown_3', 'unknown_4', 'padding']
    signature = '<4sLQQQLLQ464s'
    record = pack(signature,
    b'JNGL',
    0x0100000,      # magic
    0,              # savedata size
    0,              # unknown
    0,              # savedata blocks
    0,              # unknown
    0,              # unknown
    0,              # unknown
    b'\x00' * 464)  # padding
    header = namedtuple('jngl_header', ' '.join(fields))
    header._make(unpack(signature, record))
    return header


def read_save_header(file_desc):
    fields = ['save', 'magic', 'number', 'block_size_1', 'block_size_2', 'unknown']
    signature = '<4sLQQQQ'
    record = pack(signature,
    b'SAVE',
    0x0600000,      # magic
    0,              # number
    0,              # block size
    0,              # block size
    0)              # unknown
    header = namedtuple('save_header', ' '.join(fields))
    header._make(unpack(signature, record))
    return header


def read_rmap_header(file_desc):
    fields = ['rmap', 'magic', 'unknown']
    signature = '<4sL56s'
    record = pack(signature,
    b'RMAP',
    0x0100000,      # magic
    b'\x00' * 56)   # unknown
    header = namedtuple('rmap_header', ' '.join(fields))
    header._make(unpack(signature, record))
    return header


def read_file_offset(file_desc):
    fields = ['offset', 'unknown_1', 'unknown_2']
    signature = '<3sBL'
    record = pack(signature,
    b'ABC',         # offset
    80,             # unknown
    0)              # unknown
    header = namedtuple('file_offset', ' '.join(fields))
    header._make(unpack(signature, record))
    return header


def read_file_entry(file_desc):
    fields = ['parent_index', 'filename', 'file_index', 'file_offset_index',
    'size_or_count', 'unknown', 'next_file_index']
    signature = '<L64sLLQQL'
    record = pack(signature,
    0,              # parent index
    b'A' * 64,      # filename
    0,              # file index
    0,              # file offset index
    0,              # size or count
    0,              # unknown
    0)              # next file index
    header = namedtuple('file_entry', ' '.join(fields))
    header._make(unpack(signature, record))
    return header


# Read our arguments.
parser = argparse.ArgumentParser(
description='utility for managing save files in savegame archives by @dreadpiratepj')
parser.add_argument('-outpath', metavar='outpath', type=str,
default=os.getcwd(), help='the path where to write the save files')
parser.add_argument('savegame', metavar='savegame', type=str,
help='the savegame archive to process')
parser.add_argument('operation', metavar='operation', type=str,
help='the operation to perform on the save files')
parser.add_argument('wildcard', metavar='wildcard', nargs='?', type=str,
default='*', help='the wildcard to match the save files on which to operate')
arguments = parser.parse_args()

read_aes_cmac_header(None)
read_disf_header(None)
read_dpfs_header(None)
read_ivfc_header(None)
read_jngl_header(None)
read_save_header(None)
read_rmap_header(None)
read_file_offset(None)
read_file_entry(None)
