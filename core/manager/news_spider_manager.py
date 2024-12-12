import os
import time
from urllib.parse import quote

from DrissionPage import ChromiumPage
from datetime import datetime, timedelta
from core.manager.dp_manager import DpManager


class NewsSpiderManager:

    def __init__(self):
        self.keywords = list()
        self.page: ChromiumPage = DpManager.run_browser()
        _slice = os.environ.get("ARTICLE_SPIDER_NUMBER") or 2
        _slice = int(_slice)
        self.slice = _slice

        self.target_urls = {
            # "sina": "https://search.sina.com.cn/news",  # 新浪
            "jin10": "https://search.jin10.com/?keyword={keyword}",  # 金十
            # "rbw": "https://newssearch.chinadaily.com.cn/cn/search?query={keyword}",  # 中国日报网
            # "rmw": "http://search.people.cn/",  # 人民网
            # "xhw": "https://so.news.cn/#search/0/{keyword}/1/0",  # 新华网
            # "cfw": "https://so.eastmoney.com/news/s?keyword={keyword}",  # 东方财富网
            # "cls": "https://www.cls.cn/searchPage?keyword={keyword}&type=depth",  # 财联社
            # "ljb": "https://search.kjrb.com.cn:8888/founder/NewSearchServlet.do?siteID=1&content={keyword}"  # 科技日报
        }

    # 设置关键词
    def set_keywords(self, keywords):
        self.keywords = keywords

    def run_spider(self):

        spider_data = []
        for keyword in self.keywords:
            _dict = dict()
            _dict["keyword"] = keyword
            _dict["spider_data"] = list()
            for key in self.target_urls.keys():
                _ = dict()
                _data = getattr(self, f"_{key}_spider")(keyword)
                _["data"] = _data
                _["key"] = key
                _dict["spider_data"].append(_)

            spider_data.append(_dict)

        self.page.close()
        self.page.quit()
        return spider_data

    def _create_tab(self, key: str, keyword: str):
        target_url = self.target_urls[key]

        if "{keyword}" in target_url:
            target_url = target_url.replace("{keyword}", keyword)

        tab = self.page.new_tab(url=target_url)
        return tab

    def _create_empty_tab(self):
        tab = self.page.new_tab()
        return tab

    def _jin10_spider(self, keyword: str):
        print(f"金十[{keyword}]采集中...")
        tab = self._create_tab("jin10", keyword)
        current_time = datetime.now()
        print(f"当前时间: {current_time}")

        # 判断当前时间段
        is_evening = (
                (current_time.hour == 19 and current_time.minute >= 30) or
                (current_time.hour == 20 and current_time.minute <= 30)
        )

        is_morning = (
                (current_time.hour == 11 and current_time.minute >= 30) or
                (current_time.hour == 8 and current_time.minute <= 30)
        )

        time.sleep(5)
        try:
            print("开始查找新闻列表...")
            tab.ele('tag:li@text():快讯').click(by_js=True)
            time.sleep(1)
            news_items = tab.s_ele("tag:div@class=search-body").child("tag:div@role=feed").child(index=2).children()

            result = []
            index = 0
            for item in news_items:
                if index >= self.slice:
                    break

                try:
                    content = item.text
                    title = content.split("\n")[0]
                    pub_time_str = content.split("\n")[1]

                    # 解析发布时间
                    if " " in pub_time_str:  # 格式: "12-05 18:48:10"
                        date_str = f"{current_time.year}-{pub_time_str.replace(' ', ' ')}"
                        pub_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    else:  # 格式: "15:38:28"
                        time_str = f"{current_time.date()} {pub_time_str}"
                        pub_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

                    # 时间筛选逻辑
                    valid_time = False
                    if is_evening:
                        # 晚间：15:00-20:30
                        valid_time = (
                                pub_time.hour >= 15 and
                                pub_time.date() == current_time.date() and
                                pub_time.hour < 20  # 改为严格小于20点
                        )
                    elif is_morning:
                        # 早间：前一天20:00-当天8:30
                        yesterday = current_time.date() - timedelta(days=1)
                        valid_time = (
                            # 当天的数据
                                (pub_time.date() == current_time.date() and
                                 pub_time.hour < 12) or  # 改为严格小于8点
                                # 前一天的数据
                                (pub_time.date() == yesterday and pub_time.hour >= 20)
                        )
                    else:
                        valid_time = False  # 其他时间段不做筛选

                    if valid_time and title and pub_time_str:
                        _dict = {
                            "title": title,
                            "pub_time": pub_time_str
                        }
                        index += 1
                        result.append(_dict)
                        print(f"收录新闻: {title[:30]}... - {pub_time_str}")  # 添加调试信息

                except Exception as e:
                    continue

            print(f"共收录 {len(result)} 条新闻")  # 添加调试信息
            tab.close()
            return result

        except Exception as e:
            print(f"金十爬虫整体出错: {str(e)}")
            if 'tab' in locals():
                tab.close()
            return []




if __name__ == "__main__":
    manager = NewsSpiderManager()
    _keywords = ["互动平台"]
    manager.set_keywords(keywords=_keywords)
    manager.run_spider()
