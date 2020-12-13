# -*- coding: UTF-8 -*-
# ===========================================================================
# Copyright © 2020 Jan Erik Breimo. All rights reserved.
# Created by Jan Erik Breimo on 2020-12-06.
#
# This file is distributed under the BSD License.
# License text is included with the source distribution.
# ===========================================================================
import sys

paths = []
for line in (l.strip() for l in open(sys.argv[1])):
    if len(line) != 10:
        continue
    p = line.translate({ord(s[0]): s[1] for s in ("B1", "F0", "R1", "L0")})
    paths.append(int(p, 2))
print(max(paths))
for i in range(1, len(paths)):
    if paths[i] != paths[i-1] + 1 and paths[i] % 8 != 0:
        print(paths[i] - 1)
