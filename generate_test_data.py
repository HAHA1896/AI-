"""
生成 WordStay 应用程序的测试数据
包括测试单词本、单词、学习进度等
"""

import sqlite3
import os
from datetime import datetime, timedelta
from pathlib import Path

# 创建测试数据目录
test_data_dir = Path(__file__).parent / "test_data"
test_data_dir.mkdir(exist_ok=True)


def create_test_txt_files():
    """创建测试用的 TXT 单词本文件"""
    print("=" * 60)
    print("创建测试 TXT 单词本文件...")
    print("=" * 60)
    
    # 测试文件 1：标准格式（空格分隔）
    test_file_1 = test_data_dir / "test_vocab_standard.txt"
    content_1 = """apple 苹果
banana 香蕉
orange 橙子
grape 葡萄
pear 梨
peach 桃子
watermelon 西瓜
strawberry 草莓
pineapple 菠萝
mango 芒果"""
    
    with open(test_file_1, 'w', encoding='utf-8') as f:
        f.write(content_1)
    print(f"✓ 创建标准格式单词本：{test_file_1.name} (10 个单词)")
    
    # 测试文件 2：连字符格式
    test_file_2 = test_data_dir / "testvocab_hyphen.txt"
    content_2 = """computer - 计算机
keyboard - 键盘
mouse - 鼠标
monitor - 显示器
laptop - 笔记本电脑
tablet - 平板电脑
printer - 打印机
scanner - 扫描仪
camera - 相机
phone - 电话"""
    
    with open(test_file_2, 'w', encoding='utf-8') as f:
        f.write(content_2)
    print(f"✓ 创建连字符格式单词本：{test_file_2.name} (10 个单词)")
    
    # 测试文件 3：混合格式（包含异常行）
    test_file_3 = test_data_dir / "test_vocab_mixed.txt"
    content_3 = """hello 你好
world 世界
python 蟒蛇
programming 编程
language 语言
invalid_line_without_definition
code 代码
debug 调试
error 错误
another_invalid
function 函数
variable 变量"""
    
    with open(test_file_3, 'w', encoding='utf-8') as f:
        f.write(content_3)
    print(f"✓ 创建混合格式单词本：{test_file_3.name} (10 个有效单词，2 个异常行)")
    
    # 测试文件 4：常用英语词汇（CET-4 级别）
    test_file_4 = test_data_dir / "test_vocab_cet4.txt"
    content_4 = """ability 能力
abroad 国外
absolute 绝对的
academic 学术的
access 访问
accomplish 完成
accurate 准确的
achieve 实现
acquire 获得
adapt 适应
adequate 足够的
adjust 调整
admire 钦佩
admit 承认
adopt 采用
advance 前进
adventure 冒险
advocate 提倡
afford 负担得起
agency 代理"""
    
    with open(test_file_4, 'w', encoding='utf-8') as f:
        f.write(content_4)
    print(f"✓ 创建 CET-4 单词本：{test_file_4.name} (20 个单词)")
    
    # 测试文件 5：重复单词测试
    test_file_5 = test_data_dir / "test_vocab_duplicates.txt"
    content_5 = """test 测试
test 测试（重复）
demo 演示
demo 演示（重复）
sample 样本
sample 样本（重复）
example 例子
unique 唯一的
special 特别的"""
    
    with open(test_file_5, 'w', encoding='utf-8') as f:
        f.write(content_5)
    print(f"✓ 创建重复单词测试本：{test_file_5.name} (9 行，含重复)")
    
    print(f"\n✓ 共创建 5 个测试 TXT 文件，位于：{test_data_dir}\n")
    return [test_file_1, test_file_2, test_file_3, test_file_4, test_file_5]


