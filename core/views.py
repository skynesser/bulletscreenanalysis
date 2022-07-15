from django.shortcuts import render, HttpResponse
import csv
import os
import shutil
import re
import requests
import csv
import jieba
from itertools import islice
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud


def get_html(url, header):
    r = requests.get(url, headers=header)
    r.encoding = 'utf-8'
    return r.text


def danmu_spider(r_text, url, header):
    count = 1
    f = open('data\cav_file.csv', 'w', encoding='utf-8', newline="")
    csv1_write = csv.writer(f)
    csv1_write.writerow(['time', 'danmu'])

    f1 = open('data\csv_file.csv', 'w', encoding='utf-8', newline="")
    csv2_write = csv.writer(f1)

    # 清空ca文件夹，若不存在则创建
    filepath = 'data\detail'
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

    txt1 = get_html(url, header)
    pat = '"cid":(\d+)'
    chapter_temp = re.findall(pat, txt1)[1:-2]
    chapter_total = set(chapter_temp)  # 去重
    for chapter in chapter_total:
        path = 'data\detail\cav{}_file.csv'.format(count)
        f = open(path, 'w', encoding='utf-8', newline="")
        csv_write = csv.writer(f)
        csv_write.writerow(['time', 'danmu'])

        url1 = 'http://comment.bilibili.com/{}.xml'.format(chapter)
        txt2 = get_html(url1, header)
        data = re.compile('<d p="(.*?),.*?>(.*?)</d>')
        data2 = re.compile('<d p=".*?,.*?>(.*?)</d>')
        danmu_total = data.findall(txt2)
        for danmu in danmu_total:
            csv_write.writerow(danmu)
            csv1_write.writerow(danmu)

        csv2_write.writerow(data2.findall(txt2))
        # print(danmu)
        count += 1
        f.close()
    # print(chapter_total)


def index(request):
    return render(request, 'core/index.html')


def spider(request):
    url = request.POST.get('BV_ID')
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.2242 SLBChan/101'}
    r_text = get_html(url, header)
    danmu_spider(r_text, url, header)

    return render(request, 'core/detail.html')


def analysis(request):
    csv_file = open('data/cav_file.csv', encoding='utf-8')
    csv_reader_lines = csv.reader(csv_file)
    stopwords = [line.strip() for line in open('data/stopwords.txt', 'r', encoding='utf-8').readlines()]
    comment = {}
    for line in islice(csv_reader_lines, 1, None):
        poss = jieba.cut(line[1])
        for word in poss:
            if word in stopwords or len(word) < 2:
                continue
            if comment.get(word) is None:
                comment[word] = 0
            else:
                comment[word] += 1
    comment = dict(sorted(comment.items(), key=lambda x: x[1], reverse=True))
    count = 1
    comment_count = []
    for key, value in comment.items():
        comment_count.append([key, value])
        count += 1
        if count == 11:
            break
    comment_count = pd.DataFrame(comment_count, columns=['words', 'counts'])
    print(comment_count)

    plt.figure(figsize=(10, 6))
    plt.bar(comment_count['words'], comment_count['counts'], alpha=0.7, label='次数')
    for name, count in zip(comment_count.index, comment_count['counts']):
        plt.text(name, count + 5, count, ha='center', va='bottom')
    plt.title('评论高频词分布情况')
    plt.xlabel('高频词')
    plt.ylabel('次数')
    plt.legend(loc='upper right')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.savefig(r"core/static/core/word.jpg")
    plt.show()

    data = pd.read_csv('data/cav_file.csv', encoding="utf-8")
    data = data.sort_values('time')

    # 先对弹幕发送时间进行取整
    data['time'] = [int(item) for item in data.time]
    data = data.groupby('time').size().reset_index(name="counted")

    list2 = [item for item in data.time]
    data_sum = [item for item in data.counted]
    matplotlib.rcParams["font.family"] = "SimHei"
    plt.plot(list2, data_sum)
    plt.ylabel("弹幕数量")
    plt.xlabel("视频时间轴/(秒)")
    plt.title("弹幕密度变化图")
    plt.savefig(r"core/static/core/draw.jpg")
    plt.show()




def word_generate(r):
    with open('data/csv_file.csv', 'r', encoding="UTF-8") as f:  # 随便找了文件夹里一集爬的，关键词相对准确一点
        file = f.read()
    data_cut = jieba.cut(file, cut_all=False)
    stop_words = ["，", "。", ";", "、", "哈哈"]
    stop_words = []
    with open("data/stopwords.txt", 'r', encoding='utf-8') as f:
        for line in f:
            if len(line) > 0:
                stop_words.append(line.strip())
                data_result = [i for i in data_cut if i not in stop_words]
                result2txt = str(data_result)  # data是前面运行出的数据，先将其转为字符串才能写入
                # with open('out.txt','a',encoding='utf-8') as file_handle:
                #     file_handle.write("{}\n".format(data_result))     # 检查分词用的代码，输出分词到out.txt
                text = " ".join(data_result).replace("\n", "")  # txt形式存储处理过的数据，方便词云生成
                # with open('out1.txt','a',encoding='utf-8') as file_handle:
                #     file_handle.write("{}\n".format(data_result))     # 同检查分词用的代码
                wc = WordCloud(font_path="STXIHEI.TTF", background_color="white", max_words=5000, max_font_size=50,
                               scale=6, )
                try:
                    wc.generate(text)
                    plt.imshow(wc)
                    plt.axis("off")
                    plt.savefig(r'core/static/core/wordcloud.jpg')
                except:
                    pass



def detail(request):
    # spider(request)
    # word_generate(request)
    analysis(request)
    return render(request, 'core/detail.html')
