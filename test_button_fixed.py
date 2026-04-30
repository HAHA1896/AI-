"""
完整测试开始学习按钮功能 - 修正版
"""

import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.learning_widget import LearningWidget
from src.database.init import init_database
from src.database.crud import WordBookCRUD, WordCRUD, LearningProgressCRUD

print("=" * 60)
print("完整测试开始学习按钮 - 修正版")
print("=" * 60)

# 创建测试数据库
test_db_path = Path("test_button_db.sqlite")
if test_db_path.exists():
    test_db_path.unlink()

conn = sqlite3.connect(str(test_db_path))
conn.row_factory = sqlite3.Row
init_database(conn)

# 插入测试单词本
word_book_id = WordBookCRUD.create(conn, '测试单词本', '测试用')
print(f"\n1. 单词本已创建，ID: {word_book_id}")

# 插入单词
words = [
    ('apple', '苹果', '/ˈæpəl/'),
    ('banana', '香蕉', '/bəˈnænə/'),
    ('orange', '橙子', '/ˈɔːrɪndʒ/')
]

word_ids = []
for word, definition, phonetic in words:
    word_id = WordCRUD.create(conn, word_book_id, word, definition=definition, phonetic=phonetic)
    word_ids.append(word_id)
    
    # 为每个单词创建学习进度记录
    # 设置 next_review_at 为当前时间，使其可以被获取
    LearningProgressCRUD.create_or_update(
        conn,
        word_id=word_id,
        review_count=0,
        next_review_at=datetime.now()  # 设置为当前时间
    )

conn.commit()
print(f"2. 测试数据已创建：{len(words)} 个单词（含学习进度）")

# 检查学习进度
cursor = conn.cursor()
cursor.execute('SELECT * FROM learning_progress')
progress_rows = cursor.fetchall()
print(f"3. 学习进度记录：{len(progress_rows)} 条")
for row in progress_rows:
    print(f"   - word_id: {row['word_id']}, next_review_at: {row['next_review_at']}, is_mastered: {row['is_mastered']}")

# 检查待复习单词
due_words = LearningProgressCRUD.get_due_words(conn, word_book_id)
print(f"4. 待复习单词：{len(due_words)} 个")

# 创建应用
app = QApplication(sys.argv)

try:
    # 创建学习组件
    widget = LearningWidget(word_book_id)
    print(f"\n5. LearningWidget 创建成功")
    
    # 检查按钮
    if hasattr(widget, 'start_learning_btn'):
        btn = widget.start_learning_btn
        print(f"\n6. 开始学习按钮状态：")
        print(f"   - 存在：✓")
        print(f"   - 文本：{btn.text()}")
        print(f"   - 可见：{btn.isVisible()}")
        
        # 检查单词列表
        print(f"\n7. 单词列表：")
        print(f"   - 单词数量：{len(widget.word_list)}")
        
        if len(widget.word_list) > 0:
            print(f"   - 第一个单词：{widget.word_list[0]['word']}")
            
            # 模拟点击按钮
            print(f"\n8. 模拟点击按钮...")
            widget.start_learning()
            
            print(f"   - 按钮可见性：{btn.isVisible()}")
            print(f"   - 单词卡片可见性：{widget.word_card.isVisible()}")
            print(f"   - 当前单词：{widget.word_label.text()}")
            
            print("\n" + "=" * 60)
            print("✅ 测试成功！按钮功能正常")
            print("=" * 60)
        else:
            print("   ⚠️ 没有待学习的单词")
            print("\n" + "=" * 60)
            print("❌ 测试失败：单词列表为空")
            print("=" * 60)
            sys.exit(1)
    else:
        print("\n❌ start_learning_btn 不存在！")
        sys.exit(1)
    
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
