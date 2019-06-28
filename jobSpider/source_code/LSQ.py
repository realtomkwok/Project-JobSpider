from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid
import pandas as pd 

def LSQ1(lang) -> Bar:
    language = "data/ZQF/"+lang+".xlsx"
    df = pd.read_excel(language)
    data = df.groupby(['city', 'experience']).avgWage.mean().round(2).reset_index(name='salary')

    shanghai = list(data.query("city=='上海'").salary)
    beijing = list(data.query("city=='北京'").salary)
    guangzhou = list(data.query("city=='广州'").salary)
    shenzhen = list(data.query("city=='深圳'").salary)

    bar = (
        Bar()
        .add_xaxis(['1-5年', '10年以上', '5-10年', '不限'])
        .add_yaxis('上海', shanghai)
        .add_yaxis('北京', beijing)
        .add_yaxis('广州', guangzhou)
        .add_yaxis('深圳', shenzhen)
        .set_global_opts(title_opts={"text": lang, "subtext": "工资与经验关系图"})
    )
    return bar
