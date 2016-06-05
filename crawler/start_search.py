# coding=utf-8
from pack_tbw import *
from search_topic import SearchTopic as st
import shutil
from interface import *
from network.main import *
import xlrd
from class_headhunter import *

__author__ = 'gu'
"""
5.28 测试完毕
"""


def muL_ss():
    """
    多进程进行开始搜索搜索，多进程调用start_search
    :return:
    """
    print 'adfassss'
    threads = []

    sd = SaveData()

    sd.interface_content()
    sd.interface_event()
    sd.interface_participate()

    tbw_dict = sd.get_pack_dict()

    # search_process = multiprocessing.Process()
    # {bid1:[(title1,blog1,word1),(title2,blog2,word2)], bid2:[(title4,blog4,word4),(title5,blog5,word5)]}
    for (bid, tbw_list) in tbw_dict.items():
        search_process = multiprocessing.Process(target=start_search, args=(bid, tbw_list))  # 一个bid作为一个进程搜索
        search_process.start()
    # print search_process
    # search_process.join()
        threads.append(search_process)

    for j in range(len(threads)):
        threads[j].join()

def start_search(bid, tbw_list):
    """
    经过聚类后便可以开始搜索， 进行st().search_topic搜索，生成文件夹，如果不是热点的话题，便删除文件夹
    :param bid: 每一个类的代表博文id
    :param tbw_list: 这个类的博文相关属性的组合， [(title1,blog1,word1),(title2,blog2,word2)]
    :return:
    """
    db = Database()
    eve = Event()
    con = Content()
    e_id = 'tp' + bid
    short_dir = create_time_file(tbw_list[0][0])  # 创建标题文件夹
    corpus_dir = DOC_DIR + '/' + short_dir + 'uid=' + str(bid) + '.txt'
    print "生成的动态目录：", corpus_dir
    txt_file = open(corpus_dir, 'w+')

    bid_like = 0  # 该bid类的点赞规模
    bid_forward = 0
    bid_comment = 0

    for tbw_tuple in tbw_list:  # [(title1,blog1,word1),(title2,blog2,word2)]
        print bid, "类的博文标题, 博文, 关键词", tbw_tuple[0], tbw_tuple[1], tbw_tuple[2]

        total_result_list, total_reason_list, lfc_all_num = st().search_topic(bid, tbw_tuple)

        # total_result_list = [[博文id,博文时间,标题,博文,关键词,首发者的id,首发者的名字,点赞,转发,评论,origin], ]
        for com_index in range(len(total_result_list)):
            for com in total_result_list[com_index]:
                txt_file.write(str(com) + '\n')

            # total_reason_list = [[古阿陌@洗洗睡@人民日报, 南方报@人民日报, yutsfa@人民日报 ], ]
            for reason in total_reason_list[com_index]:
                print "转发理由：", reason
                txt_file.write(str(reason) + '\n')
            txt_file.write('\n')
        txt_file.write('\n\n\n--------------------\n')

        # lfc_all_num = [该话题的点赞规模,该话题的转发规模,该话题的评论规模]
        print '*******************************'
        print "该话题的点赞规模", lfc_all_num[0]
        print "该话题的转发规模", lfc_all_num[1]
        print "该话题的评论规模", lfc_all_num[2]

        bid_like += int(lfc_all_num[0])
        bid_forward += int(lfc_all_num[1])
        bid_comment += int(lfc_all_num[2])

    print tbw_list[0][0], '聚合的类的话题规模', bid_like, bid_forward, bid_comment

    txt_file.write(str(bid_like) + '\n' +
                   str(bid_forward) + '\n' +
                   str(bid_comment) + '\n')
    txt_file.close()
    if bid_like + bid_forward + bid_comment == 0:
        deleted_dir = DOC_DIR + '/' + 'topic' + '/' + tbw_list[0][0]
        pic_dir = deleted_dir.replace('documents','static/sna')
        print "不是热点的文件夹删除", deleted_dir
        shutil.rmtree(deleted_dir)
        shutil.rmtree(pic_dir)
        eve.delete_event(e_id)

    else:

        # now = datetime.datetime.now()
        # other_style_time = now.strftime("%Y-%m-%d %H:%M:%S")

    #  存 interface_networkscale()和increment:
        main_network()
        corpus_dir = short_dir + 'uid=' + str(bid) + '.txt'
        label_dir = short_dir + 'new_label_link.xls'
        sna_dir = 'sna/'+ short_dir + 'SNA.png'
        print 'label!!!!!!', DOC_DIR+'/'+label_dir
        if os.path.exists(DOC_DIR+'/'+label_dir):
            print 'yep'
            leader = find_leader(label_dir)
            db.save_network_scale(e_id, corpus_dir, label_dir,sna_dir, leader)
            db.save_increment(e_id, bid_comment,bid_forward, bid_like)
        else:

            label_dir = 'None'
            sna_dir = 'None'
            leader = 'Unknown'
            db.save_network_scale(e_id, corpus_dir, label_dir,sna_dir, leader)
            db.save_increment(e_id, bid_comment,bid_forward, bid_like)
        print "storing!!!"


