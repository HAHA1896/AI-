"""
测试 UI 组件初始化
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_settings_manager():
    """测试 SettingsManager 可以正常初始化"""
    print("测试 SettingsManager...")
    from src.settings import SettingsManager
    
    settings = SettingsManager()
    
    # 验证所有属性都存在
    assert hasattr(settings, 'enable_floating_window')
    assert hasattr(settings, 'floating_window_interval')
    assert settings.enable_floating_window == False
    assert settings.floating_window_interval == 10
    
    print("✓ SettingsManager 初始化成功，悬浮窗属性正常")
    return True

def test_main_window_import():
    """测试 MainWindow 可以正常导入"""
    print("测试 MainWindow 导入...")
    from src.ui.main_window import MainWindow
    
    print("✓ MainWindow 导入成功")
    return True

def test_learning_widget_import():
    """测试 LearningWidget 可以正常导入"""
    print("测试 LearningWidget 导入...")
    from src.ui.learning_widget import LearningWidget
    
    print("✓ LearningWidget 导入成功")
    return True

def test_floating_window_import():
    """测试 FloatingWindow 可以正常导入"""
    print("测试 FloatingWindow 导入...")
    from src.ui.floating_window import FloatingWindow
    
    print("✓ FloatingWindow 导入成功")
    return True

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("UI 组件导入测试")
    print("=" * 60 + "\n")
    
    tests = [
        test_settings_manager,
        test_main_window_import,
        test_learning_widget_import,
        test_floating_window_import
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} 失败：{e}\n")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("=" * 60)
    
    sys.exit(0 if passed == len(tests) else 1)
