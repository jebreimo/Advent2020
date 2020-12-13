# -*- coding: UTF-8 -*-
# ===========================================================================
# Copyright © 2020 Jan Erik Breimo. All rights reserved.
# Created by Jan Erik Breimo on 2020-12-06.
#
# This file is distributed under the BSD License.
# License text is included with the source distribution.
# ===========================================================================
import sys

group = []
groups = [group]
for line in (l.strip() for l in open(sys.argv[1])):
    if not line and group:
        group = []
        groups.append(group)
    else:
        group.append(set(line))

result1, result2 = 0, 0
for group in groups:
    if not group:
        continue
    s1, s2 = set(), set("abcdefghijklmnopqrstuvwxyz")
    for entry in group:
        s1.update(entry)
        s2.intersection_update(entry)
    result1 += len(s1)
    result2 += len(s2)

print(result1)
print(result2)
