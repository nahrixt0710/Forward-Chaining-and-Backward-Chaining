import json


def suy_dien_tien(facts, goal):
    inferred = set(facts)
    visited_rules_id = []  # Lưu các luật đã áp dụng để tránh vòng lặp vô hạn
    visited_rules = []
    steps = []  # Lưu các bước suy diễn
    while True:
        if goal in inferred:
            # steps.append(f"Muc tieu '{goal}' da dat duoc.")
            return visited_rules, steps
        is_used = False  # Kiểm tra xem có áp dụng luật nào không
        for rule in knowledge_base["rules"]:
            if all(condition in inferred for condition in rule["if"]):
                # if rule["then"] not in inferred:  # Tránh áp dụng lặp lại luật
                if rule["id"] not in visited_rules_id:
                    inferred.add(rule["then"])
                    steps.append(
                        f"{' ∧ '.join(rule['if'])} → {rule['then']} (theo {rule['id']}) \n\t{list(inferred)}\n"
                    )
                    visited_rules_id.append(rule["id"])
                    visited_rules.append(rule)
                    is_used = True
                    break  # Sau khi áp dụng luật, quay lại từ luật đầu tiên
        if is_used:  # Nếu đã áp dụng luật, quay lại xét từ đầu
            continue
        break  # Không có luật nào mới được áp dụng

    return steps


def select_rule(facts, rules):
    """
    Chọn quy tắc phù hợp nhất dựa trên số điều kiện cần tìm (không thuộc facts).
    """
    rules.sort(key=lambda r: len(set(r["if"]) - set(facts)))

    # Trả về quy tắc phù hợp nhất hoặc None nếu không có
    return rules[0] if rules else None


def suy_dien_lui(facts, goal, visited_rules):
    queue = [goal]
    checked_goals = set()
    inferred = set(facts)
    steps = []
    rule_used_id = []

    while queue:
        cur_goal = queue.pop(0)

        if cur_goal in checked_goals:
            continue

        if cur_goal in inferred:
            checked_goals.add(cur_goal)
            continue

        rule_list = []
        best_rule = {}
        # for rule in knowledge_base["rules"]:
        #     if rule["then"] == cur_goal and rule["then"] not in checked_goals:
        #         rule_list.append(rule)
        #         best_rule = rule
        for rule in visited_rules:
            if rule["then"] == cur_goal and rule["then"] not in checked_goals:
                rule_list.append(rule)
                best_rule = rule

        if len(rule_list) > 1:
            best_rule = select_rule(inferred, rule_list)

        for condition in best_rule["if"]:
            if condition not in checked_goals and condition not in inferred:
                queue.append(condition)  # Thêm vào queue nếu chưa xử lý

        checked_goals.add(cur_goal)
        rule_used_id.append(best_rule["id"])

    had = set(facts)
    for rule in visited_rules:
        if rule["id"] in rule_used_id:
            steps.append(
                f"{' ∧ '.join(rule['if'])} → {rule['then']} (theo {rule['id']}) \n\t{had.union(rule["then"])}\n"
            )
            had = had.union(rule["then"])

    return steps


def baodong(rules, input):
    pack = set(input.copy())
    old_pack = set()

    while pack != old_pack:
        old_pack = pack.copy()
        for rule in rules:
            if set(rule["if"]).issubset(pack):
                # print("\tUse:", rule["if"], "=>", rule["then"], "->", pack)
                pack.add(rule["then"])

    return pack


# Đọc cơ sở tri thức từ file JSON
with open("cstt4.json", "r") as file:
    knowledge_base = json.load(file)

# Hàm chính để nhập dữ liệu và chạy thuật toán
if __name__ == "__main__":
    # Nhập facts ban đầu
    facts = input("Nhap gia thiet (cach nhau boi dau phay): ").strip().split(",")
    facts = [fact.strip() for fact in facts]

    # Nhập goal
    goal = input("Nhap muc tieu can tim: ").strip()

    print("\nTim kiem bao dong...")
    baodong_result = baodong(knowledge_base["rules"], facts)

    print("Bao dong:", baodong_result)
    if goal in baodong_result:
        # Chạy suy diễn tiến
        print("\nSuy dien tien...")
        visited_rules, forward_steps = suy_dien_tien(facts, goal)
        for i, step in enumerate(forward_steps, 1):
            print(f"Step {i}: {step}")
        # Chạy suy diễn lùi
        print("\nRut gon (suy dien lui)...")
        backward_steps = suy_dien_lui(facts, goal, visited_rules)
        for i, step in enumerate(backward_steps, 1):
            print(f"Step {i}: {step}")
    else:
        print(
            f"Khong tim thay quy tac phu hop de suy dien tu {', '.join(facts)} sang {goal}"
        )
