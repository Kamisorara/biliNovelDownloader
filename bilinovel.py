import requests
import re
import os
from lxml import etree

# 此脚本仅用于下载bili轻小说
data_map = {'\ue800': '的', '\ue801': '一', '\ue802': '是', '\ue803': '了', '\ue804': '我', '\ue805': '不',
            '\ue806': '人', '\ue807': '在', '\ue808': '他', '\ue809': '有', '\ue80a': '这', '\ue80b': '个',
            '\ue80c': '上', '\ue80d': '们', '\ue80e': '来', '\ue80f': '到', '\ue810': '时', '\ue811': '大',
            '\ue812': '地', '\ue813': '为',
            '\ue814': '子', '\ue815': '中', '\ue816': '你', '\ue817': '说', '\ue818': '生', '\ue819': '国',
            '\ue81a': '年', '\ue81b': '着', '\ue81c': '就', '\ue81d': '那', '\ue81e': '和', '\ue81f': '要',
            '\ue820': '她', '\ue821': '出', '\ue822': '也', '\ue823': '得', '\ue824': '里', '\ue825': '后',
            '\ue826': '自', '\ue827': '以', '\ue828': '会', '\ue829': '家', '\ue82a': '可', '\ue82b': '下',
            '\ue82c': '而', '\ue82d': '过', '\ue82e': '天', '\ue82f': '去', '\ue830': '能', '\ue831': '对',
            '\ue832': '小', '\ue833': '多', '\ue834': '然', '\ue835': '于', '\ue836': '心', '\ue837': '学',
            '\ue838': '么', '\ue839': '之', '\ue83a': '都', '\ue83b': '好', '\ue83c': '看', '\ue83d': '起',
            '\ue83e': '发', '\ue83f': '当', '\ue840': '没', '\ue841': '成', '\ue842': '只', '\ue843': '如',
            '\ue844': '事', '\ue845': '把', '\ue846': '还', '\ue847': '用', '\ue848': '第',
            '\ue849': '让', '\ue84a': '道', '\ue84b': '想', '\ue84c': '作', '\ue84d': '种', '\ue84e': '开',
            '\ue84f': '美', '\ue850': '总', '\ue851': '从', '\ue852': '无', '\ue853': '情', '\ue854': '己',
            '\ue855': '面', '\ue856': '最', '\ue857': '女', '\ue858': '但', '\ue859': '现', '\ue85a': '前',
            '\ue85b': '些', '\ue85c': '所', '\ue85d': '同', '\ue85e': '日', '\ue85f': '手', '\ue860': '又',
            '\ue861': '行', '\ue862': '意', '\ue863': '动'
            }

list_1 = [
    '\ue800', '\ue801', '\ue802', '\ue803', '\ue804',
    '\ue805', '\ue806', '\ue807', '\ue808', '\ue809',
    '\ue80a', '\ue80b', '\ue80c', '\ue80d', '\ue80e',
    '\ue80f', '\ue810', '\ue811', '\ue812', '\ue813',
    '\ue814', '\ue815', '\ue816', '\ue817', '\ue818',
    '\ue819', '\ue81a', '\ue81b', '\ue81c', '\ue81d',
    '\ue81e', '\ue81f', '\ue820', '\ue821', '\ue822',
    '\ue823', '\ue824', '\ue825', '\ue826', '\ue827',
    '\ue828', '\ue829', '\ue82a', '\ue82b', '\ue82c',
    '\ue82d', '\ue82e', '\ue82f', '\ue830', '\ue831',
    '\ue832', '\ue833', '\ue834', '\ue835', '\ue836',
    '\ue837', '\ue838', '\ue839', '\ue83a', '\ue83b',
    '\ue83c', '\ue83d', '\ue83e', '\ue83f', '\ue840',
    '\ue841', '\ue842', '\ue843', '\ue844', '\ue845',
    '\ue846', '\ue847', '\ue848', '\ue849', '\ue84a',
    '\ue84b', '\ue84c', '\ue84d', '\ue84e', '\ue84f',
    '\ue850', '\ue851', '\ue852', '\ue853', '\ue854',
    '\ue855', '\ue856', '\ue857', '\ue858', '\ue859',
    '\ue85a', '\ue85b', '\ue85c', '\ue85d', '\ue85e',
    '\ue85f', '\ue860', '\ue861', '\ue862', '\ue863']

