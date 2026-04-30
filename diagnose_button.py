"""
诊断开始学习按钮问题
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("诊断开始学习按钮问题")
print("=" * 70)

# 1. 检查代码文件
print("\n【步骤 1】检查代码文件...")
learning_widget_path = "src/ui/learning_widget.py"

if os.path.exists(learning_widget_path):
    with open(learning_widget_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查关键代码
    checks = {
        'create_start_learning_button': '创建按钮方法',
        'start_learning_btn': '按钮属性',
        'def start_learning': '开始学习方法',
        '开始学习': '按钮文本'
    }
    
    print(f"   文件存在：✓")
    for key, desc in checks.items():
        if key in content:
            print(f"   {desc}：✓")
        else:
            print(f"   {desc}：✗ 缺失！")
else:
    print(f"   文件不存在：✗")
    sys.exit(1)

# 2. 检查按钮在 init_ui 中的使用
print("\n【步骤 2】检查按钮在 init_ui 中的使用...")
if 'self.start_learning_btn = self.create_start_learning_button()' in content:
    print("   按钮创建：✓")
else:
    print("   按钮创建：✗ 未找到")

if 'layout.addWidget(self.start_learning_btn)' in content:
    print("   按钮添加到布局：✓")
else:
    print("   按钮添加到布局：✗ 未找到")

# 3. 检查按钮显示逻辑
print("\n【步骤 3】检查按钮显示逻辑...")
if 'self.start_learning_btn.show()' in content:
    print("   显示按钮：✓")
else:
    print("   显示按钮：✗ 未找到")

if 'self.start_learning_btn.hide()' in content:
    print("   隐藏按钮：✓")
else:
    print("   隐藏按钮：✗ 未找到")

# 4. 创建简单的测试窗口
print("\n【步骤 4】创建测试窗口...")
try:
    from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
    
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = QWidget()
    window.setWindowTitle('开始学习按钮测试')
    window.resize(500, 300)
    
    layout = QVBoxLayout(window)
    
    # 标题
    title = QLabel('单词学习')
    title.setStyleSheet('font-size: 24px; font-weight: bold;')
    layout.addWidget(title)
    
    # 进度
    progress = QLabel('剩余单词：3')
    progress.setStyleSheet('font-size: 14px; color: gray;')
    layout.addWidget(progress)
    
    # 开始学习按钮
    start_btn = QPushButton('开始学习')
    start_btn.setStyleSheet('''
        QPushButton {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #219a52;
        }
    ''')
    
    click_count = [0]
    def on_click():
        click_count[0] += 1
        print(f"\n✓ 按钮被点击了！次数：{click_count[0]}")
        start_btn.setText(f'已点击 {click_count[0]} 次')
    
    start_btn.clicked.connect(on_click)
    layout.addWidget(start_btn)
    
    layout.addStretch()
    
    window.show()
    
    print("\n" + "=" * 70)
    print("✅ 诊断完成")
    print("=" * 70)
    print("\n测试窗口已显示，请检查：")
    print("1. 是否能看到绿色的'开始学习'按钮？")
    print("2. 点击按钮是否有效？")
    print("\n如果看不到按钮，可能的原因：")
    print("- Python 缓存问题（删除 __pycache__ 目录后重试）")
    print("- 运行的是旧版本代码（重启应用）")
    print("- 数据库中没有待学习的单词")
    
    sys.exit(app.exec())
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
