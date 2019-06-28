
from random import randrange
from flask import Flask, render_template,url_for, request, json,jsonify
from pyecharts import options as opts
from pyecharts.charts import Funnel, WordCloud
import pandas as pd



app = Flask(__name__, static_folder="templates")
app.config['JSON_AS_ASCII'] = False

def funnel_base(lang) -> Funnel:
    df = pd.read_excel("data/ZLQ/position.xlsx",sheet_name=lang)

    df_C = df.groupby('position').size().reset_index(name="count").sort_values(by="count",ascending= False).iloc[:10]#sort_values(by="count")  
    proportion = ((df_C['count']/df.shape[0])*100).apply(lambda x: format(x, '.2')) 
    df_C['proportion'] = proportion
    
    proportions = list(df_C['proportion'])
    positions = list(df_C['position'])
    df_C.reset_index(drop = True)
    
    data = [[positions[i],proportions[i]] for i in range(len(positions))]    
    funnel = (
       Funnel()
        .add(
            series_name=lang,
            data_pair=data,
            gap=2,
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
            itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
            )
        .set_global_opts(title_opts=opts.TitleOpts(title="{}岗位热门关键词Top10".format(lang)),
                         toolbox_opts=opts.ToolboxOpts(),
                         legend_opts=opts.LegendOpts(is_show=False), 
                        )
        )
    return funnel

def wordcloud_base(lang) -> WordCloud:
    DF = pd.read_excel("data/ZLQ/Lagou.xlsx",sheet_name=lang)
    
    DF_= DF.groupby('split').size().reset_index(name="count").sort_values(by="count",ascending= False).iloc[:10].reset_index(drop = True)
    proportion = ((DF_['count']/DF.shape[0])*100).apply(lambda x: format(x, '.3'))
    DF_['proportion'] = proportion
    
    splits = list(DF_['split'])
    nums = list(DF_['proportion'])
    C_cloud = []
    for i in range(10):
        C_cloud.append((splits[i],nums[i]))
       
    wordcloud = (
        WordCloud()
        .add(lang, C_cloud,
             word_size_range=[20, 150],
             shape="circle",
             )
        .set_global_opts(title_opts=opts.TitleOpts(title="{}热门应用领域".format(lang)),
                         )
    )
    return wordcloud

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/funnelChart",methods=[ 'POST'])
def get_funnel_chart():
    if request.method == "POST":
        lang = request.form.get('lang', '')   
    print(lang)
    c = funnel_base(lang)
    return c.dump_options()

@app.route("/wordcloudChart",methods=[ 'POST'])
def get_wordcloud_chart():
    if request.method == "POST":
        lang = request.form.get('lang', '')
    
    d = wordcloud_base(lang)  
   # print(d.dump_options())
    return d.dump_options()
  
if __name__ == "__main__":
    app.run()
