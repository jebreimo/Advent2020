# -*- coding: UTF-8 -*-
# ===========================================================================
# Copyright © 2020 Jan Erik Breimo. All rights reserved.
# Created by Jan Erik Breimo on 2020-12-09.
#
# This file is distributed under the BSD License.
# License text is included with the source distribution.
# ===========================================================================
import sys

program = []
for line in (l.strip() for l in open(sys.argv[1]) if l.strip()):
    parts = line.split()
    program.append((parts[0].strip(), int(parts[1])))


def execute_program(program, acc, lin, visited):
    visited = visited.copy()
    while lin < len(program):
        if lin in visited:
            return acc, False
        visited.add(lin)
        cmd, val = program[lin]
        print(f"{lin+1:03d} {cmd} {val}")
        if cmd == "nop":
            lin += 1
        elif cmd == "acc":
            acc += val
            lin += 1
        elif cmd == "jmp":
            lin += val
    return acc, True


print(execute_program(program, 0, 0, set()))


def find_bad_instruction(program):
    acc = 0
    lin = 0
    visited = set()
    while lin < len(program):
        if lin in visited:
            return 0, acc, False
        visited.add(lin)
        cmd, val = program[lin]
        if cmd == "nop":
            acc2, terminated = execute_program(program, acc, lin + val, visited)
            if terminated:
                return lin + 1, acc2, True
            lin += 1
        elif cmd == "acc":
            acc += val
            lin += 1
        elif cmd == "jmp":
            acc2, terminated = execute_program(program, acc, lin + 1, visited)
            if terminated:
                return lin + 1, acc2, True
            lin += val
    return acc, True


print(find_bad_instruction(program))

# look_for = [("nop", (622, 626)]
# for i, instruction in enumerate(program):
#     cmd, val = instruction
#     if cmd == "nop" and i + val + 1 >= 622:
#         print(f"{i + 1} {cmd} {val:4} -> {i + val + 1}")
#     if cmd == "jmp" and i + val + 1 >= 622:
#         print(f"{i + 1} {cmd} {val:4} -> {i + val + 1}")
