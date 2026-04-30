import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.connection import get_connection
from database.crud import LearningProgressCRUD, WordCRUD, WordBookCRUD

def test_word_loading():
    print("测试单词加载...")
    
    conn = get_connection()
    import sqlite3
    conn.row_factory = sqlite3.Row
    
    # 获取所有单词本
    word_books = WordBookCRUD.get_all(conn)
    print(f"\n找到 {len(word_books)} 个单词本")
    
    for book in word_books:
        print(f"\n单词本: {book['name']} (ID: {book['id']})")
        
        # 获取该单词本的单词
        words = WordCRUD.get_by_word_book_id(conn, book['id'])
        print(f"  总单词数: {len(words)}")
        
        # 获取待学习单词
        due_words = LearningProgressCRUD.get_due_words(conn, book['id'])
        print(f"  待学习单词数: {len(due_words)}")
        
        if due_words:
            print("\n  前3个待学习单词:")
            for i, word in enumerate(due_words[:3]):
                definition = word['definition'] if 'definition' in word.keys() else 'N/A'
                print(f"    {i+1}. {word['word']} - {definition}")
    
    conn.close()

if __name__ == '__main__':
    test_word_loading()
