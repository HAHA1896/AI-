"""
简单演示：开始学习按钮
直接创建一个窗口显示按钮
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

app = QApplication(sys.argv)

# 创建窗口
window = QWidget()
window.setWindowTitle('开始学习按钮演示')
window.resize(400, 300)

layout = QVBoxLayout(window)

# 添加标题
title = QLabel('单词学习')
title.setStyleSheet('font-size: 24px; font-weight: bold;')
layout.addWidget(title)

# 添加进度标签
progress = QLabel('剩余单词：3')
progress.setStyleSheet('font-size: 14px; color: gray;')
layout.addWidget(progress)

# 添加开始学习按钮
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

def on_click():
    print("按钮被点击了！")
    start_btn.hide()
    word_label.show()
    input_label.show()

start_btn.clicked.connect(on_click)
layout.addWidget(start_btn)

# 添加单词标签（初始隐藏）
word_label = QLabel('apple')
word_label.setStyleSheet('font-size: 36px; font-weight: bold;')
word_label.hide()
layout.addWidget(word_label)

# 添加输入提示（初始隐藏）
input_label = QLabel('请输入中文释义：')
input_label.setStyleSheet('font-size: 16px;')
input_label.hide()
layout.addWidget(input_label)

layout.addStretch()

window.show()

print("=" * 60)
print("演示窗口已显示")
print("=" * 60)
print("\n请查看窗口：")
print("1. 应该能看到绿色的'开始学习'按钮")
print("2. 点击按钮后，按钮会隐藏")
print("3. 然后显示单词内容")
print("\n如果看不到按钮，请告诉我具体看到了什么。")

sys.exit(app.exec())
