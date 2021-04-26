 import pandas as pd
 import plotly.graph_objects as go

 df = pd.read_excel('/refineddata.xlsx')
 df = df[df['parts'] != 0]
aggregated = df.groupby('entreprises').agg(
    {   'parts' : sum ,
        'valeur' : sum , 
        'id' : "count" })
df2 = aggregated.sort_values('valeur', ascending= False)
df2 = df2.head(10)
colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

fig = go.Figure(data=[go.Pie(labels=df2.index,
                             values=df2['valeur'])])
fig.update_layout(
    title_text="Principales entreprises par sommes totales investies par les parlementaires",)
fig.update_traces( textinfo='value', textfont_size=15,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.show()
