from flask import render_template,request
from app import app, db
from pyecharts import Bar, Pie,Line
import re


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/wel')
def welcome():
    """欢迎页面"""

    # 获取数据
    curse = db.find()
    data = list(curse)


    # 一共数据条数
    data_count = len(data)

    # 分类
    tencent =[]
    zhilian = []
    for d in data:
        if d['company'] == '腾讯':
            tencent.append(d)
        else:
            zhilian.append(d)

    # 腾讯招聘数
    tencent_count = len(tencent)
    # 智联招聘数
    zhilian_count = len(zhilian)

    # 获取ip
    ip = request.remote_addr


    context = {
        "data_count":data_count,
        "tencent":tencent_count,
        "zhilian":zhilian_count,
        "ip":ip,
    }



    return render_template('welcome.html',context=context)


@app.route('/list/<int:page>')
def list_data(page):
    """数据列表"""

    # 获取数据
    curse = db.find()
    data = list(curse)
    count = len(data)  # 获取数据总数

    # 分页
    list_data = data[page * 50:page * 50 + 50]
    page_count = count / 50

    context = {
        'data': list_data,  # 分页数据
        'count': count,  # 数据数量
        'page_num': page,  # 当前页码
        'page_count': int(page_count) - 1  # 页码总数
    }

    return render_template('admin-list.html', context=context)


# 工资
@app.route('/salary')
def salary():
    """计算工资分布"""
    # 获取数据
    curse = db.find({}, {"_id": 0, "salary": 1})
    data = list(curse)

    # 提取出工资
    salarys_temp = [i["salary"] for i in data if i['salary'] != '#' and i['salary'] != "薪资面议"]

    # 将工资转数字 4k-6k => 5k
    salarys = []
    for s in salarys_temp:
        # 用正则提取出数字部分
        l = re.findall(r'\d+\.?\d*', s)

        # 计算平均数
        sum = 0
        for i in l:
            sum += float(i)
        val = sum / len(l)

        salarys.append(val)  # 加入列表

    # 构建图表
    x = []  # x轴
    y = []  # y轴

    # 先构建一个字典 {“2k以下”:出现次数，。。。。。}
    result = {'2k以下': 0, '2k-4k': 0, '4k-6k': 0, '6k-7k': 0, '7k-10k': 0, '10k-15K': 0, "15K以上": 0}

    # 根据salarys为字典加值
    for s in salarys:
        if s < 2:
            result["2k以下"] += 1
        elif s > 2 and s < 4:
            result["2k-4k"] += 1
        elif s >= 4 and s < 6:
            result["4k-6k"] += 1
        elif s >= 6 and s < 7:
            result["6k-7k"] += 1
        elif s >= 7 and s < 10:
            result["7k-10k"] += 1
        elif s >= 10 and s < 15:
            result["10k-15K"] += 1
        else:
            result["15K以上"] += 1

    for key, value in result.items():
        x.append(key)
        y.append(value)

    line = Line("薪资分布柱状图", title_color='blue',
              width=1200, height=600, background_color='white')

    line.add("职位数", x, y, mark_point=['max'], legend_text_color='red')

    line.render('app/templates/line.html')

    return render_template('line.html')


# 要求
@app.route('/level')
def level():
    """计算学历"""

    # 获取数据
    curse = db.find({}, {"_id": 0, "requirement": 1,"company":1})
    # data = list(curse)


    # 去掉腾讯的
    data = [i for i in curse if i['company'] != "腾讯" ]


    # 构建字典
    result = {}
    for d in data:
        result[d['requirement']] = result.get(d['requirement'],0) + 1


    # 构建x，y列表
    x = []
    y = []
    for key,value in result.items():
        x.append(key)
        y.append(value)



    pie = Pie("学历要求饼图",width=1200, height=600,title_color='blue')
    pie.add('学历要求', x, y, is_label_show=True)

    pie.render('app/templates/pie.html')

    return render_template('pie.html')


# 腾讯工作地点分布
@app.route('/workposition')
def tencentpost():
    """腾讯工作地点分布"""

    # 获取数据
    # 获取数据
    curse = db.find({}, {"_id": 0, "workposition": 1, "company": 1})


    # 取出腾讯的
    data = [i for i in curse if i['company'] == "腾讯"]



    # 构建字典
    result = {}
    for d in data:
        result[d['workposition']] = result.get(d['workposition'], 0) + 1

    # 构建x,y轴
    x = []
    y = []
    for key, value in result.items():

        x.append(key)
        y.append(value)



    bar = Bar("腾讯工作地点分布", width=1200, height=600)
    bar.add("职位数", x, y, mark_point=['max'], legend_text_color='red', is_datazoom_show=True)
    bar.render(path="app/templates/tencent.html")






    return render_template("tencent.html")




