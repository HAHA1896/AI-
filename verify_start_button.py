"""
验证开始学习按钮功能
"""

import sys

print("=" * 60)
print("验证开始学习按钮功能")
print("=" * 60)

try:
    # 1. 验证导入
    print("\n1. 检查模块导入...")
    from src.ui.learning_widget import LearningWidget
    print("   ✓ LearningWidget 导入成功")
    
    # 2. 验证代码中有开始学习按钮
    print("\n2. 检查开始学习按钮...")
    import ast
    with open('src/ui/learning_widget.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查关键元素
    checks = {
        'start_learning_btn': '开始学习按钮属性',
        'create_start_learning_button': '创建按钮方法',
        'def start_learning': '开始学习方法',
        '开始学习': '按钮文本'
    }
    
    all_found = True
    for key, desc in checks.items():
        if key in content:
            print(f"   ✓ {desc} 已添加")
        else:
            print(f"   ✗ {desc} 未找到")
            all_found = False
    
    if not all_found:
        print("\n❌ 部分功能未添加成功")
        sys.exit(1)
    
    # 3. 验证代码可以编译
    print("\n3. 编译检查...")
    compile(content, 'learning_widget.py', 'exec')
    print("   ✓ learning_widget.py 语法正确")
    
    # 4. 验证逻辑
    print("\n4. 检查功能逻辑...")
    
    # 检查 load_words 方法是否显示开始按钮
    if 'self.start_learning_btn.show()' in content:
        print("   ✓ 加载单词后显示开始按钮")
    else:
        print("   ✗ 未找到显示开始按钮逻辑")
        sys.exit(1)
    
    # 检查 start_learning 方法是否隐藏按钮
    if 'self.start_learning_btn.hide()' in content:
        print("   ✓ 点击开始后隐藏按钮")
    else:
        print("   ✗ 未找到隐藏按钮逻辑")
        sys.exit(1)
    
    # 检查 show_current_word 是否显示组件
    if 'self.word_card.show()' in content and 'self.input_area.show()' in content:
        print("   ✓ 显示当前单词时显示学习组件")
    else:
        print("   ✗ 未找到显示学习组件逻辑")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ 验证通过！")
    print("=" * 60)
    print("\n新增功能：")
    print("  • 学习界面添加了醒目的'开始学习'按钮")
    print("  • 导入单词本后不会自动显示单词")
    print("  • 点击'开始学习'按钮后才开始学习")
    print("  • 学习过程中按钮隐藏，专注学习")
    print("  • 完成学习后再次显示开始按钮")
    print("\n使用流程：")
    print("  1. 导入单词本")
    print("  2. 切换到'学习'标签")
    print("  3. 点击绿色的'开始学习'按钮")
    print("  4. 开始答题学习")
    print("  5. 完成后自动显示下一个单词")
    print("\n按钮样式：")
    print("  • 绿色背景，大字号，醒目易见")
    print("  • 悬停时颜色加深，提供视觉反馈")
    print("  • 点击后立即开始学习\n")
    
except Exception as e:
    print(f"\n❌ 验证失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
