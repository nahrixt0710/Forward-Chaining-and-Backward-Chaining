import json


def suy_dien_tien(facts, goal):
    inferred = set(facts)
    visited_rules = set()  # Lưu các luật đã áp dụng để tránh vòng lặp vô hạn
    steps = []  # Lưu các bước suy diễn
    while True:
        if goal in inferred:
            # steps.append(f"Muc tieu '{goal}' da dat duoc.")
            return steps
        is_used = False  # Kiểm tra xem có áp dụng luật nào không
        for rule in knowledge_base["rules"]:
            if all(condition in inferred for condition in rule["if"]):
                # if rule["then"] not in inferred:  # Tránh áp dụng lặp lại luật
                if rule["id"] not in visited_rules:
                    inferred.add(rule["then"])
                    steps.append(
                        f"{' ∧ '.join(rule['if'])} → {rule['then']} (theo {rule['id']}) {list(inferred)}"
                    )
                    visited_rules.add(rule["id"])
                    is_used = True
                    break  # Sau khi áp dụng luật, quay lại từ luật đầu tiên
        if is_used:  # Nếu đã áp dụng luật, quay lại xét từ đầu
            continue
        break  # Không có luật nào mới được áp dụng
    steps.clear()
    steps.append(
        f"Khong tim thay quy tac phu hop de suy dien tu {', '.join(facts)} sang {goal}"
    )
    return steps


# def select_rule(facts, rules):
#     """
#     Chọn quy tắc phù hợp nhất để áp dụng dựa trên tập facts hiện tại.
#     """
#     applicable_rules = []

#     for rule in rules:
#         # Kiểm tra nếu tất cả điều kiện của rule đều có trong facts
#         # if set(rule["if"]).issubset(facts):
#         applicable_rules.append(rule)

#     # Ưu tiên quy tắc có ít điều kiện hơn
#     applicable_rules.sort(key=lambda r: len(r["if"]))

#     return applicable_rules[0] if applicable_rules else None


def select_rule(facts, rules):
    """
    Chọn quy tắc phù hợp nhất dựa trên số điều kiện cần tìm (không thuộc facts).
    """
    applicable_rules = []

    for rule in rules:
        # Nếu quy tắc có ít nhất một điều kiện trong facts, coi là applicable
        if set(rule["if"]) & set(facts):
            applicable_rules.append(rule)

    # Sắp xếp theo số điều kiện cần tìm (ít điều kiện cần tìm nhất được ưu tiên)
    applicable_rules.sort(key=lambda r: len(set(r["if"]) - set(facts)))

    # Trả về quy tắc phù hợp nhất hoặc None nếu không có
    return applicable_rules[0] if applicable_rules else None


def suy_dien_lui(facts, goal):
    queue = [goal]
    checked_goals = set()
    inferred = set(facts)
    steps = []

    while queue:
        cur_goal = queue.pop(0)

        if cur_goal in checked_goals:
            continue

        if cur_goal in inferred:
            checked_goals.add(cur_goal)
            continue

        rule_list = []
        best_rule = {}
        for rule in knowledge_base["rules"]:
            if rule["then"] == cur_goal and rule["then"] not in checked_goals:
                rule_list.append(rule)
                best_rule = rule

        if len(rule_list) > 1:
            best_rule = select_rule(inferred, rule_list)

        if not best_rule:
            steps.clear()
            steps.append(
                f"Khong tim thay quy tac phu hop de suy dien tu {', '.join(facts)} sang {goal}"
            )
            break

        for condition in best_rule["if"]:
            if condition not in checked_goals and condition not in inferred:
                queue.append(condition)  # Thêm vào queue nếu chưa xử lý

        steps.append(
            f"{' ∧ '.join(best_rule['if'])} → {best_rule['then']} (theo {best_rule['id']})"
        )
        checked_goals.add(cur_goal)

    return steps


# Đọc cơ sở tri thức từ file JSON
with open("cstt2-gbaonr.json", "r") as file:
    knowledge_base = json.load(file)

# Hàm chính để nhập dữ liệu và chạy thuật toán
if __name__ == "__main__":
    # Nhập facts ban đầu
    facts = input("Nhap gia thiet (cach nhau boi dau phay): ").strip().split(",")
    facts = [fact.strip() for fact in facts]

    # Nhập goal
    goal = input("Nhap muc tieu can tim: ").strip()

    # Chạy suy diễn tiến
    print("\nSuy dien tien...")
    forward_steps = suy_dien_tien(facts, goal)
    for i, step in enumerate(forward_steps, 1):
        print(f"Step {i}: {step}")

    # Chạy suy diễn lùi
    print("\nSuy dien lui...")
    backward_steps = suy_dien_lui(facts, goal)
    backward_steps.reverse()
    for i, step in enumerate(backward_steps, 1):
        print(f"Step {i}: {step}")
