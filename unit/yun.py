import jieba
import jieba.posseg as pseg
from wordcloud import WordCloud
from PIL import Image
from PIL import ImageFont
import numpy as np

#字体
font = '../resource/simfang.ttf'

def stop_works():
    # 加载停用词表
    stop = [line.strip() for line in open('../dataFile/stop_words.txt', encoding='utf-8').readlines()]
    # 导入自定义词典
    jieba.load_userdict("../dataFile/userdict.txt")

    # 读取文本
    f = open('../dataFile/shuoshuo.txt', encoding='utf-8')
    s = f.read()

    # 分词
    segs = jieba.cut(s, cut_all=False)
    # print u"[精确模式]: ", "  ".join(segs)

    # 分词并标注词性
    segs = pseg.cut(s)

    final = ''
    for seg, flag in segs:
        # 去停用词
        if seg not in stop:
            # 去数词和去字符串
            if flag != 'm' and flag != 'x':
                # 输出分词
                final += ' ' + seg
                # 输出分词带词性
                # final +=' '+ seg+'/'+flag
    return final

def worksYun(msg):
    img = Image.open('../image/22.jpg')  # 以什么图片进行显示
    img_array = np.array(img)  # 将图片转换为数组

    wc = WordCloud(
        background_color='white',
        mask=img_array,  # 若没有该项，则生成默认图片
        font_path=font  # 中文分词必须有中文字体设置
    )
    wc.generate_from_text(msg)  # 绘制图片
    wc.to_file('../image/new.png')  # 保存图片

msg = stop_works()
worksYun(msg)