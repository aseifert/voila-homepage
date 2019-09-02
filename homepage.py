# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + {"Collapsed": "false"}
import ipyvuetify as v
import scrapbook as sb
import yaml
from pathlib import Path

# + {"Collapsed": "false"}
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

dashboard_name  = config.get('title', '')
server_url      = config.get('server_url', 'http://localhost:8866')
voila_nb_path   = Path(config.get('voila_nb_path', '.'))
title_bar_color = config.get('title_bar_color', 'orange')
voila_base_url  = server_url + '/voila/render/'

logo = { 'jupyter': 'https://jupyter.org/assets/nav_logo.svg' }

# + {"Collapsed": "false"}
app_bar_links = [
    v.Btn(children=[name], flat=True, href=link, target='_blank')
    for name, link in config.get('app_bar_links', {}).items()
]

# + {"Collapsed": "false"}
filelist = {}

stages = [p for p in voila_nb_path.glob('*') if p.is_dir() and not str(p).startswith(".")]

for stage in stages:
    files = stage.glob("*.ipynb")

    items = []
    for f in files:
        this_item = {}
        this_item['title'] = f.name
        this_item['description'] = 'A Jupyter Notebook.'
        this_item['link'] = voila_base_url + str(f)
        this_item['logo'] = 'https://jupyter.org/assets/nav_logo.svg'
        this_item['fname'] = str(f)

        nb = sb.read_notebook(str(f))
        for key, value in nb.scraps.data_dict.items():
            this_item[key] = value
        items.append(this_item)

    filelist[stage.name] = items


# + {"Collapsed": "false"}
# build toolbar
toolbar = v.Toolbar(color=title_bar_color, dark=True, children=[
    v.ToolbarItems(children=[v.Img(src=logo['jupyter'], style_='height:100%')]),
    v.ToolbarTitle(children=[dashboard_name], color='green'),
    v.Spacer(),
    v.ToolbarItems(children=app_bar_links)
], app=True)

# + {"Collapsed": "false"}
tab_children = []

for stage in sorted(filelist.keys()):
    items = filelist[stage]
    cards = [
        v.Flex(ma_2=True, fluid=True, children=[
            v.Card(hover=True,
                   align_center=True,
                   fluid=True,
                   min_width='300px',
                   max_width='300px',
                   href=details['link'],
                   target='_blank',
                   children=[
                       v.CardTitle(children=[
                           v.Html(tag='div', class_='headline mb-0', children=[details['title']]),
                           v.Spacer(),
                       ]),
                       v.CardText(children=[details['description']]),
                   ])
        ])
        for i, details in enumerate(items)
    ]

    tab_children.append(v.Tab(children=[stage]))
    tab_children.append(v.TabItem(children=[v.Layout(ma_5=True, wrap=True, children=cards)]))


# + {"Collapsed": "false"}
tabs = v.Tabs(v_model='tab', color='grey lighten-5', fixed_tabs=True, children=tab_children)

app = v.App(
    style_="background: white",
    children=[
        toolbar,
        v.Container(fluid=True, mt_3=True, children=[
            v.Layout(children=[
                v.Flex(children=[tabs])
            ])
        ])
    ]
)

# + {"Collapsed": "false"}
app

# + {"Collapsed": "false"}

