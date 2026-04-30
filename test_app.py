"""
WordStay 应用程序测试脚本
测试核心功能模块
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database():
    """测试数据库模块"""
    print("=" * 60)
    print("测试数据库模块...")
    print("=" * 60)
    
    from src.database import get_db, WordBookCRUD, WordCRUD, LearningProgressCRUD
    from src.database.init import init_database
    from src.database.connection import DatabaseConnection
    
    # 初始化数据库
    conn = get_db()
    DatabaseConnection._instance = None  # 重置单例以重新初始化
    conn = get_db()
    init_database(conn)
    
    # 测试创建单词本
    book_id = WordBookCRUD.create(conn, "测试单词本", "用于测试的单词本")
    print(f"✓ 创建单词本成功，ID: {book_id}")
    
    # 测试添加单词
    word_id = WordCRUD.create(conn, book_id, "hello", "你好", "Hello, world!")
    print(f"✓ 添加单词成功，ID: {word_id}")
    
    # 测试获取单词
    word = WordCRUD.get_by_id(conn, word_id)
    assert word['word'] == "hello"
    assert word['definition'] == "你好"
    print(f"✓ 获取单词成功：{word['word']} - {word['definition']}")
    
    # 测试创建学习进度
    LearningProgressCRUD.create_or_update(conn, word_id, book_id)
    print(f"✓ 创建学习进度成功")
    
    # 测试获取待复习单词
    due_words = LearningProgressCRUD.get_due_words(conn, book_id)
    print(f"✓ 获取待复习单词成功，数量：{len(due_words)}")
    
    print("\n✓ 数据库模块测试通过！\n")
    return True

def test_importer():
    """测试 TXT 导入模块"""
    print("=" * 60)
    print("测试 TXT 导入模块...")
    print("=" * 60)
    
    from src.importer import TxtParser, WordBookImporter
    
    # 创建测试 TXT 文件
    test_content = """apple 苹果
banana 香蕉
orange - 橙子
grape 葡萄
invalid_line
pear 梨"""
    
    test_file = "test_vocab.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    # 测试解析
    parser = TxtParser()
    result = parser.parse(test_file)
    
    print(f"✓ 解析成功，单词数：{len(result.words)}")
    print(f"✓ 异常行数：{len(result.error_lines)}")
    
    # 验证解析结果
    assert len(result.words) == 5, f"期望 5 个单词，实际{len(result.words)}个"
    assert len(result.error_lines) == 1, f"期望 1 个异常行，实际{len(result.error_lines)}个"
    
    # 清理测试文件
    os.remove(test_file)
    
    print("\n✓ TXT 导入模块测试通过！\n")
    return True

def test_algorithm():
    """测试记忆算法模块"""
    print("=" * 60)
    print("测试记忆算法模块...")
    print("=" * 60)
    
    from src.algorithm import EbbinghausMemoryCurve, WordScheduler
    
    # 测试复习间隔
    intervals = [
        (0, "首次记忆"),
        (1, "10 分钟后"),
        (2, "1 小时后"),
        (3, "1 天后"),
        (4, "3 天后"),
        (5, "7 天后")
    ]
    
    for review_count, expected in intervals:
        next_time = EbbinghausMemoryCurve.get_next_review_time(review_count)
        print(f"✓ 复习{review_count}次后，下次复习时间：{next_time}")
    
    # 测试进度计算
    progress = EbbinghausMemoryCurve.calculate_progress(5)
    assert progress == 1.0, "完成 5 次复习后进度应为 100%"
    print(f"✓ 进度计算正确：{progress * 100}%")
    
    print("\n✓ 记忆算法模块测试通过！\n")
    return True

def test_settings():
    """测试设置模块"""
    print("=" * 60)
    print("测试设置模块...")
    print("=" * 60)
    
    from src.settings import SettingsManager
    
    settings = SettingsManager()
    
    # 测试默认值
    assert settings.enable_floating_window == False
    assert settings.floating_window_interval == 10
    print(f"✓ 悬浮窗默认设置：启用={settings.enable_floating_window}, 间隔={settings.floating_window_interval}秒")
    
    # 测试设置
    settings.enable_floating_window = True
    settings.floating_window_interval = 15
    assert settings.enable_floating_window == True
    assert settings.floating_window_interval == 15
    print(f"✓ 设置修改成功：启用={settings.enable_floating_window}, 间隔={settings.floating_window_interval}秒")
    
    print("\n✓ 设置模块测试通过！\n")
    return True

def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("WordStay 应用程序功能测试")
    print("=" * 60 + "\n")
    
    tests = [
        ("数据库模块", test_database),
        ("TXT 导入模块", test_importer),
        ("记忆算法模块", test_algorithm),
        ("设置模块", test_settings)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n✗ {test_name}测试失败：{e}\n")
            failed += 1
    
    print("=" * 60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("=" * 60)
    
    return failed == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
