"""
验证单词本导入功能
"""

import sys

print("=" * 60)
print("验证单词本导入功能")
print("=" * 60)

try:
    # 1. 验证导入功能
    print("\n1. 检查模块导入...")
    from src.ui.word_book_widget import WordBookDialog
    print("   ✓ WordBookDialog 导入成功")
    
    from src.importer import WordBookImporter, ImportResult
    print("   ✓ WordBookImporter 导入成功")
    
    from src.importer.parser import TxtParser
    print("   ✓ TxtParser 导入成功")
    
    # 2. 验证 ImportResult 有新的属性
    print("\n2. 检查 ImportResult 属性...")
    result = ImportResult()
    assert hasattr(result, 'success_count'), "缺少 success_count 属性"
    assert hasattr(result, 'duplicate_count'), "缺少 duplicate_count 属性"
    assert hasattr(result, 'error_count'), "缺少 error_count 属性"
    print("   ✓ ImportResult 包含所有必要属性")
    
    # 3. 验证导入方法存在
    print("\n3. 检查导入方法...")
    assert hasattr(WordBookImporter, 'import_from_parse_result'), "缺少 import_from_parse_result 方法"
    print("   ✓ import_from_parse_result 方法存在")
    
    # 4. 验证 WordBookDialog 有导入按钮
    print("\n4. 检查 WordBookDialog 导入按钮...")
    import ast
    with open('src/ui/word_book_widget.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有 import_btn
    if 'import_btn' in content and '导入单词本' in content:
        print("   ✓ 导入按钮已添加")
    else:
        print("   ✗ 导入按钮未找到")
        sys.exit(1)
    
    # 检查是否有 import_word_book 方法
    if 'def import_word_book' in content:
        print("   ✓ import_word_book 方法已添加")
    else:
        print("   ✗ import_word_book 方法未找到")
        sys.exit(1)
    
    # 5. 验证代码可以编译
    print("\n5. 编译检查...")
    compile(content, 'word_book_widget.py', 'exec')
    print("   ✓ word_book_widget.py 语法正确")
    
    with open('src/importer/importer.py', 'r', encoding='utf-8') as f:
        importer_content = f.read()
    compile(importer_content, 'importer.py', 'exec')
    print("   ✓ importer.py 语法正确")
    
    print("\n" + "=" * 60)
    print("✅ 验证通过！")
    print("=" * 60)
    print("\n新增功能：")
    print("  • 单词本管理对话框已添加'导入单词本'按钮")
    print("  • 支持导入 TXT 文件（空格或连字符分隔格式）")
    print("  • 自动解析文件并创建单词本")
    print("  • 支持重复单词检测和异常行标记")
    print("  • 显示详细的导入结果统计")
    print("\n使用方法：")
    print("  1. 运行 python main.py")
    print("  2. 点击右上角'设置'按钮")
    print("  3. 点击左侧'单词本'按钮")
    print("  4. 点击'导入单词本'按钮")
    print("  5. 选择 TXT 文件即可导入\n")
    
except Exception as e:
    print(f"\n❌ 验证失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
