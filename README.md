# Welcome Page Static Agent

一个基于 Web 的欢迎页面静态智能体，提供交互式聊天界面和多种工具功能。

## Features

- 🤖 **智能聊天** - 交互式聊天界面，支持实时对话
- 🧮 **计算器** - 支持数学计算功能
- 🌤️ **天气查询** - 查询指定城市的天气情况
- 📝 **文件操作** - 支持文件读写操作
- 🎨 **现代化 UI** - 渐变紫色背景，卡片式布局，平滑动画效果

## Getting Started

### 本地运行

```bash
# 启动 HTTP 服务器
python -m http.server 8000

# 访问页面
open http://localhost:8000/welcome.html
```

### 项目结构

```
├── welcome.html    # 欢迎页面（含聊天功能）
├── agent.py        # 智能体核心类
└── README.md       # 项目说明文档
```

## Usage

1. 打开 `welcome.html` 页面
2. 点击「开始对话」按钮进入聊天模式
3. 输入问题与智能助手进行交互

## Technologies

- HTML5
- CSS3
- JavaScript (ES6+)
- Python 3 (后端智能体)

## License

MIT
