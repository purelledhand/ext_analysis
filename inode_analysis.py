import sys
import struct
import math

f = open(sys.argv[1], "rb")
f.seek(1024, 0)
sp = f.read(1024)

print(hex(struct.unpack_from("<H", sp, 0x38)[0]))

total_inode = struct.unpack_from("<I", sp, 0x0)[0]
print("total inode : ", hex(total_inode), total_inode)

total_block = struct.unpack_from("<I", sp, 0x4)[0]
print("total block :", hex(total_block), total_block)

inodes_per_group = struct.unpack_from("<I", sp, 0x28)[0]
print("inodes_per_group : ", hex(inodes_per_group), inodes_per_group)
blocks_per_group = struct.unpack_from("<I", sp, 0x20)[0]
print("blocks_per_group : ", hex(blocks_per_group), blocks_per_group)

print("ngroups(by block) : ", math.ceil(total_block/blocks_per_group))
print("ngroups(by Inode) : ", math.ceil(total_inode/inodes_per_group))
