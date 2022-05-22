#!/usr/bin/env python
# coding: utf-8

# # 备注：f19011632詹康宁-月饼数据可视化分析

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import Series, DataFrame
import openpyxl
import seaborn as sns
import pyecharts.charts as pyc
import pyecharts.options as opts
# 作图的字体默认设置
fontdict = {'fontsize': 15,'horizontalalignment': 'center'}
import matplotlib
font = {'family': 'Microsoft Yahei'}
matplotlib.rc('font', **font)


# # 1.数据导入

# In[2]:


df = pd.read_excel("MoonData.xlsx",engine="openpyxl")


# In[3]:


df.head(2)


# # 2.数据可视化

# ## 2.1各省销售额

# In[4]:


result1 = df.groupby(by=[df['city']])['sales'].sum()
total_sales_city = list(result1)
city = list(result1.index)


# In[5]:


from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker

total_city = (
    Map()
    .add("销售额", [list(z) for z in zip(city,total_sales_city)], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各地区销售额",subtitle="按省汇总"),
        visualmap_opts=opts.VisualMapOpts(split_number=10, is_piecewise=True,pieces=[
        #不指定 max，表示 max 为无限大（Infinity）。
        {"min": 10000000},
        {"min": 1000000, "max": 9999999},
        {"min": 100000, "max": 999999},
        {"min": 10000, "max": 99999},
        {"min": 1000, "max": 9999},
         #不指定 min，表示 min 为无限大（-Infinity）
        {"max": 999}],    
        )
    )
)
total_city.render_notebook()


# >分析：其中广东的总销售额最大，为11570151元

# ## 2.2销售额前十店铺

# In[6]:


df2 = df
result4 = df2.groupby(by=[df['shop']])['sales'].sum()
result4 = Series.sort_values(result4)
result4 = result4.tail(10)
total_sales_shop = list(result4)
shop = list(result4.index)


# In[7]:


import pyecharts.options as opts
from pyecharts.charts import Pie

data_pair = [list(z) for z in zip(shop, total_sales_shop)]
data_pair.sort(key=lambda x: x[1])
shop_sales = (
    Pie(init_opts=opts.InitOpts(width="1600px", height="800px", bg_color="#2c343c"))
    .add(
        series_name="销售额",
        data_pair=data_pair,
        rosetype="radius",
        radius="50%",
        center=["50%", "50%"],
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="各个店铺销售额",
            pos_left="center",
            pos_top="20",
            title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(color="rgba(255, 255, 255, 0.3)"),
    ) 
)
shop_sales.render_notebook()


# >可以从图中看出，销售额前三的店铺分别是华美京东自营旗舰店、稻香村自营官方旗舰店、舌里京东自营旗舰店

# ## 2.3各种类月饼销售额

# In[8]:


result2 = df.groupby(by=[df['category']])['sales'].sum()
total_sales_category = list(result2)
category = list(result2.index)


# In[13]:


from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

total_category = (
     Bar()
    .add_xaxis(category)
    .add_yaxis("销售额",total_sales_category)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title="各种类月饼销售额"),
    )
     .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
    markpoint_opts=opts.MarkPointOpts(
    data=[
    opts.MarkPointItem(type_="max", name="最⼤值"),
    opts.MarkPointItem(type_="min", name="最⼩值"),
    ]))
)
total_category.render_notebook()


# >分析：可以看出，广式月饼的销售额最高，其次是苏式月饼和港式月饼,最大销售额6992，最小销售额2072

# ## 2.4各种类销量

# In[12]:


#利用销售额和单价计算出销量
df.eval('salesVolume = sales/price' , inplace=True)
df.head(2)


# In[13]:


result3 = df.groupby(by=[df['category']])['salesVolume'].sum()
total_salesVolume_category = list(result3)
category = list(result3.index)


# In[14]:


import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker


total_category_num = (
    Line()
    .add_xaxis(category)
    .add_yaxis("销量", total_salesVolume_category, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各种类月饼销量"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
    )
)
total_category_num.render_notebook()


# >分析：可以看出，广式月饼的销量最高，其次是苏式月饼

# # 3.数据大屏

# In[15]:


from pyecharts import options as opts
from pyecharts.charts import Bar,Map,Line, Page, Pie
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.faker import Faker


# In[16]:


def total_city()->Map:
    total_city = (
        Map()
        .add("销售额", [list(z) for z in zip(city,total_sales_city)], "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各地区销售额",subtitle="按省汇总"),
            visualmap_opts=opts.VisualMapOpts(split_number=10, is_piecewise=True,pieces=[
            #不指定 max，表示 max 为无限大（Infinity）。
            {"min": 10000000},
            {"min": 1000000, "max": 9999999},
            {"min": 100000, "max": 999999},
            {"min": 10000, "max": 99999},
            {"min": 1000, "max": 9999},
             #不指定 min，表示 min 为无限大（-Infinity）
            {"max": 999}],    
            )
        )
    )
    return total_city

def shop_sales()->Pie:
    shop_sales = (
    Pie(init_opts=opts.InitOpts(width="1600px", height="800px", bg_color="#2c343c"))
    .add(
        series_name="销售额",
        data_pair=data_pair,
        rosetype="radius",
        radius="50%",
        center=["50%", "50%"],
        label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="各个店铺销售额",
            pos_left="center",
            pos_top="20",
            title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
        )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(color="rgba(255, 255, 255, 0.3)"),
        ) 
    )
    return shop_sales

def total_category()->Bar:
    total_category = (
     Bar()
    .add_xaxis(category)
    .add_yaxis("销售额",total_sales_category)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title="各种类月饼销售额"),
        )
    )
    return total_category

def total_category_num()->Line:
	total_category_num = (
		Line()
		.add_xaxis(category)
		.add_yaxis("销量", total_salesVolume_category, is_smooth=True)
		.set_series_opts(
			areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
			label_opts=opts.LabelOpts(is_show=False),
		)
		.set_global_opts(
			title_opts=opts.TitleOpts(title="各种类月饼销量"),
			xaxis_opts=opts.AxisOpts(
				axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
				is_scale=False,
				boundary_gap=False,
			),
		)
	)
	return total_category_num


# In[17]:


page = Page(layout=Page.DraggablePageLayout, page_title="月饼数据可视化分析")
# 在页面中添加图表
page.add(
    total_city(),
    shop_sales(),
    total_category(),
    total_category_num(),)
page.render('test.html')


# In[ ]:




