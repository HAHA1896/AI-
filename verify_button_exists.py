"""
完整验证开始学习按钮
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("完整验证开始学习按钮")
print("=" * 70)

# 读取代码文件
with open('src/ui/learning_widget.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找关键代码
print("\n【检查 1】按钮创建代码：")
if 'self.start_learning_btn = self.create_start_learning_button()' in content:
    print("✓ 按钮创建代码存在")
else:
    print("✗ 按钮创建代码不存在")

print("\n【检查 2】按钮添加到布局代码：")
if 'layout.addWidget(self.start_learning_btn)' in content:
    print("✓ 按钮添加到布局代码存在")
else:
    print("✗ 按钮添加到布局代码不存在")

print("\n【检查 3】按钮显示/隐藏逻辑：")
show_count = content.count('self.start_learning_btn.show()')
hide_count = content.count('self.start_learning_btn.hide()')
print(f"  show() 调用次数：{show_count}")
print(f"  hide() 调用次数：{hide_count}")

print("\n【检查 4】按钮点击事件：")
if 'btn.clicked.connect(self.start_learning)' in content:
    print("✓ 按钮点击事件绑定存在")
else:
    print("✗ 按钮点击事件绑定不存在")

print("\n" + "=" * 70)
print("结论：")
if 'self.start_learning_btn = self.create_start_learning_button()' in content and \
   'layout.addWidget(self.start_learning_btn)' in content:
    print("✅ 代码中确实包含开始学习按钮")
    print("\n如果按钮没有显示，可能的原因：")
    print("1. 数据库中没有待学习的单词（load_words 返回空列表）")
    print("2. Python 缓存问题（删除 __pycache__ 目录）")
    print("3. 运行的是旧版本代码（重启应用）")
    print("4. 按钮被隐藏了（检查 load_words 方法）")
else:
    print("✗ 代码中缺少开始学习按钮")

print("=" * 70)
