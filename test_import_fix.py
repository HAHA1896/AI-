import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.connection import get_connection
from database.crud import WordBookCRUD, WordCRUD, LearningProgressCRUD
from importer.importer import WordBookImporter

def test_import_with_learning_progress():
    print("测试导入功能是否正确创建学习进度记录...")
    
    test_file = os.path.join(os.path.dirname(__file__), 'test_data', 'test_vocab_cet4.txt')
    
    if not os.path.exists(test_file):
        print(f"测试文件不存在: {test_file}")
        return False
    
    # 导入单词本
    result = WordBookImporter.import_from_txt(
        test_file,
        '测试单词本 - 修复验证',
        '用于验证导入修复功能'
    )
    
    print(f"导入结果: {result.message}")
    print(f"成功导入: {result.success_count} 个单词")
    
    if not result.success:
        print("导入失败！")
        return False
    
    # 检查数据库中的学习进度记录
    conn = get_connection()
    conn.row_factory = True
    
    # 获取单词
    words = WordCRUD.get_by_word_book_id(conn, result.word_book_id)
    print(f"\n数据库中有 {len(words)} 个单词")
    
    # 检查每个单词是否有学习进度记录
    missing_progress = []
    for word in words:
        progress = LearningProgressCRUD.get_by_word_id(conn, word['id'])
        if progress is None:
            missing_progress.append(word['word'])
    
    if missing_progress:
        print(f"\n错误: 以下单词没有学习进度记录: {missing_progress}")
        conn.close()
        return False
    
    print("\n✓ 所有单词都有学习进度记录！")
    
    # 测试获取待学习单词
    due_words = LearningProgressCRUD.get_due_words(conn, result.word_book_id)
    print(f"获取到 {len(due_words)} 个待学习单词")
    
    if len(due_words) != len(words):
        print(f"错误: 应该获取到 {len(words)} 个单词，但只获取到 {len(due_words)} 个")
        conn.close()
        return False
    
    print("✓ 所有单词都能被正确获取为待学习单词！")
    
    conn.close()
    return True

if __name__ == '__main__':
    success = test_import_with_learning_progress()
    if success:
        print("\n🎉 所有测试通过！导入功能已修复。")
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)
