import json  # 导入JSON模块，用于处理关键词列表
import os  # 导入OS模块，用于环境变量操作

from core.handler.spider_handler import SpiderHandler  # 导入SpiderHandler类


# 初始化配置数据
def __init_data():
    # 设置默认的API密钥
    os.environ.setdefault("DASHSCOPE_API_KEY", "sk-18987f46bd2543619b5d52f32ebb1127")
    os.environ.setdefault("ARTICLE_NUMBER", "8")  # 用于生成海报的文章数量
    os.environ.setdefault("ARTICLE_SPIDER_NUMBER", "10")  # 每次采集的新闻文章数量

    # 定义需要采集的关键词列表
    _keywords = ["互动平台"]
    os.environ.setdefault("SPIDER_KEYWORDS", json.dumps(_keywords))  # 将关键词序列化为JSON格式并保存


__init_data()  # 初始化配置

# 执行调度任务
def run_schedule():
    handler = SpiderHandler()  # 实例化SpiderHandler类
    handler.run_spider()  # 立即执行一次爬虫任务


# 程序入口
if __name__ == '__main__':
    # print(f"Key: {key}, Keyword: {keyword}")
    run_schedule()  # 运行调度任务
