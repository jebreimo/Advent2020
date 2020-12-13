import sys

rules = {}
for line in (l.strip() for l in open(sys.argv[1])):
    main_parts = line.split("contain")
    from_color = " ".join(main_parts[0].split()[:2])
    to_colors = {}
    for c in main_parts[1].split(","):
        parts = c.split()
        if parts[0].isnumeric():
            to_colors[" ".join(parts[1:3])] = int(parts[0])
    rules[from_color] = to_colors


def can_contain_shiny_gold(from_color, rules, known_colors):
    if from_color in known_colors:
        return known_colors[from_color]
    result = False
    for to_color in rules[from_color]:
        if to_color == "shiny gold":
            result = True
            break
        else:
            result = can_contain_shiny_gold(to_color, rules, known_colors)
            if result:
                break
    known_colors[from_color] = result
    return result


result1 = 0
known_colors = {}
for rule in rules:
    if can_contain_shiny_gold(rule, rules, known_colors):
        result1 += 1
print(result1)


def count_bags(from_color, rules, known_counts):
    if from_color in known_counts:
        return known_counts[from_color]
    total_count = 0
    for to_color, count in rules[from_color].items():
        total_count += count * (1 + count_bags(to_color, rules, known_counts))
    known_counts[from_color] = total_count
    return total_count


print(count_bags("shiny gold", rules, {}))