list_2 = [
    '的', '一', '是', '了', '我',
    '不', '人', '在', '他', '有',
    '这', '个', '上', '们', '来',
    '到', '时', '大', '地', '为',
    '子', '中', '你', '说', '生',
    '国', '年', '着', '就', '那',
    '和', '要', '她', '出', '也',
    '得', '里', '后', '自', '以',
    '会', '家', '可', '下', '而',
    '过', '天', '去', '能', '对',
    '小', '多', '然', '于', '心',
    '学', '么', '之', '都', '好',
    '看', '起', '发', '当', '没',
    '成', '只', '如', '事', '把',
    '还', '用', '第', '让', '道',
    '想', '作', '种', '开', '美',
    '总', '从', '无', '情', '己',
    '面', '最', '女', '但', '现',
    '前', '些', '所', '同', '日',
    '手', '又', '行', '意', '动']


class biliNovel:
    def __init__(self, novel_num):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
        # 小说编号
        self.novel_num = novel_num
        self.main_url = 'https://www.linovelib.com/'
        # 小说名
        self.novel_title = ""
        # 小说字数(str)
        self.novel_word_count = ""
        # 小说卷列表
        self.novel_chapters = []
        # 小说具体章节 [[[]], [[]], [[]]]
        self.novel_chapter_detail = []

    def request_method(self, request_url):
        res = requests.get(request_url, headers=self.header)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            res_element = etree.HTML(res.text)
            return res_element
        else:
            print("网络请求失败！！！")
            return None

    # 获取主页
    def get_index_page(self):
        # 拼接url
        url = "https://www.linovelib.com/novel/" + self.novel_num + "/catalog"
        # 请求首页
        index_page_element = self.request_method(url)
        if index_page_element is not None:
            # 小说标题
            self.novel_title = index_page_element.xpath(
                '/html/body/div[2]/div[3]/div[1]/h1/text()')[0]
            # 小说字数
            self.novel_word_count = index_page_element.xpath(
                '//div[@class="container"]/div[2]/div[1]/p/span/cite/text()')[0]
            # 小说章节
            self.novel_chapters = index_page_element.xpath(
                '//div[@class="volume-list"]/div/ul/div[@class="volume"]/text()')
            # 分割章节
            ul_element = index_page_element.xpath(
                '//div[@class="volume-list"]/div/ul')[0]
            # 获取 <ul> 元素下的所有子元素
            elements = ul_element.xpath('*')
            segments = []
            current_segment = []
            for elem in elements:
                # 如果是章节的开始
                if elem.tag == "div":
                    if current_segment:
                        segments.append(current_segment)
                    current_segment = []
                elif elem.tag == "li":
                    # 获取对应话名称
                    chapter_content_title = elem.xpath('./a/text()')[0]
                    # 获取对应话地址
                    chapter_content_url = elem.xpath('./a/@href')[0]
                    current_segment.append(
                        [chapter_content_title, chapter_content_url])
            # 处理最后一个段落
            if current_segment:
                segments.append(current_segment)

            self.novel_chapter_detail = segments
            # 打印list测试
            # print(segments)
        else:
            print("无HTML内容，无法解析!!!")

    # 根据输入下载
    def download_order(self, number):
        if number == 0:
            total_num = len(self.novel_chapters)
            for i in range(total_num):
                self.download_novel(i)
        else:
            self.download_novel(number - 1)

    # 下载具体小说
    def download_novel(self, download_num):
        # 当前小说名 + 卷名
        novel_title_num = self.novel_title + "-" + self.novel_chapters[download_num]
        # 小说名 + 格式
        file_name = novel_title_num + ".txt"
        # 获取具体下载拿一本书 [['插图', '/novel/2547/128663.html'], ['第1话 与天使共度岁末', '/novel/2547/128651.html']]
        novel_download_list = self.novel_chapter_detail[download_num]
        # 这本小说的话数 
        novel_count = len(novel_download_list)
        # 打印测试
        print(novel_title_num)
        print(novel_download_list)
        print("共有" + str(novel_count) + "话")
        # 创建文件夹
        folder_name = self.novel_title
        # 获取当前工作目录
        current_directory = os.getcwd()
        # 构建文件夹路径
        folder_path = os.path.join(current_directory, folder_name)
        # 创建文件夹(如果不存在则创建)
        os.makedirs(folder_path, exist_ok=True)
        # 开始下载具体话
        for count in range(novel_count):
            # 创建这个文件的地址
            file_path = os.path.join(folder_path, file_name)
            # 添加标题
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(novel_download_list[count][0] + '\n\n')
            # 拼接url
            page_url = self.main_url + novel_download_list[count][1]
            self.write_method(page_url, file_path, novel_download_list[count][0])
            # 判断这一话是否下载完全
            next_page_url = self.is_exhaustive(page_url)
            if next_page_url is not None:
                last_slash_index = next_page_url.rindex("/") + 1
                underscore_index = next_page_url.rindex("_")
                # 当前页的页码
                result_num = next_page_url[last_slash_index:underscore_index]
                # 获取这一话的页数
                res_element = self.request_method(next_page_url)
                page_num = res_element.xpath('//*[@id="mlfy_main_text"]/h1/text()')[0]
                # 使用正则提取
                pattern = r"\d+"
                matches = re.findall(pattern, page_num)
                if matches:
                    page_num = matches[-1]
                for page_count in range(2, int(page_num) + 1):
                    # 拼接url https://www.linovelib.com/novel/2547/resultNum_pageCount.html
                    page_url_temp = self.main_url + "/novel/" + self.novel_num + "/" + result_num + "_" + str(
                        page_count) + ".html"
                    # print(page_url_temp)
                    self.write_method(page_url_temp, file_path, novel_download_list[count][0])
            print(novel_download_list[count][0] + "···下载完成")
        # 最终下载完成
        print("·········" + novel_title_num + "·········" + "下载完成")

    # 写入文件方法
    def write_method(self, page_url, file_path, novel_detail_name):
        str_list = self.download_novel_page(page_url)
        if str_list is not None:
            with open(file_path, 'a', encoding='utf-8') as f:
                for i in range(len(str_list)):
                    f.write(str_list[i] + '\n\n')
        else:
            print(novel_detail_name + "···下载失败")

    # 下载具体页
    def download_novel_page(self, page_url):
        res_element = self.request_method(page_url)
        if res_element is not None:
            # 获取内容
            content = res_element.xpath('//div[@class="read-content"]/p/text()')
            # return的字符串list
            str_list = []
            for i in range(len(content)):
                str_n = ""
                for j in range(len(content[i])):
                    str_n += content[i][j]
                str_list.append(str_n)

            # 处理bilinovel的反爬机制
            for i in range(len(str_list)):
                content_str = str_list[i]
                for j in range(100):
                    content_str = content_str.replace(list_1[j], list_2[j])
                str_list[i] = content_str
            return str_list
        else:
            return None

    # 判断当前话是否完整
    def is_exhaustive(self, page_url):
        res_element = self.request_method(page_url)
        if res_element is not None:
            # 获取下一页按钮的url
            next_page_url = res_element.xpath('//p[@class="mlfy_page"]/a[5]/@href')[0]
            if '_' in next_page_url:
                return self.main_url + next_page_url
            else:
                return None

    # 使用正则判断url 是否合法
    def check_string_format(self, string):
        pattern = r'^/novel/\d+/(\d+(_\d+)?\.html)$'
        if re.match(pattern, string):
            return True
        else:
            return False


if __name__ == '__main__':
    # 小说编号
    novel_number = input("输入小说编号(例如“2547”):")
    # 实例化
    bili = biliNovel(novel_number)
    # 获取主页相关信息
    bili.get_index_page()
    # 终端打印
    print(bili.novel_title)
    print(bili.novel_word_count + "字")
    for i in range(len(bili.novel_chapters)):
        if i == 0:
            print("0" + "\t" + "【下载全部】")
        print(str(i + 1) + "\t" + "【" + bili.novel_chapters[i] + "】")
    # print(bili.novel_chapter_detail)
    download_num = int(input("输入编号:"))
    bili.download_order(download_num)
