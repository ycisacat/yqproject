#coding=utf-8
__author__ = 'yc'
from yqproject.settings import *
import re
import xlrd
# file = open(BASE_DIR+'/static/scripts/lineChart.js','r')
# new_file = open(BASE_DIR+'/static/scripts/linechart.js','w+')
# a=file.readlines()
# xaxis="['1.8','1.9','1.10','1.11','1.12','1.13','1.14','1.15','1.16','1.17','1.18','1.19','1.20','1.21','1.22','1.23','1.24','1.25','1.26','1.27','1.28','1.29','1.30']"
# yaxis=[]
# seris_data = "[12, 13, 10,6,3,5,11, 11, 15, 13, 12, 13, 10,6,3,5]"
# print type(a)
# a[40]=a[40].replace('xaxis',xaxis)
# a[72]=a[72].replace('seris_data',seris_data)
# for i in a:
#     # i=i.replace('\r\n','')
#     new_file.write(i)
#     print i

# event = '魏则西之死'
# re.compile(event)
# path_list = []
# for root, dir, file in os.walk('../documents/topic1'):
#         if "label_link.xls" in file:
#             path = os.path.join(root,'label_link.xls')
#             path_list.append(path)
#
# for i in path_list:
#     a = re.search(event,i)
#     if a is not None:
#         print i
#
# print BASE_DIR
# file_name = BASE_DIR+'/network/result/new_label_link.xls'
# data = xlrd.open_workbook(file_name)
# sheet1 = data.sheet_by_index(0)
# print sheet1.nrows

# a=({'topic':'aaa'},{'topic':'aaa'})
# for i in a:
#     print i['topic']

import datetime
a=datetime.datetime.now()
date = datetime.datetime.date(a)
time = datetime.datetime.replace(a,minute=0,second=0,microsecond=0)
print time
a=()
print len(a),type(a)

a=({'a':'a b c d'},)
for i in a:
    # print i
    a = i['a'].split(' ')
    print a

a='/home/yc/PycharmProjects/yqproject/topic/患癌老爸怕拖累家人留信出走女儿泪奔寻父/2016-06-04 16:09:58/new_label_lin'
b=a.replace('topic','doo')
print b
leader_list = ['a','b']
seg=','
print seg.join(leader_list)

from crawler.start_search import *
db = Database()
label_dir = '/topic/别传了！杨雷雷丢高考准考证是谣言！/2016-06-05 13:27:57/new_label_link.xls'
sna_dir ='sna/topic/别传了！杨雷雷丢高考准考证是谣言！/2016-06-05 13:27:57/SNA.png'
if os.path.exists(DOC_DIR+'/'+label_dir):
    print 'yes'
    leader = find_leader(label_dir)
    db.save_network_scale('tpM_DyOMhrQ8O', 'aaa', label_dir,sna_dir, leader)
    # db.save_increment(e_id, bid_comment,bid_forward, bid_like)
else:
    print 'no'