def create_test_database():
    """创建包含测试数据的数据库"""
    print("=" * 60)
    print("创建测试数据库...")
    print("=" * 60)
    
    # 获取数据库路径（使用项目目录，避免 sandbox 权限问题）
    db_path = Path(__file__).parent / "test_data" / "wordstay_test.db"
    db_path.parent.mkdir(exist_ok=True)
    
    # 删除旧数据库（如果存在）
    if db_path.exists():
        db_path.unlink()
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 创建表结构
    print("创建数据库表结构...")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_book_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            phonetic TEXT,
            definition TEXT,
            example TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (word_book_id) REFERENCES word_books (id) ON DELETE CASCADE,
            UNIQUE(word_book_id, word)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL UNIQUE,
            review_count INTEGER DEFAULT 0,
            correct_count INTEGER DEFAULT 0,
            wrong_count INTEGER DEFAULT 0,
            last_reviewed_at TIMESTAMP,
            next_review_at TIMESTAMP,
            ease_factor REAL DEFAULT 2.5,
            interval INTEGER DEFAULT 0,
            is_mastered INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (word_id) REFERENCES words (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wrong_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL UNIQUE,
            wrong_count INTEGER DEFAULT 0,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_wrong_at TIMESTAMP,
            FOREIGN KEY (word_id) REFERENCES words (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,
            study_date DATE NOT NULL,
            reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_correct INTEGER DEFAULT 0,
            FOREIGN KEY (word_id) REFERENCES words (id) ON DELETE CASCADE
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_words_word_book_id ON words (word_book_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_learning_progress_next_review ON learning_progress (next_review_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_wrong_words_word_id ON wrong_words (word_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_study_records_word_id ON study_records (word_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_study_records_study_date ON study_records (study_date)')
    
    conn.commit()
    print("✓ 数据库表结构创建完成\n")
    
    # 插入测试数据 - 单词本
    print("插入测试单词本...")
    test_word_books = [
        ('测试单词本 1', '用于功能测试的第一个单词本'),
        ('测试单词本 2', '用于功能测试的第二个单词本'),
        ('CET-4 核心词汇', '大学英语四级核心词汇'),
        ('计算机专业词汇', '计算机科学相关专业术语'),
    ]
    
    for name, desc in test_word_books:
        cursor.execute('''
            INSERT INTO word_books (name, description) VALUES (?, ?)
        ''', (name, desc))
    
    conn.commit()
    print(f"✓ 插入 {len(test_word_books)} 个测试单词本\n")
    
    # 插入测试数据 - 单词
    print("插入测试单词...")
    test_words = {
        1: [  # 测试单词本 1
            ('apple', '/ˈæpəl/', '苹果', 'I eat an apple every day.'),
            ('banana', '/bəˈnænə/', '香蕉', 'Monkeys love bananas.'),
            ('orange', '/ˈɔːrɪndʒ/', '橙子', 'This orange is very sweet.'),
            ('grape', '/ɡreɪp/', '葡萄', 'We make wine from grapes.'),
            ('pear', '/per/', '梨', 'The pear is juicy.'),
        ],
        2: [  # 测试单词本 2
            ('computer', '/kəmˈpjuːtər/', '计算机', 'I use a computer for work.'),
            ('keyboard', '/ˈkiːbɔːrd/', '键盘', 'This keyboard is wireless.'),
            ('mouse', '/maʊs/', '鼠标', 'The mouse has two buttons.'),
            ('monitor', '/ˈmɑːnɪtər/', '显示器', 'The monitor is 27 inches.'),
            ('laptop', '/ˈlæptɑːp/', '笔记本电脑', 'My laptop is very light.'),
        ],
        3: [  # CET-4 核心词汇
            ('ability', '/əˈbɪləti/', '能力', 'He has the ability to do the job.'),
            ('abroad', '/əˈbrɔːd/', '国外', 'She studies abroad.'),
            ('absolute', '/ˈæbsəluːt/', '绝对的', 'I have absolute confidence in you.'),
            ('academic', '/ˌækəˈdemɪk/', '学术的', 'This is an academic question.'),
            ('access', '/ˈækses/', '访问', 'You need a password to access the system.'),
            ('accomplish', '/əˈkɑːmplɪʃ/', '完成', 'We accomplished the task on time.'),
            ('accurate', '/ˈækjərət/', '准确的', 'The information is accurate.'),
            ('achieve', '/əˈtʃiːv/', '实现', 'He achieved his goal.'),
            ('acquire', '/əˈkwaɪər/', '获得', 'She acquired a lot of knowledge.'),
            ('adapt', '/əˈdæpt/', '适应', 'It took him a while to adapt to the new environment.'),
        ],
        4: [  # 计算机专业词汇
            ('algorithm', '/ˈælɡərɪðəm/', '算法', 'This algorithm is very efficient.'),
            ('database', '/ˈdeɪtəbeɪs/', '数据库', 'The database contains millions of records.'),
            ('network', '/ˈnetwɜːrk/', '网络', 'The network is down.'),
            ('protocol', '/ˈproʊtəkɔːl/', '协议', 'HTTP is a network protocol.'),
            ('interface', '/ˈɪntərfeɪs/', '接口', 'The user interface is friendly.'),
            ('variable', '/ˈveriəbl/', '变量', 'Declare a variable first.'),
            ('function', '/ˈfʌŋkʃn/', '函数', 'This function returns a value.'),
            ('object', '/ˈɑːbdʒekt/', '对象', 'Everything is an object in Python.'),
            ('class', '/klæs/', '类', 'Define a class to encapsulate data.'),
            ('method', '/ˈmeθəd/', '方法', 'Call a method on the object.'),
        ],
    }
    
    total_words = 0
    for book_id, words in test_words.items():
        for word_data in words:
            cursor.execute('''
                INSERT INTO words (word_book_id, word, phonetic, definition, example)
                VALUES (?, ?, ?, ?, ?)
            ''', (book_id, *word_data))
            total_words += 1
    
    conn.commit()
    print(f"✓ 插入 {total_words} 个测试单词\n")
    
    # 插入测试数据 - 学习进度
    print("插入测试学习进度...")
    
    # 获取所有单词 ID
    cursor.execute('SELECT id FROM words')
    word_ids = [row['id'] for row in cursor.fetchall()]
    
    now = datetime.now()
    
    # 为部分单词创建学习进度
    for i, word_id in enumerate(word_ids[:30]):  # 前 30 个单词有学习进度
        review_count = i % 6  # 0-5 次复习
        correct_count = max(0, review_count - (i % 3))
        wrong_count = i % 3
        
        # 根据复习次数计算下次复习时间
        if review_count == 0:
            next_review = now  # 立即复习
        elif review_count == 1:
            next_review = now - timedelta(minutes=5)  # 已过期 5 分钟
        elif review_count == 2:
            next_review = now - timedelta(hours=1)  # 已过期 1 小时
        elif review_count == 3:
            next_review = now + timedelta(days=1)  # 明天复习
        elif review_count == 4:
            next_review = now + timedelta(days=3)  # 3 天后复习
        else:
            next_review = now + timedelta(days=7)  # 7 天后复习
        
        is_mastered = 1 if review_count >= 5 else 0
        
        cursor.execute('''
            INSERT INTO learning_progress 
            (word_id, review_count, correct_count, wrong_count, last_reviewed_at, 
             next_review_at, ease_factor, interval, is_mastered)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (word_id, review_count, correct_count, wrong_count,
              now - timedelta(days=review_count), next_review, 2.5, review_count, is_mastered))
    
    conn.commit()
    print(f"✓ 插入 {len(word_ids[:30])} 条学习进度记录\n")
    
    # 插入测试数据 - 错题
    print("插入测试错题...")
    
    # 为前 10 个单词创建错题记录
    for word_id in word_ids[:10]:
        wrong_count = (word_id % 5) + 1
        cursor.execute('''
            INSERT INTO wrong_words (word_id, wrong_count, last_wrong_at)
            VALUES (?, ?, ?)
        ''', (word_id, wrong_count, now - timedelta(days=wrong_count)))
    
    conn.commit()
    print(f"✓ 插入 10 条错题记录\n")
    
    # 插入测试数据 - 学习记录
    print("插入测试学习记录...")
    
    # 为今天和过去几天创建学习记录
    for day_offset in range(7):  # 过去 7 天
        study_date = (now - timedelta(days=day_offset)).date()
        reviewed_at = now - timedelta(days=day_offset, hours=2)
        
        # 每天随机记录一些学习
        num_records = min(20, (7 - day_offset) * 5)
        for j in range(num_records):
            word_id = word_ids[j % len(word_ids)]
            is_correct = 1 if j % 3 != 0 else 0  # 75% 正确率
            
            cursor.execute('''
                INSERT INTO study_records (word_id, study_date, reviewed_at, is_correct)
                VALUES (?, ?, ?, ?)
            ''', (word_id, study_date, reviewed_at, is_correct))
    
    conn.commit()
    print(f"✓ 插入学习记录\n")
    
    # 插入测试数据 - 设置
    print("插入测试设置...")
    
    settings = [
        ('daily_new_words', '20'),
        ('candidate_options', '4'),
        ('enable_local_pronunciation', 'true'),
        ('cache_location', str(Path.home() / ".wordstay")),
        ('current_word_book_id', '1'),
        ('enable_floating_window', 'false'),
        ('floating_window_interval', '10'),
    ]
    
    for key, value in settings:
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
        ''', (key, value))
    
    conn.commit()
    print(f"✓ 插入 {len(settings)} 条设置记录\n")
    
    conn.close()
    
    print(f"✓ 测试数据库创建完成：{db_path}")
    print(f"✓ 数据库包含：")
    print(f"  - {len(test_word_books)} 个单词本")
    print(f"  - {total_words} 个单词")
    print(f"  - 30 条学习进度")
    print(f"  - 10 条错题记录")
    print(f"  - 多天的学习记录")
    print(f"  - 7 条系统设置\n")
    
    return db_path


def main():
    """主函数：生成所有测试数据"""
    print("\n" + "=" * 60)
    print("WordStay 测试数据生成器")
    print("=" * 60 + "\n")
    
    # 生成 TXT 测试文件
    txt_files = create_test_txt_files()
    
    # 生成测试数据库
    db_path = create_test_database()
    
    print("=" * 60)
    print("测试数据生成完成！")
    print("=" * 60)
    print(f"\n生成的文件：")
    print(f"  📁 TXT 测试文件：{len(txt_files)} 个")
    for f in txt_files:
        print(f"     - {f.name}")
    print(f"\n  📁 测试数据库：{db_path.name}")
    print(f"     位置：{db_path.parent}")
    
    print("\n使用说明：")
    print("  1. 运行应用程序：python main.py")
    print("  2. 导入测试单词本：点击'单词本' -> '导入单词本'")
    print("  3. 选择 test_data 目录中的 TXT 文件")
    print("  4. 开始学习和测试各项功能\n")


if __name__ == '__main__':
    main()
