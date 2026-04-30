"""
完整测试开始学习按钮功能
"""

import sys
import os
import sqlite3
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.learning_widget import LearningWidget
from src.database.init import init_database
from src.database.connection import DatabaseConnection

print("=" * 60)
print("完整测试开始学习按钮")
print("=" * 60)

# 创建测试数据库
test_db_path = Path("test_button_db.sqlite")
if test_db_path.exists():
    test_db_path.unlink()

conn = sqlite3.connect(str(test_db_path))
init_database(conn)

# 插入测试单词
conn.execute('''
    INSERT INTO word_books (name, description) VALUES ('测试单词本', '测试用')
''')
word_book_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

# 插入单词
words = [
    ('apple', '苹果', '/ˈæpəl/'),
    ('banana', '香蕉', '/bəˈnænə/'),
    ('orange', '橙子', '/ˈɔːrɪndʒ/')
]

for word, definition, phonetic in words:
    cursor = conn.execute('''
        INSERT INTO words (word_book_id, word, definition, phonetic)
        VALUES (?, ?, ?, ?)
    ''', (word_book_id, word, definition, phonetic))
    word_id = cursor.lastrowid
    
    # 为每个单词创建学习进度记录（设置为待学习）
    conn.execute('''
        INSERT INTO learning_progress (word_id, review_count, next_review_at, is_mastered)
        VALUES (?, 0, datetime('now'), 0)
    ''', (word_id,))

conn.commit()

print(f"\n1. 测试数据已创建：{len(words)} 个单词（含学习进度）")

# 创建应用
app = QApplication(sys.argv)

try:
    # 创建学习组件
    widget = LearningWidget(word_book_id)
    print("\n2. LearningWidget 创建成功")
    
    # 检查按钮
    if hasattr(widget, 'start_learning_btn'):
        btn = widget.start_learning_btn
        print(f"\n3. 开始学习按钮状态：")
        print(f"   - 存在：✓")
        print(f"   - 文本：{btn.text()}")
        print(f"   - 可见：{btn.isVisible()}")
        print(f"   - 大小：{btn.size().width()} x {btn.size().height()}")
        
        # 检查单词列表
        print(f"\n4. 单词列表：")
        print(f"   - 单词数量：{len(widget.word_list)}")
        
        if len(widget.word_list) > 0:
            print(f"   - 第一个单词：{widget.word_list[0]['word']}")
            
            # 模拟点击按钮
            print(f"\n5. 模拟点击按钮...")
            widget.start_learning()
            
            print(f"   - 按钮可见性：{btn.isVisible()}")
            print(f"   - 单词卡片可见性：{widget.word_card.isVisible()}")
            print(f"   - 当前单词：{widget.word_label.text()}")
        else:
            print("   ⚠️ 没有待学习的单词")
    else:
        print("\n❌ start_learning_btn 不存在！")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    
    # 显示窗口
    widget.show()
    widget.resize(800, 600)
    print("\n窗口已显示，请检查界面...")
    
    # 清理
    # conn.close()
    # test_db_path.unlink()
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
