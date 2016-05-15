# coding=utf-8

from django import forms
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from yuqing.jsondump import *
from yuqing.main_run import *
from crawler.class_event import *

# Create your views here.


def ajax_list(request):
    a = range(100)
    return JsonResponse(a, safe=False)


def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)


def homepage(request):
    data = dump_time_line()
    # print data
    # data = [{'topic':u'烧鸡公双方了时间','month':4L,'day':30L},{'topic':u'222','month':4L,'day':15L},{'topic':u'111','month':4,'day':1}]
    # data = [{'a':'aaa'},{'b':'bbb'}]
    return render_to_response('index.html', {'data': data})


class SearchForm(forms.Form):
    input_words = forms.CharField(max_length=100)


def network(request, event_id, ctime):
    # if request.method == 'POST':
    #     event_id = request.POST['event_id']
    #     ctime = request.POST['ctime']
    event = Event().get_topic(event_id)  # topic
    result = dump_force(event_id, ctime)
    scale = result[2]
    node_data = result[0]
    edge_data = result[1]
    leader = result[3]
    return render(request, 'network.html', {'scale': scale, 'node_data': node_data, 'edge_data': edge_data,
                                            'event': event['etopic'], 'leader': leader})

    # else:
    #     return HttpResponseRedirect('/linechart/')


def line_chart(request, topic=''):
    eid_tuple = ()
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            search_words = sf.cleaned_data['input_words']
            eid_tuple = Event().search_vague_topic(search_words)  # ({eid,etp},{})

        else:
            print 'invalid form'
    else :
        eid_tuple = Event().search_exact_topic(topic)

    if len(eid_tuple) == 0:
        return render_to_response('error.html')

    if len(eid_tuple) > 1:
        event_list = []
        for i in eid_tuple:
            event_list.append(i)
        return render(request, 'list.html', {'event_list': event_list})

    else:
        event_id = eid_tuple[0]['event_id']
        inc = Increment()
        rows = inc.get_data(event_id)
        event = Event().get_topic(event_id)
        topic_words = Content().get_keywords(event_id)
        cmt = inc.get_comment(event_id)
        rpt = inc.get_repost(event_id)
        lik = inc.get_like(event_id)
        cnt = Content().get_content(event_id)
        print 'eve', event_id, event
        xaxis = str(inc.time_list)
        yaxis = str(inc.scale_rate)
        seris_data = str(inc.scale_rate)
        if len(rows) == 0:
            default = True

        else:
            default = False
            old_file = open(BASE_DIR + '/static/scripts/lineChart.js', 'rw')
            new_file = open(BASE_DIR + '/static/scripts/line_chart.js', 'w+')
            rw = old_file.readlines()
            rw[40] = rw[40].replace('xaxis', xaxis)
            rw[71] = rw[71].replace('seris_data', seris_data)
            for i in rw:
                new_file.write(i)
        return render(request, 'lineChart.html',
                      {'default': default, 'event_id':event_id, 'event': event['etopic'], 'topic_words': topic_words['keywords'],
                       'cmt': cmt['comment_num'], 'rpt': rpt['repost_num'], 'lik': lik['like_num'],
                       'cnt': cnt['content']})
