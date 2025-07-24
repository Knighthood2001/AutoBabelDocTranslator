# 🔥 AutoBabelDocTranslator

<div align="center">


[![GitHub Stars](https://img.shields.io/github/stars/Knighthood2001/AutoBabelDocTranslator?style=social)](https://github.com/Knighthood2001/AutoBabelDocTranslator/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Knighthood2001/AutoBabelDocTranslator?style=social)](https://github.com/Knighthood2001/AutoBabelDocTranslator/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/Knighthood2001/AutoBabelDocTranslator)](https://github.com/Knighthood2001/AutoBabelDocTranslator/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Knighthood2001/AutoBabelDocTranslator)](https://github.com/Knighthood2001/AutoBabelDocTranslator/pulls)
[![License](https://img.shields.io/github/license/Knighthood2001/AutoBabelDocTranslator)](https://github.com/Knighthood2001/AutoBabelDocTranslator/blob/main/LICENSE)
[![中文](https://img.shields.io/badge/🇨🇳_中文-当前-blue)](README.md)
[![English](https://img.shields.io/badge/🇺🇸_English-Available-green)](README_en.md)
</div>

> **⚠️ 免责声明：**
> 
> 本工具仅供学习交流使用，请遵守 BabelDOC 平台的使用条款。任何因使用本工具导致的账号问题或法律纠纷，开发者不承担任何责任。

## 🌟 项目简介

**AutoBabelDocTranslator** 是一个自动化工具，能够将 PDF 文件自动上传至 https://app.immersivetranslate.com/babel-doc 平台进行翻译。支持保留登录状态、自动点击验证和翻译按钮，实现自动化 PDF 翻译流程。

### 🛠️ 技术原理

- **基于 Playwright**：使用浏览器自动化技术模拟真实用户操作
- **登录态持久化**：保存 cookies 避免重复登录
- **智能等待机制**：自动检测页面元素，确保操作可靠性

## ✨ 功能特性

✅ **自动上传 PDF 文件**  
✅ **一键触发翻译**  
✅ **登录状态持久化**  
✅ **跨平台支持** (Windows/Linux)  
✅ **可调节视窗大小** (自动适配屏幕尺寸)  

## 🚀 快速开始

### 📋 前置依赖

1. Python 3.8+
2. Playwright 浏览器驱动

### 🔧 安装步骤

```bash
# 克隆仓库
git clone https://github.com/Knighthood2001/AutoBabelDocTranslator.git
cd AutoBabelDocTranslator

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
# 这一步骤可能需要花费较长时间，取决于网络环境
```

### 🏃 使用教程

#### 上传并翻译 PDF

```bash
python main.py https://arxiv.org/pdf/2111.02045
```

另外，`url2babeldoc.py`脚本可以在你的编辑器中执行。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 💖 致谢

- https://playwright.dev/ - 强大的浏览器自动化框架
- https://app.immersivetranslate.com/ - 优秀的翻译平台

---

<div align="center">
✨ 如果这个项目对您有帮助，请给个 ⭐ Star 支持一下！ ✨
</div>