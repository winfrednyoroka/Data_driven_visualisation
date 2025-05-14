# Loading libraries
import streamlit as st
import pandas as pd 
import numpy as np 
import scipy
import altair as alt 

st.title('Merged Eucdist and Scenario Range')
# Read in both datasets

# Range dataset
range_df = pd.read_csv('/Users/qb21134/OneDrive - University of Bristol/Winfred_PhDApps/Data_driven_visualisation/Data/BMI_DBP_scenariorange.csv')
result_df = pd.read_csv('/Users/qb21134/OneDrive - University of Bristol/Winfred_PhDApps/Data_driven_visualisation/Data/DBP_baseline_normalizedeucdist.csv')

# Combine the two datasets for visualisation on column 'Author_pmid'
st.dataframe(range_df)
st.dataframe(result_df)

df = pd.merge(range_df,result_df, on ='Author_pmid')
st.dataframe(df)

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



# Base chart definition
P = alt.Chart(df).encode(
    alt.X('standardizedeucl_dist',
          title='Standardized Euclidean distance at baseline',
          scale=alt.Scale(zero=False, domain=[0, 3])),
    alt.Y('DBP_scenariorange',
          title='Scenario Range',
          scale=alt.Scale(zero=False, domain=[0, 35])),
    color=alt.Color('Author_pmid:N').legend(None),
    tooltip=list(df.columns)
)

# Points layer
p1 = P.mark_point(filled=True, opacity=0.9, size=100)
p2= alt.Chart(df).mark_rule(strokeDash=[10, 10],color='gray',size=3).encode(y=alt.datum(0))
p3 = alt.Chart(df).mark_rule(strokeDash=[10, 10],color='gray',size=3).encode(x=alt.datum(0))

# Text labels layer — here I'm labeling with 'Author_pmid' but you can pick any other column
labels = P.mark_text(
    align='left',
    dx=5,  # horizontal offset
    dy=-5,  # vertical offset
    fontSize=14,
    angle=300
).encode(
    text='Author_pmid:N'
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
    use_container_width=True
)