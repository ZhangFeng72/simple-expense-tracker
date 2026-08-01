"""程序入口：负责菜单和用户输入。

运行方式：在终端进入本文件夹，输入  python main.py
"""

from expense import (
    add_expense,
    list_expenses,
    total_by_category,
    delete_expense,
    monthly_summary,
)


def show_menu():
    print("\n==== 极简记账工具 ====")
    print("1. 记一笔")
    print("2. 查看所有")
    print("3. 按分类统计")
    print("4. 删除一笔")
    print("5. 查看某月统计")
    print("6. 退出")


def main():
    while True:
        show_menu()
        choice = input("请选择(1-6): ").strip()

        if choice == "1":
            try:
                amount = float(input("金额: "))
                category = input("分类(如 餐饮/交通/学习): ").strip()
                note = input("备注(可空): ").strip()
                when = input("日期(默认今天，格式2026-08-01): ").strip()
                item = add_expense(amount, category, note, when or None)
                print(f"已记录: #{item['id']} {item['date']} {item['category']} "
                      f"{item['amount']}元 {item['note']}")
            except ValueError as err:
                print("输入有误:", err)

        elif choice == "2":
            records = list_expenses()
            if not records:
                print("(还没有记录)")
            for e in records:
                print(f"#{e['id']} {e['date']} {e['category']} "
                      f"{e['amount']}元 {e['note']}")

        elif choice == "3":
            totals = total_by_category()
            if not totals:
                print("(还没有记录)")
            for cat, total in totals.items():
                print(f"{cat}: {total}元")

        elif choice == "4":
            try:
                item_id = int(input("要删除的编号: "))
                ok = delete_expense(item_id)
                print("已删除" if ok else "没找到该编号")
            except ValueError:
                print("请输入数字编号")

        elif choice == "5":
            month = input("看哪个月(格式 2026-08): ").strip()
            s = monthly_summary(month)
            if s["count"] == 0:
                print(f"( {month} 还没有记录 )")
            else:
                print(f"\n--- {month} 统计 ---")
                for cat, t in s["by_category"].items():
                    print(f"{cat}: {t}元")
                print(f"共 {s['count']} 笔，合计 {s['total']}元")

        elif choice == "6":
            print("再见")
            break

        else:
            print("请输入 1-6")


if __name__ == "__main__":
    main()
