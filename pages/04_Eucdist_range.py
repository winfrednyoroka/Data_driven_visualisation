# Loading libraries
import streamlit as st
import pandas as pd 
import numpy as np 
#import scipy
import altair as alt 

st.title('Merged Eucdist and Scenario Range')
# Read in both datasets

# Range dataset
range_df = pd.read_csv('Data/BMI_DBP_scenariorange.csv')
result_df = pd.read_csv('Data/DBP_baseline_normalizedeucdist.csv')

# Combine the two datasets for visualisation on column 'Author_pmid'
st.dataframe(range_df)
st.dataframe(result_df)

df = pd.merge(range_df,result_df, on ='Author_pmid')
st.dataframe(df)
# Manipulate the data before plotting to rename some columns
df.loc[df['Author_pmid']=='Ospanov_33963974_a','lname']=df['lname']+'_a'
df.loc[df['Author_pmid']=='Ospanov_33963974_b','lname']=df['lname']+'_b'
df.loc[df['Author_pmid']=='Tur_23163735_a','lname']=df['lname']+'_a'
df.loc[df['Author_pmid']=='Tur_23163735_b','lname']=df['lname']+'_b'
st.dataframe(df)
# Download the data for further analysis
rounded_df =df.round(4)
csv = rounded_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download data as CSV",
    data=csv,
    file_name='BMI_DBP_range_eucdist.csv',
    mime='text/csv',
)

# Visualise using a scatter plot

P = alt.Chart(df).encode(
    alt.X('standardizedeucl_dist',
          title='Standardized Euclidean distance at baseline)',
          scale=alt.Scale(zero=False, domain=[0, 2.5])),
    alt.Y('DBP_scenariorange',
          title='Scenario Range',
          scale=alt.Scale(zero=False, domain=[0, 30])),
    color=alt.Color('Author_pmid:N'),
        # .scale(domain=['Control', 'Intervention'], range=['blue', 'red']),
    tooltip=list(df.columns)
)
p1 = P.mark_point(filled=True,opacity=0.9,size=100).encode()
#p2 = P.mark_point(filled=True, size=100,opacity=0.9).encode(shape=alt.Shape('durationofstudy:N').scale(range=["circle","diamond"]))
#p1

st.altair_chart(p1.configure_axis(
    labelFontSize=20,
    titleFontSize=20
).configure_title(
    fontSize=20
).configure_legend(
    titleFontSize=18,
    labelFontSize=18,
symbolSize = 100).configure_headerFacet(labelFontSize=20,labelFontWeight='bold', title= None)
,use_container_width=True)

custom_colors = [
    '#1f77b4',  # blue
    '#ff7f0e',  # orange
    '#2ca02c',  # green
    '#d62728',  # red
    '#9467bd',  # purple
    '#8c564b',  # brown
    '#e377c2',  # pink
    '#7f7f7f',  # gray
    '#bcbd22',  # olive
    '#17becf',  # cyan
    "#00060e",  # black
    "#ff9878",  # light orange
    '#98df8a',  # light green
    '#ff9896'   # light red
]

# Base chart definition
P = alt.Chart(df).encode(
    alt.X('standardizedeucl_dist',
          title='Standardized Euclidean distance at baseline',
          scale=alt.Scale(zero=False, domain=[0, 3])),
    alt.Y('DBP_scenariorange',
          title='Scenario Range',
          scale=alt.Scale(zero=False, domain=[0, 35])),
    color=alt.Color('Author_pmid:N',scale=alt.Scale(range=custom_colors)).legend(None),
    tooltip=list(df.columns)
)
#color=alt.Color('Scenario',#scale=alt.Scale(scheme='tableau10'))
# alt.Scale(scheme='viridis')
# Points layer
p1 = P.mark_point(filled=True, opacity=0.9, size=100)
p2= alt.Chart(df).mark_rule(color='gray',size=3).encode(y=alt.datum(0))
p3 = alt.Chart(df).mark_rule(color='gray',size=3).encode(x=alt.datum(0))

# Text labels layer — here I'm labeling with 'Author_pmid' but you can pick any other column
labels = P.mark_text(
    align='left',
    dx=5,  # horizontal offset
    dy=-5,  # vertical offset
    fontSize=10,
    angle=290
).encode(
    text='lname:N'
)

# Combine points and labels
final_chart = (p1 +p2+p3+ labels)

# Streamlit render
st.altair_chart(
    final_chart.configure_axis(
        labelFontSize=20,
        titleFontSize=20
    ).configure_title(
        fontSize=20
    ).configure_legend(
        titleFontSize=18,
        labelFontSize=18,
        symbolSize=100
    ).configure_headerFacet(
        labelFontSize=20,
        labelFontWeight='bold',
        title=None
    ),
    width='stretch'
)