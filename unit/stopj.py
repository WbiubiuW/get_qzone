#encoding=utf-8
import sys
sys.path.append("../")
import jieba
import jieba.posseg as pseg
from jieba import analyse
#加载停用词表
stop = [line.strip() for line in open('../dataFile/stop_words.txt',encoding='utf-8').readlines() ]
#导入自定义词典
jieba.load_userdict("../dataFile/userdict.txt")

# 读取文本
f = open('../dataFile/example.txt',encoding='utf-8')
s = f.read()
#s="朝鲜半岛西北部古元古代高温变质-深熔作用:宏观和微观岩石学以及锆石U-Pb年代学制约"

#分词
segs = jieba.cut(s, cut_all=False)
#print u"[精确模式]: ", "  ".join(segs)

#分词并标注词性
segs = pseg.cut(s)


final = ''
for seg ,flag in segs:
    #去停用词
    if seg not in stop:
       #去数词和去字符串
       if flag !='m' and flag !='x':
            #输出分词
            final +=' '+ seg
            #输出分词带词性
            # final +=' '+ seg+'/'+flag
print(final)
