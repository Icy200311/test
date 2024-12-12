from DrissionPage import ChromiumOptions, ChromiumPage
import time


class DpManager(object):

    @staticmethod
    def run_browser() -> ChromiumPage or None:
        co = ChromiumOptions()
        co.auto_port(True)  # 此方法用于设置是否使用自动分配的端口，启动一个全新的浏览器
        co.headless()
        co.set_argument('--headless=new')
        co.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
        co.set_argument('--no-sandbox')
        co.set_argument('--disable-dev-shm-usage')
        co.set_argument('--disable-gpu')
        
        max_retries = 3
        for i in range(max_retries):
            try:
                page: ChromiumPage = ChromiumPage(co)
                return page
            except Exception as e:
                print(f"浏览器启动失败 (尝试 {i+1}/{max_retries}): {str(e)}")
                if i < max_retries - 1:
                    time.sleep(2)  # 等待2秒后重试
                else:
                    raise e  # 最后一次尝试失败时抛出异常
        
        return None

