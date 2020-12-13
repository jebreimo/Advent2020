# -*- coding: UTF-8 -*-
# ===========================================================================
# Copyright © 2020 Jan Erik Breimo. All rights reserved.
# Created by Jan Erik Breimo on 2020-12-05.
#
# This file is distributed under the BSD License.
# License text is included with the source distribution.
# ===========================================================================
import sys

entries = []
current_entry = {}
for line in (l.strip() for l in open(sys.argv[1])):
    if not line:
        if current_entry:
            entries.append(current_entry)
            current_entry = {}
    else:
        for kv in (s.split(":", 1) for s in line.split()):
            current_entry[kv[0]] = kv[1]

if current_entry:
    entries.append(current_entry)

required_keys = {"ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"}


def is_valid_height(s):
    if s[-2:] == "in":
        return 59 <= int(s[:-2]) <= 76
    elif s[-2:] == "cm":
        return 150 <= int(s[:-2]) <= 193
    else:
        return False


validators = {
    "byr": lambda s: 1920 <= int(s) <= 2002,
    "iyr": lambda s: 2010 <= int(s) <= 2020,
    "eyr": lambda s: 2020 <= int(s) <= 2030,
    "hgt": is_valid_height,
    "hcl": lambda s: len(s) == 7 and s[0] == "#" and int(s[1:], 16),
    "ecl": lambda s: s in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": lambda s: len(s) == 9 and int(s)
}


count1, count2 = 0, 0
for entry in entries:
    if len(required_keys.intersection(entry.keys())) == 7:
        count1 += 1
        try:
            for key in entry:
                validator = validators.get(key)
                if validator and not validator(entry[key]):
                    print("bad " + key, entry)
                    break
            else:
                count2 += 1
        except ValueError:
            print("exception " + key, entry)
            pass

print(count1)
print(count2)
