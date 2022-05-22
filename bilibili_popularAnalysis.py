#!/usr/bin/env python
# coding: utf-8

# # 备注：f19011632詹康宁-bilibili_popular可视化分析

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


df = pd.read_excel("bilibili_popular.xlsx",engine="openpyxl")


# In[3]:


df.head(1)


# # 2.数据可视化

# ##  2.1播放量前十up主视频硬币数

# In[4]:


df1 = df
result1 = df.groupby(by=[df['up主']])['播放'].sum()
result1 = Series.sort_values(result1)
result1 = result1.tail(10)
playbackVolume = list(result1)
up_list = list(result1.index)


# In[5]:


result1 = df.groupby(by=[df['硬币']])['播放'].sum()
result1 = Series.sort_values(result1)
result1 = result1.tail(10)
coins_count = list(result1)


# In[6]:


from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

up_coins_count = (
     Bar()
    .add_xaxis(up_list)
    .add_yaxis("硬币数",coins_count)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title="f19011632詹康宁-播放量前十视频硬币数"),
    )
)
up_coins_count.render_notebook()


# >该图展示了播放量前十的视频的硬币数，以及相关up主

# In[7]:


import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker


up_playbackVolume = (
    Line()
    .set_global_opts(
        title_opts=opts.TitleOpts(title="f19011632詹康宁-播放量前十"),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category",axislabel_opts={"rotate":50}),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
    )
    .add_xaxis(xaxis_data=up_list)
    .add_yaxis(
        series_name="",
        y_axis=playbackVolume,
        symbol="triangle",
        label_opts=opts.LabelOpts(is_show=False),
    )
)
up_playbackVolume.render_notebook()


# >该图展示了播放量前十的视频,以及相关up主

# In[9]:


up_playbackVolume.overlap(up_coins_count)
up_playbackVolume.render_notebook()


# >从图中可以得知，可以初步得出结论，播放量高的视频，投币数一般也较高

# ## 2.2 播放量数据前10的分区

# In[31]:


result2 = df.groupby(by=[df['分区']])['播放'].sum()
result2 = Series.sort_values(result2)
result2 = result2.tail(10)
playbackVolume = list(result2)
part_list = list(result2.index)
result2


# In[32]:


playbackVolume 


# In[33]:


part_list


# In[34]:


from pyecharts import options as opts
from pyecharts.charts import Radar
part = (
    Radar()
    .add_schema(
        schema=[
            opts.RadarIndicatorItem(name='游戏', max_=3000000000),
            opts.RadarIndicatorItem(name='生活', max_=3000000000),
            opts.RadarIndicatorItem(name='动画', max_=3000000000),
            opts.RadarIndicatorItem(name="音乐", max_=3000000000),
            opts.RadarIndicatorItem(name='影视', max_=3000000000),
            opts.RadarIndicatorItem(name='美食', max_=3000000000),
            opts.RadarIndicatorItem(name='咨讯', max_=3000000000),
            opts.RadarIndicatorItem(name="舞蹈", max_=3000000000),
            opts.RadarIndicatorItem(name="知识", max_=3000000000),
            opts.RadarIndicatorItem(name='鬼畜', max_=3000000000),
        ]
    )
    .add("分区播放量",[[231506191,248872047,817506202,823588622,832529098,940589461,988664180,1717922975,1849951264,2934458139]])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        legend_opts=opts.LegendOpts(selected_mode="single"),
        title_opts=opts.TitleOpts(title="15个分区总播放量数据"),
    )
)
part.render_notebook()


# >从图中可以看出，分区播放量前三的分别是鬼畜区、知识区、舞蹈区

# # 3.数据大屏

# In[39]:


def up_coins_count()->Bar:
    up_coins_count = (
         Bar()
        .add_xaxis(up_list)
        .add_yaxis("硬币数",coins_count)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            title_opts=opts.TitleOpts(title="播放量前十视频硬币数"),
        )
    )
    return up_coins_count
def up_playbackVolume()->Line:
    up_playbackVolume = (
        Line()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="播放量前十"),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category",axislabel_opts={"rotate":50}),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        )
        .add_xaxis(xaxis_data=up_list)
        .add_yaxis(
            series_name="",
            y_axis=playbackVolume,
            symbol="triangle",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    return up_playbackVolume

def part()->Radar:
    part = (
        Radar()
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name='游戏', max_=3000000000),
                opts.RadarIndicatorItem(name='生活', max_=3000000000),
                opts.RadarIndicatorItem(name='动画', max_=3000000000),
                opts.RadarIndicatorItem(name="音乐", max_=3000000000),
                opts.RadarIndicatorItem(name='影视', max_=3000000000),
                opts.RadarIndicatorItem(name='美食', max_=3000000000),
                opts.RadarIndicatorItem(name='咨讯', max_=3000000000),
                opts.RadarIndicatorItem(name="舞蹈", max_=3000000000),
                opts.RadarIndicatorItem(name="知识", max_=3000000000),
                opts.RadarIndicatorItem(name='鬼畜', max_=3000000000),
            ]
        )
        .add("分区播放量",[[231506191,248872047,817506202,823588622,832529098,940589461,988664180,1717922975,1849951264,2934458139]])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(selected_mode="single"),
            title_opts=opts.TitleOpts(title="15个分区总播放量数据"),
        )
    )
    return part


# In[41]:


from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie
page = Page(layout=Page.DraggablePageLayout, page_title="bilibili_popular可视化分析")
# 在页面中添加图表
page.add(
    up_coins_count(),
    up_playbackVolume(),
    part(),)
page.render('bilibili_popular数据大屏.html')


# In[ ]:




