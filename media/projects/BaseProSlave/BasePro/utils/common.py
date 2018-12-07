# -*- coding:utf-8 -*-
# Author : oldman
# License : (C) Copyright 2015-2017, minivision
import re
import pymongo

def get_num(strs):
    num = re.match('.*?(\d+).*',strs).group(1)
    return num


def get_all_num(s):
    sl = list(s)
    num = []
    for s in sl:
        if s.isdigit() or s == '(' or s == ')':
            num.append(s)
    num = ''.join(num)
    return num


def get_name():
    namelist = []
    # name3list = []
    with open('name.txt','r') as f:
        for index,name in enumerate(f.read().split('#')):
                namelist.append(name.strip())
        namelist[0] = '杨朝来'


    name500list = []
    with open('name500.txt','r') as f:
        for name in f.readlines():
            # print(name.strip())
            name500list.append(name.strip())
        name500list[0]='张伟'

    names = name500list + namelist
    return names


# 检查字符串中是否有数字
def has_num(instr):
    return any(i.isdigit() for i in instr)


def get_url_from_mongo():
    #
    client = pymongo.MongoClient('localhost', 27017)
    db = client['comp_tel']
    col = db['info_temp']
    url = col.find()
    return url

# for url in get_url_from_mongo()[0:100]:
#     print(url['comp_page'])

# 替换html标签
##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s

##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}

    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s,re_exp,repl_string):
    return re_exp.sub(repl_string,s)

def screenshot_ele(driver,ele_id,img_name):
    from PIL import Image
    driver.save_screenshot(img_name)
    element = driver.find_element_by_id(ele_id)

    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']

    im = Image.open(img_name)
    im = im.crop((left, top, right, bottom))
    im.save(img_name)



if __name__=='__main__':
    # news=filter_tags(s)
    # print(news)
    pass