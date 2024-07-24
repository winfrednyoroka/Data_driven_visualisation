# Loading libraries
import streamlit as st
import pandas as pd 
import numpy as np 
import scipy
import altair as alt 

st.markdown(":blue[Scenario range]")
st.write(''' We calculated Wald ratios for three scenarios in each study to estimate the effect of change in body mass index (BMI)
    on diastolic blood pressure (DBP). We calculated the range by determining the maximum and the minimum Wald ratio.
    A range of zero shows the treatment arms have similar slope and the difference at twelve months is a result of either of the treatment
    causing more weightloss and subsequently lower DBP.
    ''')
st.sidebar.markdown("Scenario range  data and visualisation")

tab1,tab2=st.tabs(['Data','Scenario range visualisation'])
# Read in the data (Scenario range)
range_df = pd.read_csv('/Users/qb21134/OneDrive - University of Bristol/Winfred_PhDApps/Data_driven_visualisation/Data/BMI_DBP_scenariorange.csv')


# Plot the scenario rnage
# Visualise the scenario range and show how far each datapoint is from zero (0)



DBPrange =alt.Chart(range_df).mark_point(filled=True,size =200,color='red').encode(
    x=alt.X('DBP_scenariorange').scale(zero=True, domain=[0.0,27]),
    y = alt.Y('Author_pmid:N'),tooltip=list(range_df.columns)
).properties( title = 'A plot showing how far the range between max and min scenario is from zero')
DBPrange_ref = alt.Chart(range_df).mark_rule(strokeDash=[10, 10],color='green',size=3).encode(x=alt.datum(0))
line = DBPrange.mark_rule(size = 5).encode( y='Author_pmid:N',x='DBP_scenariorange',x2=alt.datum(0)) # adding lines to show how far the range is from reference (0)
DBPrange_plot = (line + DBPrange_ref + DBPrange)
DBPrangeplot = DBPrange_plot.configure_axis(
    labelFontSize=15,
    titleFontSize=20   
).configure_title(fontSize=22)


# Display the dataframe
with tab1:
    st.dataframe(range_df)

    st.text("""The dataframe shown above contains the range and study 
characteristics.
It has the minimum and maximum Wald ratio.""")

with tab2:
    st.altair_chart(DBPrangeplot, use_container_width=True)
    st.text("""The plot above shows the range i.e. maximum Wald ratio less 
minimum Wald ratio for each.
A range of zero, shows that the baseline characteristics were the same 
across the treatment arms.
All the studies""")