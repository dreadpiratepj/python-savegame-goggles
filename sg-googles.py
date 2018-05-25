#!/usr/bin/env python3
#
# savegame-goggles
#

import os
import sys
import argparse

from struct import pack, unpack
from collections import namedtuple


def read_aes_cmac_header(file_desc):
    '''
    record = pack(signature,
    b'\x00' * 16,   # cmac
    b'\x00' * 240)  # zeroes
    '''
    byte_count = 256
    record = file_desc.read(byte_count)
    signature = '<16s240s'
    header = namedtuple('aes_cmac_header', 'cmac zeroes')
    return header._make(unpack(signature, record))


def read_disf_header(file_desc):
    '''
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
    '''
    byte_count = 512
    record = file_desc.read(byte_count)
    fields = ['disf', 'magic', 'hash', 'first_partition_offset',
    'first_partition_size', 'second_partition_offset', 'second_partition_size',
    'save_partition_offset', 'save_partition_size', 'end']
    signature = '<4sL32sQQQQQQ424s'
    header = namedtuple('disf_header', ' '.join(fields))
    return header._make(unpack(signature, record))


def read_dpfs_header(file_desc):
    '''
    record = pack(signature,
    b'DPFS',
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
    '''
    byte_count = 68
    record = file_desc.read(byte_count)
    fields = ['dpfs', 'magic', 'offset_0', 'size_0', 'blocks_0', 'offset_1',
    'size_1', 'blocks_1', 'offset_2', 'size_2', 'blocks_2']
    signature = '<4sLQQLQQLQQL'
    header = namedtuple('dpfs_header', ' '.join(fields))
    return header._make(unpack(signature, record))


def read_ivfc_header(file_desc):
    '''
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
    0,              # offset, level 4
    0,              # size, level 4
    0,              # blocks, level 4
    0,              # reserved
    0,              # reserved
    b'\x00' * 48,   # unknown
    b'\x00' * 32)   # hash
    '''
    byte_count = 196
    record = file_desc.read(byte_count)
    fields = ['ivfc', 'magic', 'master_hash_size', 'offset_1', 'size_1',
    'blocks_1', 'reserved_1', 'offset_2', 'size_2', 'blocks_2', 'reserved_2',
    'offset_3', 'size_3', 'blocks_3', 'reserved_3', 'offset_4', 'size_4',
    'blocks_4', 'reserved_4', 'reserved_5', 'unknown', 'hash']
    signature = '<4sLQQQLLQQLLQQLLQQLLL48s32s'
    header = namedtuple('ivfc_header', ' '.join(fields))
    return header._make(unpack(signature, record))


def read_jngl_header(file_desc):
    '''
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
    '''
    byte_count = 512
    record = file_desc.read(byte_count)
    fields = ['jngl', 'magic', 'savedata_size', 'unknown_1', 'savedata_blocks',
    'unknown_2', 'unknown_3', 'unknown_4', 'padding']
    signature = '<4sLQQQLLQ464s'
    header = namedtuple('jngl_header', ' '.join(fields))
    return header._make(unpack(signature, record))


def read_save_header(file_desc):
    '''
    record = pack(signature,
    b'SAVE',
    0x0600000,      # magic
    0,              # number
    0,              # block size
    0,              # block size
    b'\x00' * 40)   # unknown
    '''
    byte_count = 72
    record = file_desc.read(byte_count)
    fields = ['save', 'magic', 'number', 'block_size_1', 'block_size_2', 'unknown']
    signature = '<4sLQQQ40s'
    header = namedtuple('save_header', ' '.join(fields))
    return header._make(unpack(signature, record))


def read_rmap_header(file_desc):
    '''
    record = pack(signature,
    b'RMAP',
    0x0100000,      # magic
    b'\x00' * 56)   # unknown
    '''
    byte_count = 64
    record = file_desc.read(byte_count)
    fields = ['rmap', 'magic', 'unknown']
    signature = '<4sL56s'
    header = namedtuple('rmap_header', ' '.join(fields))
    return header._make(unpack(signature, record))


def read_file_offset(file_desc):
    '''
    record = pack(signature,
    0,              # offset
    0)              # unknown
    '''
    byte_count = 8
    record = file_desc.read(byte_count)
    fields = ['offset', 'unknown']
    signature = '<LL'
    header = namedtuple('file_offset', ' '.join(fields))
    return header._make(unpack(signature, record))


def read_file_entry(file_desc):
    '''
    record = pack(signature,
    0,              # parent index
    b'A' * 64,      # filename
    0,              # file index
    0,              # file offset index
    0,              # size or count
    0,              # unknown
    0)              # next file index
    '''
    byte_count = 96
    record = file_desc.read(byte_count)
    fields = ['parent_index', 'filename', 'file_index', 'file_offset_index',
    'size_or_count', 'unknown', 'next_file_index']
    signature = '<L64sLLQQL'
    header = namedtuple('file_entry', ' '.join(fields))
    return header._make(unpack(signature, record))


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

with open(arguments.savegame, "rb") as file:
    cmac_header = read_aes_cmac_header(file)
    disf_header = read_disf_header(file)
    if disf_header.disf != b'DISF':
        print(disf_header.disf)
        print('DISF read error')
        sys.exit(-1)
    dpfs_header = read_dpfs_header(file)
    if dpfs_header.dpfs != b'DPFS':
        print(dpfs_header.dpfs)
        print('DPSF read error')
        sys.exit(-1)
    ivfc_header = read_ivfc_header(file)
    if ivfc_header.ivfc != b'IVFC':
        print(ivfc_header.ivfc)
        print('IVFC read error')
        sys.exit(-1)
    jngl_header = read_jngl_header(file)
    if jngl_header.jngl != b'JNGL':
        print(jngl_header.jngl)
        print('JNGL read error')
        sys.exit(-1)
    save_header = read_save_header(file)
    if save_header.save != b'SAVE':
        print(save_header.save)
        print('SAVE read error')
        sys.exit(-1)
    rmap_header_1 = read_rmap_header(file)
    if rmap_header_1.rmap != b'RMAP':
        print(rmap_header_1.rmap)
        print('RMAP 1 read error')
        sys.exit(-1)
    rmap_header_2 = read_rmap_header(file)
    if rmap_header_2.rmap != b'RMAP':
        print(rmap_header_2.rmap)
        print('RMAP 2 read error')
        sys.exit(-1)

print('Done')
sys.exit(0)
