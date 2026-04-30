"""
查看测试数据库内容
用于快速验证生成的测试数据
"""

import sqlite3
from pathlib import Path

# 数据库路径
db_path = Path(__file__).parent / "test_data" / "wordstay_test.db"

if not db_path.exists():
    print(f"❌ 数据库文件不存在：{db_path}")
    print("请先运行：python generate_test_data.py")
    exit(1)

conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=" * 70)
print("WordStay 测试数据库内容查看器")
print("=" * 70)
print(f"\n数据库位置：{db_path}\n")

# 1. 查看单词本
print("-" * 70)
print("📚 单词本列表")
print("-" * 70)
cursor.execute('SELECT * FROM word_books')
word_books = cursor.fetchall()
for book in word_books:
    cursor.execute('SELECT COUNT(*) as count FROM words WHERE word_book_id = ?', (book['id'],))
    count = cursor.fetchone()['count']
    print(f"  ID: {book['id']} | 名称：{book['name']} | 单词数：{count}")
    print(f"     描述：{book['description']}")

# 2. 查看单词（每个单词本前 5 个）
print("\n" + "-" * 70)
print("📝 单词示例（每个单词本前 5 个）")
print("-" * 70)
for book in word_books:
    print(f"\n【{book['name']}】")
    cursor.execute('''
        SELECT word, phonetic, definition 
        FROM words 
        WHERE word_book_id = ? 
        LIMIT 5
    ''', (book['id'],))
    words = cursor.fetchall()
    for word in words:
        print(f"  • {word['word']} {word['phonetic']}")
        print(f"    释义：{word['definition']}")

# 3. 查看学习进度分布
print("\n" + "-" * 70)
print("📊 学习进度统计")
print("-" * 70)
cursor.execute('''
    SELECT 
        review_count,
        COUNT(*) as count,
        SUM(is_mastered) as mastered
    FROM learning_progress
    GROUP BY review_count
    ORDER BY review_count
''')
progress_stats = cursor.fetchall()
print("  复习次数分布：")
for stat in progress_stats:
    status = "✓已掌握" if stat['mastered'] > 0 else ""
    print(f"    复习{stat['review_count']}次：{stat['count']}个单词 {status}")

# 4. 查看待复习单词
print("\n" + "-" * 70)
print("⏰ 待复习单词（已过期）")
print("-" * 70)
from datetime import datetime
now = datetime.now()
cursor.execute('''
    SELECT w.word, w.definition, lp.review_count, lp.next_review_at
    FROM learning_progress lp
    JOIN words w ON lp.word_id = w.id
    WHERE lp.next_review_at < ? AND lp.is_mastered = 0
    ORDER BY lp.next_review_at ASC
    LIMIT 10
''', (now,))
due_words = cursor.fetchall()
if due_words:
    for i, word in enumerate(due_words, 1):
        try:
            next_review = datetime.fromisoformat(word['next_review_at']) if isinstance(word['next_review_at'], str) else word['next_review_at']
            overdue = now - next_review
            print(f"  {i}. {word['word']} - {word['definition']}")
            print(f"     复习{word['review_count']}次 | 已过期 {overdue.total_seconds()/60:.0f}分钟")
        except:
            print(f"  {i}. {word['word']} - {word['definition']}")
            print(f"     复习{word['review_count']}次")
else:
    print("  没有待复习的单词")

# 5. 查看错题
print("\n" + "-" * 70)
print("❌ 错题本（前 10 个）")
print("-" * 70)
cursor.execute('''
    SELECT w.word, w.definition, ww.wrong_count, ww.last_wrong_at
    FROM wrong_words ww
    JOIN words w ON ww.word_id = w.id
    ORDER BY ww.wrong_count DESC
    LIMIT 10
''')
wrong_words = cursor.fetchall()
if wrong_words:
    for i, word in enumerate(wrong_words, 1):
        print(f"  {i}. {word['word']} - {word['definition']}")
        print(f"     错误{word['wrong_count']}次")
else:
    print("  错题本为空")

# 6. 查看学习记录统计
print("\n" + "-" * 70)
print("📈 学习记录统计（过去 7 天）")
print("-" * 70)
cursor.execute('''
    SELECT 
        study_date,
        COUNT(*) as total,
        SUM(is_correct) as correct,
        COUNT(*) - SUM(is_correct) as wrong
    FROM study_records
    GROUP BY study_date
    ORDER BY study_date DESC
    LIMIT 7
''')
records = cursor.fetchall()
for record in records:
    accuracy = (record['correct'] / record['total'] * 100) if record['total'] > 0 else 0
    print(f"  {record['study_date']}: 学习{record['total']}次 | 正确{record['correct']} | 错误{record['wrong']} | 正确率{accuracy:.1f}%")

# 7. 查看系统设置
print("\n" + "-" * 70)
print("⚙️  系统设置")
print("-" * 70)
cursor.execute('SELECT * FROM settings')
settings = cursor.fetchall()
for setting in settings:
    print(f"  • {setting['key']}: {setting['value']}")

# 8. 总结
print("\n" + "=" * 70)
print("📊 数据总结")
print("=" * 70)
cursor.execute('SELECT COUNT(*) FROM word_books')
print(f"  单词本总数：{cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM words')
print(f"  单词总数：{cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM learning_progress')
print(f"  学习进度记录：{cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM wrong_words')
print(f"  错题数量：{cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM study_records')
print(f"  学习记录总数：{cursor.fetchone()[0]}")

print("\n" + "=" * 70)
print("✅ 测试数据查看完成！")
print("=" * 70)
print("\n提示：")
print("  • 运行 python main.py 启动应用")
print("  • 导入 test_data 目录中的 TXT 文件进行测试")
print("  • 查看 README.md 了解详细测试指南\n")

conn.close()
