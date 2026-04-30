# WordStay - 单词记忆应用

## 项目简介

WordStay 是一个功能完整的桌面端单词学习应用程序，基于 PyQt6 开发，采用艾宾浩斯记忆曲线算法，帮助用户高效记忆单词。

## 功能特性

### 核心功能
- ✅ **TXT 单词本导入**：支持"单词 释义"和"单词 - 释义"两种格式，自动去重、标记异常行
- ✅ **双向答题模式**：
  - 英译中：显示英文单词，输入中文释义
  - 中译英：显示中文释义，拼写英文单词
- ✅ **单词标记**：可标记"已掌握"或"不熟悉"，已掌握单词不再复习
- ✅ **艾宾浩斯记忆曲线**：首次记忆→10 分钟→1 小时→1 天→3 天→7 天
- ✅ **学习进度管理**：自动保存学习位置，下次打开续学

### 扩展功能
- ✅ **错题本**：自动收集答错单词，支持"错题特训"模式
- ✅ **学习统计**：今日学习数、累计掌握数、复习完成率
- ✅ **桌面悬浮窗**：迷你可拖动置顶窗，随机显示待复习单词，悬停显示释义
- ✅ **自定义设置**：每日学习新词数、答题候选选项数、开关单词本地发音
- ✅ **多单词本管理**：支持导入多个 TXT，切换学习、单独保存进度
- ✅ **快捷键操作**：
  - `空格` - 确认答案
  - `↑↓` - 选择选项
  - `Ctrl+S` - 保存
  - `Esc` - 最小化到托盘
- ✅ **数据缓存配置**：可自定义数据缓存存放位置

## 技术栈

- **界面框架**：PyQt6
- **数据库**：SQLite3（Python 内置）
- **文件解析**：Python 原生文件操作
- **记忆算法**：自定义艾宾浩斯曲线实现
- **本地发音**：pyttsx3
- **打包工具**：PyInstaller

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

### 直接运行
```bash
python main.py
```

### 功能测试
```bash
python test_app.py    # 测试核心功能模块
python test_ui.py     # 测试 UI 组件
```

## 打包成可执行文件

### Windows
```bash
.\build.bat
```
或手动执行：
```bash
pyinstaller WordStay.spec --clean
```

打包后的可执行文件位于 `dist/WordStay.exe`

### Mac/Linux
```bash
pyinstaller WordStay.spec --clean
```

## 项目结构

```
WordStay/
├── src/
│   ├── algorithm/        # 艾宾浩斯记忆曲线算法
│   │   ├── __init__.py
│   │   ├── ebbinghaus.py # 记忆曲线核心算法
│   │   └── scheduler.py  # 单词调度器
│   ├── database/         # SQLite3 数据库模块
│   │   ├── __init__.py
│   │   ├── connection.py # 数据库连接管理
│   │   ├── crud.py       # CRUD 操作
│   │   └── init.py       # 数据库初始化
│   ├── importer/         # TXT 单词本解析器
│   │   ├── __init__.py
│   │   ├── parser.py     # TXT 解析器
│   │   └── importer.py   # 单词本导入器
│   ├── settings/         # 设置管理模块
│   │   ├── __init__.py
│   │   ├── settings_manager.py
│   │   └── settings_dialog.py
│   ├── statistics/       # 学习统计模块
│   │   ├── __init__.py
│   │   └── calculator.py
│   └── ui/               # PyQt6 界面模块
│       ├── __init__.py
│       ├── main_window.py        # 主窗口
│       ├── learning_widget.py    # 学习界面
│       ├── wrong_word_widget.py  # 错题本界面
│       ├── statistics_widget.py  # 统计界面
│       ├── word_book_widget.py   # 单词本管理
│       ├── floating_window.py    # 桌面悬浮窗
│       └── components.py         # 通用组件
├── main.py               # 应用入口
├── requirements.txt      # 依赖列表
├── WordStay.spec         # PyInstaller 打包配置
├── build.bat             # Windows 打包脚本
├── test_app.py           # 功能测试脚本
├── test_ui.py            # UI 测试脚本
├── .gitignore
└── README.md
```

## 使用说明

### 1. 导入单词本
1. 点击主界面右上角"设置"按钮
2. 在侧边栏点击"单词本"按钮
3. 点击"导入单词本"，选择 TXT 文件
4. 支持格式：
   ```
   apple 苹果
   banana 香蕉
   orange - 橙子
   ```

### 2. 开始学习
1. 选择答题模式（英译中/中译英）
2. 输入答案后按空格键确认
3. 可使用↑↓键选择按钮
4. 答错自动加入错题本

### 3. 错题特训
1. 点击侧边栏"错题本"
2. 切换到"错题特训"标签
3. 专注练习错题

### 4. 查看统计
1. 点击侧边栏"统计"
2. 查看今日学习数、累计掌握数等

### 5. 启用悬浮窗
1. 点击右上角"设置"
2. 在"悬浮窗设置"中启用
3. 可调整单词切换间隔

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| `空格` | 确认答案/下一个单词 |
| `↑` | 上一个选项 |
| `↓` | 下一个选项 |
| `Enter` | 触发选中按钮 |
| `Ctrl+S` | 保存 |
| `Esc` | 最小化到托盘 |

## 系统要求

- Python 3.8+
- Windows/Mac/Linux
- PyQt6
- pyttsx3（可选，用于本地发音）

## 注意事项

1. 首次运行会自动创建默认单词本
2. 数据默认保存在 `~/.wordstay/` 目录
3. 可通过设置自定义数据缓存位置
4. 已掌握的单词不会出现在复习列表中

## 开发说明

### 运行测试
```bash
# 功能测试
python test_app.py

# UI 组件测试
python test_ui.py
```

### 代码规范
- 遵循 PEP 8 编码规范
- 使用类型提示
- 模块化设计

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
