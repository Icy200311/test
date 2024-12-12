import json
import os
import typing
from dashscope.api_entities.dashscope_response import Choice
# from core.manager.carbon_spider_manager import CarbonSpiderManager
from core.manager.ds_manager import DashScopeManager
from core.manager.news_spider_manager import NewsSpiderManager
from core.utils.date_util import DateUtil
#  导入各个模块

class SpiderHandler(object):
    #定义爬虫运行方法
    def run_spider(self):
        _keywords_str = os.environ.get("SPIDER_KEYWORDS") or ""
        _keywords = ["互动平台"]
        if bool(_keywords_str):
            _keywords = json.loads(_keywords_str)

        timestamp = DateUtil.get_timestamp()
        time_str = DateUtil.timestamp_format(timestamp, "%Y-%m-%d_%H-%M-%S")

        # 新闻数据采集
        spider_data = self._news_spider(_keywords, time_str)

        # 文本大模型处理新闻
        # self._ai_llm(_keywords, spider_data, time_str)

        # 碳市场交易数据采集
        # carbon_data = self._carbon_spider()

        # ai生成banner图
        # ai_img_path = self._ai_img(time_str)

        # html转图片
        # self._html_to_image(ai_img_path, time_str)

        # msg = f"执行成功，数据已处理完毕。"
        # print(f"{msg}\n\n")
        #
        # print("请等待下一次任务调度执行...\n\n")
        # logger.info(msg)

        print("请等待下一次任务调度执行...\n\n")

    @staticmethod
    def _html_to_image(ai_img_path, time_str):
        slice_article_number = os.environ.get("ARTICLE_NUMBER") or 8
        slice_article_number = int(slice_article_number)

        while True:
            result = input(f"人工审核[{time_str}_poster.jpg]的新闻内容是否已完成(yes/no)?")
            if result == 'yes':
                break

        with open(f"./spider_cache/{time_str}_cn_data.json", "r", encoding="utf-8") as f:
            cn_str = f.read()

        _cn = json.loads(cn_str)

        cn = list()
        for item in _cn:
            if bool(item["used"]):
                cn.append(item)

        _data = {"cn": cn[:slice_article_number], "aiImgPath": ai_img_path}

    @staticmethod
    def _ai_img(time_str):
        # while True:
        #     ai_img_path = input(f"\n\n请配置[{time_str}_poster.jpg]Banner图片的本地绝对路径：")
        #     if os.path.exists(ai_img_path):
        #         break
        ai_img_path="C:\\Users\\21182\\Desktop\\Task\\Spider\\insert_image\\智能城市\\1.jpg"
        return ai_img_path

    # @staticmethod
    # def _carbon_spider():
    #     carbon_spider_manager = CarbonSpiderManager()
    #     carbon_data = carbon_spider_manager.run_spider()
    #     return carbon_data

    @staticmethod
    def _ai_llm(_keywords, spider_data, time_str):
        cn = list()
        themes = list()
        start_time = DateUtil.get_timestamp()
        print("开始处理新闻数据...")
        
        for _spider in spider_data:
            _keyword = _spider.get("keyword")
            _spider_data = _spider.get("spider_data")

            for _ in _spider_data:
                _data = _.get("data")
                for __data in _data:
                    _article: str = __data.get("article")
                    pub_time = __data.get("pub_time", "未知时间")
                    
                    choices: typing.List[Choice] = DashScopeManager.chat(
                        topic=_keyword,
                        content=_article,
                        pub_time=pub_time
                    )
                    
                    ai_article = json.loads(choices[0].message.content
                                         .replace("json\n", "")
                                         .replace("`", "")
                                         .replace(" ", "")
                                         .replace("\n", ""))

                    if _keyword == _keywords[0]:
                        cn.append({
                            "pub_time": pub_time,
                            "title": ai_article.get("title"),
                            "con": ai_article.get("con"),
                            "used": True
                        })
                        
                        themes.append({
                            "pub_time": pub_time,
                            "title": ai_article.get("title")
                        })

        end_time = DateUtil.get_timestamp()
        print(f"耗时[{end_time - start_time}]秒，数据处理完成!!!")

        # 保存数据
        with open(f"./spider_cache/{time_str}_low_sky_economy_data.json", "w", encoding="utf-8") as f:
            json.dump(cn, f, ensure_ascii=False, indent=2)

        with open(f"./spider_cache/{time_str}_themes.json", "w", encoding="utf-8") as f:
            json.dump(themes, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _news_spider(_keywords, time_str):
        spider_manager = NewsSpiderManager()

        spider_manager.set_keywords(keywords=_keywords)
        start_time = DateUtil.get_timestamp()
        print("开始采集...")
        spider_data = spider_manager.run_spider()
        end_time = DateUtil.get_timestamp()
        print(f"耗时[{end_time - start_time}]秒，采集完成!!!!")

        with open(f"./spider_cache/{time_str}_spider_data.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(spider_data, ensure_ascii=False))
        return spider_data


if __name__ == '__main__':
    # SpiderHandler.html_to_image([], [], [], [], "2024-10-29_21-39-39")
    pass