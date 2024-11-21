import json


def baodong(rules, input):
    pack = set(input.copy())
    old_pack = set()

    while pack != old_pack:
        old_pack = pack.copy()
        for rule in rules:
            if set(rule["then"]).issubset(pack):
                continue
            if set(rule["if"]).issubset(pack):
                pack.add(rule["then"])
                print("\tUse:", rule["if"], "=>", rule["then"], "->", pack)

    return pack


def convert(path):
    # function to convert rules from txt to json
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    rules = []
    for line in lines:
        id = line.strip().split(":")[0]
        rule_if = (
            line.strip().split(":")[1].strip(", ").split("→")[0].strip().split("∧")
        )

        rule_if = [item.strip().replace(" ", "") for item in rule_if]

        rule_then = line.strip().split("→")[1].strip().replace(" ", "")

        rule = {"id": id, "if": rule_if, "then": rule_then}
        rules.append(rule)

    output = {}
    output.update({"rules": rules})

    with open("rules.json", "w", encoding="utf-8") as file:
        json.dump(output, file)

    return rules


# convert("rules.txt")

with open("cstt2.json", "r", encoding="utf-8") as file:
    knowledge_base = json.load(file)

facts = input("Nhập các sự kiện ban đầu (cách nhau bởi dấu phẩy): ").strip().split(",")
result = baodong(knowledge_base["rules"], facts)
print("Bao dong: ", ", ".join(result))