def find_leader(lbdir):
    """
    读label找出核心人物
    :param lbdir: label dir
    :return: 核心人物
    """
    leader_list = []
    file_name = DOC_DIR + '/' + lbdir
    print 'find leader', file_name
    # file_name = BASE_DIR+'/network/result/new_label_link.xls'

    data = xlrd.open_workbook(file_name)
    sheet1 = data.sheet_by_index(0)
    value_list = sheet1.col_values(2,1)
    for i in range(0, len(value_list)):
        if value_list[i]>2:
            name = sheet1.cell_value(i+1,1).encode('utf-8')
            leader_list.append(name)
            uid = get_uid_by_name(name)
            if uid is not None:
                Sina('rmrb').process_control(uid)
            else:
                print '无法获取',name,'用户的信息'

    if len(leader_list) == 0:
        return 'Unknown'
    else:
        seg=','
        return seg.join(leader_list)

def get_uid_by_name(name):
    header = {'User-Agent': 'Mozilla/' + str(
            float(int(random.uniform(1, 6)))) + '(X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/' + str(
            float(int(random.uniform(29, 36))))}
    pageurl = 'http://weibo.cn/search/user?keyword=' + str(urllib2.quote(name))
    req = urllib2.Request(url=pageurl, headers=header)
    content = urllib2.urlopen(req).read()
    print content
    # content ='首页<span class="tk">!</span></a>|<a href="http://weibo.cn/msg/?tf=5_010" class="nl">消息</a>|<a href="http://huati.weibo.cn" class="nl">话题</a>|<a href="http://weibo.cn/search/?tf=5_012" class="nl">搜索</a>|<a href="/search/?keyword=%E5%8C%97%E6%96%B9&amp;suser=%E6%89%BE%E4%BA%BA&amp;rand=8409&amp;p=r" class="nl">刷新</a></div><div class="c"><form action="/search/" method="post"><div><input type="text" name="keyword" value="北方" /><input type="submit" name="suser" value="找人" /></div></form></div><div class="c"><span class="cmt">共500条</span></div><div class="tip">类型:全部-<a href="/search/user/?keyword=%E5%8C%97%E6%96%B9&amp;filter=stag">标签</a>-<a href="/search/user/?keyword=%E5%8C%97%E6%96%B9&amp;filter=isv">认证</a>-<a href="/search/user/?keyword=%E5%8C%97%E6%96%B9&amp;advanced=user&amp;rl=1">更多&gt;&gt;</a><br/>排序:全部-<a href="/search/user/?keyword=%E5%8C%97%E6%96%B9&amp;sort=0">粉丝数</a></div><table><tr><td valign="top"><a href="/234779216?f=search_0"><img src="http://tva2.sinaimg.cn/crop.0.0.179.179.50/40a34a3ajw1eveuyfmdu6j2050050aad.jpg" alt="pic" /></a></td><td valign="top"><a href="/234779216?f=search_0">新北方官方微博</a><img src="http://h5.sinaimg.cn/upload/2016/05/26/319/5337.gif" alt="V"/><br/>粉丝529324人&nbsp;辽宁 沈阳<br/><a href="/attention/add?uid=1084443194&amp;rl=1&amp;st=abb783">关注她</a></td></tr></table><div class="s"></div><table><tr><td valign="top"><a href="/jinxia0802?f=search_1"><img src="http://tva2.sinaimg.cn/crop.0.0.757.757.50/471397c5jw8eijps7akbmj20l10l2q41.jpg" alt="pic" /></a></td><td valign="top"><a href="/jinxia0802?f=search_1">新北方金霞</a><img src="http://h5.sinaimg.cn/upload/2016/05/26/319/5338.gif" alt=/haiwainet?f=search_2"><img src="htt'
    pattern = re.compile('<table><tr>(.*?)<a href="/(.*?)\?f=search_0">')
    result = re.search(pattern, content)
    if result != None:
        uid = result.group(2)
        print 'UID!!!!', uid
        return uid
    else:
        return None

# get_uid_by_name('新北方官方微博')