from pyecharts import options as opts
from pyecharts.charts import Radar
from pyecharts.commons.utils import JsCode

captain_america = [{"value": [4, 4, 4, 4, 1, 7], "name": "美国队长"}] #每个超级英雄的战斗力数值
iron_man= [{"value": [6, 3, 5, 3, 5, 3], "name": "钢铁侠"}]
black_widow = [{"value": [3, 3, 2, 3, 2, 7], "name": "黑寡妇"}]
hawkeye = [{"value": [3, 3, 3, 2, 3, 7], "name": "鹰眼"}]
hulk = [{"value": [2, 7, 3, 7, 1, 3], "name": "绿巨人"}]
thor =  [{"value": [2, 7, 6, 7, 7, 6], "name": "雷神"}]

myschema = [
    {"name": '智力', "max": 7, "min": 0},
    {"name": '力量', "max": 7, "min": 0},
    {"name": '速度', "max": 7, "min": 0},
    {"name": '耐力', "max": 7, "min": 0},
    {"name": '能量发射', "max": 7, "min": 0},
    {"name": '战斗技能', "max": 7, "min": 0}
] #设置雷达图的属性
r = Radar(init_opts=opts.InitOpts(
            bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}
        )
) #初始化雷达图
r.add_js_funcs(
    """
    var img = new Image(); img.src = 'a5.png';
    """
) #执行js代码

(
    r.add_schema(
        schema=myschema,
        shape="circle", #图片形状
        center=["50%", "50%"], #图片中心位置
        radius="80%", #图片半径大小
        angleaxis_opts=opts.AngleAxisOpts(
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
        radiusaxis_opts=opts.RadiusAxisOpts(
            min_=0,
            max_=7,
            interval=1,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            splitline_opts=opts.series_options.SplitLineOpts(is_show=True, linestyle_opts={'color':'grey','opacity':0.8})   
            
        ),
        polar_opts=opts.PolarOpts(),
        splitline_opt=opts.SplitLineOpts(is_show=False),
        textstyle_opts=opts.TextStyleOpts(color="black"),
    )
    .add(
        series_name="美国队长",
        data=captain_america,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
    )
    .add(
        series_name="钢铁侠",
        data=iron_man,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
    )
    .add(
        series_name="黑寡妇",
        data=black_widow,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
    )
    .add(
        series_name="鹰眼",
        data=hawkeye,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
    )
    .add(
        series_name="绿巨人",
        data=hulk,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
    )
    .add(
        series_name="雷神",
        data=thor,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="复联六巨头实力对比"), legend_opts=opts.LegendOpts()
    )
    .render('ht1.html') #生成网页
)
