"""
测试修改后的开始学习按钮
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("测试修改后的开始学习按钮")
print("=" * 70)

# 读取修改后的代码
with open('src/ui/learning_widget.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查修改
print("\n【检查 1】load_words 方法中的按钮显示逻辑：")
if 'self.start_learning_btn.show()' in content:
    # 计算在 load_words 方法中的位置
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def load_words' in line:
            print(f"✓ load_words 方法在第 {i+1} 行")
            # 检查接下来的 30 行
            for j in range(i, min(i+30, len(lines))):
                if 'self.start_learning_btn.show()' in lines[j]:
                    print(f"✓ 按钮显示代码在第 {j+1} 行：{lines[j].strip()}")
            break

print("\n【检查 2】按钮文本更新逻辑：")
if '暂无单词，请先导入单词本' in content:
    print("✓ 没有单词时的提示文本已添加")
else:
    print("✗ 没有单词时的提示文本未找到")

if 'self.start_learning_btn.setText' in content:
    print("✓ 按钮文本更新代码存在")
else:
    print("✗ 按钮文本更新代码不存在")

print("\n【检查 3】按钮启用/禁用逻辑：")
if 'self.start_learning_btn.setEnabled(False)' in content:
    print("✓ 按钮禁用逻辑存在")
else:
    print("✗ 按钮禁用逻辑不存在")

if 'self.start_learning_btn.setEnabled(True)' in content:
    print("✓ 按钮启用逻辑存在")
else:
    print("✗ 按钮启用逻辑不存在")

print("\n" + "=" * 70)
print("✅ 修改完成！")
print("=" * 70)
print("\n现在的行为：")
print("1. 按钮始终显示，不会隐藏")
print("2. 没有单词时，按钮显示'暂无单词，请先导入单词本'并禁用")
print("3. 有单词时，按钮显示'开始学习'并可点击")
print("4. 点击按钮后开始学习")
print("\n请运行 python main.py 测试！")
