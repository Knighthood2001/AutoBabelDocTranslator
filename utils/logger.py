import logging
from typing import Any
import sys
from pathlib import Path

def setup_logger(
    name: str = "AutoBabelDocTranslator",
    log_file: str = "AutoBabelDocTranslator.log",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG
) -> logging.Logger:
    """
    配置并返回一个标准logger实例
    
    :param name: 日志器名称
    :param log_file: 日志文件路径
    :param console_level: 控制台日志级别
    :param file_level: 文件日志级别
    :return: 配置好的logging.Logger实例
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置根级别为最低
    
    # 确保不重复添加handler
    if logger.handlers:
        return logger
    
    # 创建日志目录
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 标准格式 - 移除了文件名和行号
    formatter = logging.Formatter(
        fmt="%(asctime)s %(name)s %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)
    logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)
    logger.addHandler(file_handler)
    
    return logger

# 全局日志器实例
logger = setup_logger()

# 快捷方法
def debug(msg: Any, **kwargs):
    logger.debug(msg, **kwargs)

def info(msg: Any, **kwargs):
    logger.info(msg, **kwargs)

def warning(msg: Any, **kwargs):
    logger.warning(msg, **kwargs)

def error(msg: Any, **kwargs):
    logger.error(msg, **kwargs)

def critical(msg: Any, **kwargs):
    logger.critical(msg, **kwargs)

if __name__ == '__main__':
    debug('This is a debug message')
    info('This is an info message')
    warning('This is a warning message')
    error('This is an error message')
    critical('This is a critical message')