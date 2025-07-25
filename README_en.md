# 🔥 AutoBabelDocTranslator

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/Knighthood2001/AutoBabelDocTranslator?style=social)](https://github.com/Knighthood2001/AutoBabelDocTranslator/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Knighthood2001/AutoBabelDocTranslator?style=social)](https://github.com/Knighthood2001/AutoBabelDocTranslator/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/Knighthood2001/AutoBabelDocTranslator)](https://github.com/Knighthood2001/AutoBabelDocTranslator/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Knighthood2001/AutoBabelDocTranslator)](https://github.com/Knighthood2001/AutoBabelDocTranslator/pulls)
[![中文](https://img.shields.io/badge/🇨🇳_中文文档-blue)](README.md)
[![English](https://img.shields.io/badge/🇺🇸_English-Available-green)](README_en.md)
</div>

> **⚠️ Disclaimer:**
> 
> This tool is for learning and communication purposes only. Please comply with BabelDOC's terms of service. The developer is not responsible for any account issues or legal disputes caused by using this tool.

## 🌟 Project Introduction

**AutoBabelDocTranslator** is an automation tool that can automatically upload PDF files to https://app.immersivetranslate.com/babel-doc for translation. It supports login state persistence, automatic verification clicking, and translation button triggering, enabling an automated PDF translation workflow.

### 🛠️ Technical Principles

- **Based on Playwright**: Uses browser automation to simulate real user operations
- **Login State Persistence**: Saves cookies to avoid repeated logins
- **Smart Waiting Mechanism**: Automatically detects page elements to ensure operational reliability

## ✨ Features

✅ **Automatic PDF Upload**  
✅ **One-click Translation**  
✅ **Login State Persistence**  
✅ **Cross-platform Support** (Windows/Linux)  

## 📝 URL Support
Only supports web links that directly point to PDF files

| **Website Link** | **Support Status** | **Notes** | 
| ---         |---          |---      | 
| arxiv | ✅ Supported |Automatically retrieves paper title as PDF filename|
| CVPR | ✅ Supported | Automatically retrieves paper name|
| Other PDF links |✅ Supported | Requires custom PDF filename|


## 🚀 Quick Start

### 📋 Prerequisites

1. Python 3.8+
2. Playwright browser drivers

### 🔧 Installation Steps

```bash
# Clone repository
git clone https://github.com/Knighthood2001/AutoBabelDocTranslator.git
cd AutoBabelDocTranslator

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
# This step may take some time depending on network conditions
```

### 🏃 Usage Guide

#### Upload and Translate PDF

```bash
python main.py
```

## 🤝 Contribution Guidelines

Issues and Pull Requests are welcome!

## 💖 Acknowledgments

- https://playwright.dev/ - Powerful browser automation framework
- https://app.immersivetranslate.com/ - Excellent translation platform

---

<div align="center">
✨ If you find this project helpful, please give it a ⭐ Star! ✨
</div>
