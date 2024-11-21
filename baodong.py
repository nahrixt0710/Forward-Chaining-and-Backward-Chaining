import json


def baodong(rules, input):
    pack = set(input.copy())
    old_pack = set()

    while pack != old_pack:
        old_pack = pack.copy()
        for rule in rules:
            if set(rule["if"]) <= pack:
                pack.add(rule["then"])

    return pack


with open("cstt2-gbaonr.json", "r", encoding="utf-8") as file:
    knowledge_base = json.load(file)

facts = input("Nhập các sự kiện ban đầu (cách nhau bởi dấu phẩy): ").strip().split(",")
result = baodong(knowledge_base["rules"], facts)
print("Kết quả sau khi suy diễn: ", ", ".join(result))
