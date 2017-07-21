import sys
import struct
import math


f = open(sys.argv[1], "rb")
f.seek(1024)
sp = f.read(1024)

print("FS Signature : ", hex(struct.unpack_from("<H", sp, 0x38)[0]))

#total inode
total_inode = struct.unpack_from("<I", sp, 0x0)[0]
print("total inode: ", hex(total_inode), total_inode)

#total block
total_block = struct.unpack_from("<I", sp, 0x4)[0]
print("total block: ", hex(total_block), total_block)

#inodes_per_group
inodes_per_group = struct.unpack_from("<I", sp, 0x28)[0]
print("inodes_per_group: ", hex(inodes_per_group), inodes_per_group)

#blokcs_per_group
blocks_per_group = struct.unpack_from("<I", sp, 0x20)[0]
print("blocks_per_group: ", hex(blocks_per_group), blocks_per_group)

ngroups = math.ceil(total_block / blocks_per_group)
print("ngroups(by block) : ", math.ceil(total_block / blocks_per_group))
print("ngroups(by inode) : ", math.ceil(total_inode / inodes_per_group))

#gdt_size
gdt_size = struct.unpack_from("<H", sp, 0xFE)[0]
if gdt_size == 0:
    gdt_size = 32

print("gdt_size : ", gdt_size)

block_size = struct.unpack_from("<I", sp, 0x18)[0]
block_size = pow(2, 10+block_size)
print("block_size : ", block_size)

offset = 2048
if block_size > 1:
    offset = block_size  

gdt_total_size = gdt_size * ngroups
n = math.ceil(gdt_total_size / block_size)

f.seek(offset)
gdt_block = f.read(block_size * n)

offset = 0
for i in range(ngroups):
    start_block_bitmap = struct.unpack_from("<I", gdt_block, offset+0)[0]
    start_inode_bitmap = struct.unpack_from("<I", gdt_block, offset+4)[0]
    start_inode_table = struct.unpack_from("<I", gdt_block, offset+8)[0]
    print("gdt #",i, hex(start_block_bitmap), hex(start_inode_bitmap), hex(start_inode_table))
    offset += gdt_size 
