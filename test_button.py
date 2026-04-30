"""
测试开始学习按钮是否真的存在
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.learning_widget import LearningWidget

print("=" * 60)
print("测试开始学习按钮")
print("=" * 60)

app = QApplication(sys.argv)

try:
    # 创建学习组件
    widget = LearningWidget()
    print("\n1. LearningWidget 创建成功")
    
    # 检查是否有 start_learning_btn 属性
    if hasattr(widget, 'start_learning_btn'):
        print("2. ✓ start_learning_btn 属性存在")
        btn = widget.start_learning_btn
        print(f"   - 按钮文本: {btn.text()}")
        print(f"   - 按钮是否可见: {btn.isVisible()}")
        print(f"   - 按钮大小: {btn.size().width()} x {btn.size().height()}")
    else:
        print("2. ✗ start_learning_btn 属性不存在！")
        sys.exit(1)
    
    # 检查其他组件
    print("\n3. 检查其他组件:")
    components = {
        'word_card': '单词卡片',
        'input_area': '输入区域',
        'feedback_area': '反馈区域',
        'action_area': '操作区域'
    }
    
    for attr, name in components.items():
        if hasattr(widget, attr):
            comp = getattr(widget, attr)
            visible = comp.isVisible()
            print(f"   - {name}: 存在, 可见={visible}")
        else:
            print(f"   - {name}: 不存在")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    
    # 显示窗口
    widget.show()
    widget.resize(800, 600)
    print("\n窗口已显示，请检查界面...")
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
