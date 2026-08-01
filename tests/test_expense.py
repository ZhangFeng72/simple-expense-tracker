"""自动测试：保证核心逻辑没写错。

运行方式：python -m unittest tests/test_expense.py
"""

import os
import tempfile
import unittest

import expense


class TestExpense(unittest.TestCase):
    def setUp(self):
        # 用临时文件代替真实数据，测试完自动清理，不污染你的记录
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        expense.DATA_FILE = self.tmp.name

    def tearDown(self):
        os.remove(self.tmp.name)

    def test_add_and_list(self):
        item = expense.add_expense(10.5, "餐饮", "午饭")
        self.assertEqual(item["amount"], 10.5)
        self.assertEqual(len(expense.list_expenses()), 1)

    def test_amount_must_be_positive(self):
        with self.assertRaises(ValueError):
            expense.add_expense(-5, "餐饮")

    def test_total_by_category(self):
        expense.add_expense(10, "餐饮")
        expense.add_expense(20, "餐饮")
        expense.add_expense(5, "交通")
        self.assertEqual(expense.total_by_category()["餐饮"], 30)

    def test_monthly_summary(self):
        # 用 when 参数造不同日期的数据来测
        expense.add_expense(10, "餐饮", when="2026-08-01")
        expense.add_expense(20, "餐饮", when="2026-08-15")
        expense.add_expense(5, "交通", when="2026-08-20")
        expense.add_expense(99, "学习", when="2026-07-30")  # 7月，不算进8月
        s = expense.monthly_summary("2026-08")
        self.assertEqual(s["count"], 3)
        self.assertEqual(s["total"], 35)
        self.assertEqual(s["by_category"]["餐饮"], 30)
        self.assertNotIn("学习", s["by_category"])


if __name__ == "__main__":
    unittest.main()
