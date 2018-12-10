#-*- encoding: utf-8 -*-
'''
str_util.py
Created on 2018/8/2815:12
Copyright (c) wangjie
'''
import re
def checkEndwith(url):
    if isinstance(url,str):
        if url.endswith('/'):
            return url[0:-1]
        else:
            return url
    else:
        return checkEndwith(str(url))

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

#词频统计
def wordcount(strlist):
    count_dict = {}
    # 如果字典里有该单词则加1，否则添加入字典
    if strlist:
        for str in strlist:
            if str in count_dict.keys():
                count_dict[str] = count_dict[str] + 1
            else:
                count_dict[str] = 1
        #按照词频从高到低排列
        count_list=sorted(count_dict.items(),key=lambda x:x[1],reverse=True)
        return count_list
    else:
        return ""

#任意符号分词
def split_punctuation(list_input):
    if list_input:
        pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
        test_text = " ".join(list_input)
        result_list = re.split(pattern, test_text)
        return result_list
    else:
        return None

#计算平均数
def averagenum(num_list):
    if len(num_list)>0:
        nsum = 0
        for i in range(len(num_list)):
            nsum += num_list[i]
        return nsum / len(num_list)
    else:
        return 0
#从字符串中获取数字，没有为None
def getNumberType(ss):
    if not ss:
        return None
    else:
        s = re.findall("\d+",ss)[0]
        return s


if __name__ == '__main__':
    wordcount("")