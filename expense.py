"""记账的核心逻辑（和界面分开，方便测试与复用）。

这个文件不负责"和用户聊天"，只负责"把一笔花费存起来、算统计"。
数据存在同目录 data/expenses.json 里。
"""

import json
import os
from datetime import date

# 数据文件的路径：和本文件在同一目录下的 data/expenses.json
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "expenses.json")


def load_expenses():
    """读取所有花费记录；文件不存在或为空就返回空列表。"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.strip():
        return []
    return json.loads(content)


def save_expenses(expenses):
    """把所有记录写回文件。"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)


def add_expense(amount, category, note="", when=None):
    """记一笔花费。

    amount: 金额（必须大于 0）
    category: 分类，如「餐饮」「交通」「学习」
    note: 备注，可空
    when: 日期，默认今天
    返回刚写入的这条记录。
    """
    if amount <= 0:
        raise ValueError("金额必须大于 0")
    expenses = load_expenses()
    item = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category,
        "note": note,
        "date": when or date.today().isoformat(),
    }
    expenses.append(item)
    save_expenses(expenses)
    return item


def list_expenses():
    """返回所有记录。"""
    return load_expenses()


def total_by_category():
    """按分类汇总总金额，例如 {'餐饮': 30, '交通': 5}。"""
    expenses = load_expenses()
    result = {}
    for e in expenses:
        result[e["category"]] = result.get(e["category"], 0) + e["amount"]
    return result


def delete_expense(item_id):
    """按编号删除一条记录，删除成功返回 True，没找到返回 False。"""
    expenses = load_expenses()
    new = [e for e in expenses if e["id"] != item_id]
    if len(new) == len(expenses):
        return False
    save_expenses(new)
    return True
