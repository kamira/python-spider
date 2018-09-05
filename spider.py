import requests, re, os, json, codecs, datetime
# from selenium import webdriver
from bs4 import BeautifulSoup

# 篩選字串
pattern = re.compile(r"資安|入侵|漏洞")
pattern_date = re.compile(r"[0-9]{4}")
pattern_cont = re.compile(r"\<p\>")
items_Tag = ".channel-item"
title_Tag = ".title"
summary_Tag = ".summary"
content_Tag = ".even"

title_Text = ""
summary_Text = ""
content_Text = ""


url = "https://www.ithome.com.tw"
url_sec = "https://www.ithome.com.tw/security"
res = requests.get(url_sec)

soup = BeautifulSoup(res.text, "lxml")

Json_data = {}
Json_data[1] = []

for item in soup.select(items_Tag):
    item_Text = item.get_text()
    # 篩選是否含有關鍵字
    if pattern.search(item_Text):

        # 標題擷取
        title = item.select(title_Tag)[0]
        title_Text = str(title.get_text())

        # 擷取內文連結
        content_url = url + title.a.get('href')

        # 摘錄擷取
        summary_Text = item.select(summary_Tag)[0].get_text()

        # 內容擷取
        if not pattern_date.search(summary_Text):
            res_content = requests.get(content_url)
            soup_content = BeautifulSoup(res_content.text, 'lxml')
            contents = soup_content.select(content_Tag)
            content_Text = ""

            for i in range(len(contents)):
                if len(pattern_cont.findall(str(contents[i]))) > 3:
                    content_Text = content_Text + str(contents[i]).replace("\n","")
            content_Text = content_Text + "<p>資料來源 : <a href='" + str(content_url) + "'>" + str(title_Text) + "</a></p>"
            Json_data[1].append({"Title": title_Text, "Summary" : str(summary_Text), "Content" : str(content_Text), "URL" : str(content_url)})

print(Json_data)
with codecs.open("WebSpider-ithome-" + datetime.date.today().strftime("%Y%m%d") + ".json", "w", "utf-8") as fp:
    json.dump(Json_data, fp)
