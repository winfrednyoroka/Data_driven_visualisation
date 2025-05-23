# Importing necessary libraries

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(layout='wide')
st.title('Data-driven Visualisation')
st.markdown(":blue[BMI vs DBP pre-post treatment]")
st.write('''We visualise the body mass index (BMI) and 
         diastolic blood pressure (DBP) at baseline. If the treatment arms started the same, we expect the
		 datapoints to overlap.''')
st.sidebar.markdown("**Data visualisation of BMI vs DBP pre-post**")

# Read in the data
DBP = pd.read_csv('./Data/Study_Pop_BMI_DBP_V1.csv')
tab1,tab2 = st.tabs(['Data', 'BMI_DBP visualisation pre-post treatment'])

with tab1:
	# view the data on the web app
	st.dataframe(DBP)
	st.text('''The dataframe above details pre-post average BMI and DBP in each study.''')
	
	
DBP.rename(columns={'durationofstudy': 'Study duration','intervention_control':'Intervention_Control'}, inplace=True) # rename columns in place

# Update the entries in Intervention_control
DBP['Intervention_Control'] = DBP['Intervention_Control'].str.capitalize() # Make the first letter of the entries capital
#DBP
##### Visualize baseline and post-intervention at 12 months - DBP and split some studies with more than 2 treatment groups
df = DBP.loc[DBP['Study duration'].isin ([12,0])]
df = df.loc[~df['pmid'].isin([34554379,194696,25919069,30471927,32805133,1234567,23706413])]# Exclude papers without 12 month measures
P = alt.Chart(df).encode(
    alt.X('meanBMI',
          title='Mean BMI (kg/m²)',
          scale=alt.Scale(zero=False, domain=[10, 70])),
    alt.Y('meanDBP',
          title='Mean Diastolic Blood Pressure (mmHg)',
          scale=alt.Scale(zero=False, domain=[28, 150])),
    color=alt.Color('Intervention_Control:N')
        .scale(domain=['Control', 'Intervention'], range=['blue', 'red']),
    tooltip=list(df.columns)
)
p1 = P.mark_line(opacity=0.9,size=3).encode()
p2 = P.mark_point(filled=True, size=100,opacity=0.9).encode(shape=alt.Shape('durationofstudy:N').scale(range=["circle","diamond"]))
p3= alt.Chart(df).mark_rule(strokeDash=[10, 10],color='green',size=3).encode(y=alt.datum(80))
p4 = alt.Chart(df).mark_rule(strokeDash=[10, 10],color='gray',size=3).encode(x=alt.datum(30))
# Vertical error bars for DBP (y-axis)
error_y = alt.Chart(df).mark_rule(strokeDash=[4, 4],color='gray',opacity=0.3,size=2).encode(
    x='meanBMI',
    y='lowerboundDBP',
    y2='upperboundDBP'
)

# Horizontal error bars for BMI (x-axis)
error_x = alt.Chart(df).mark_rule(strokeDash=[4, 4],color='green',opacity=0.3,size=2).encode(
    y='meanDBP',
    x='lowerboundBMI',
    x2='upperboundBMI'
)
#p4.mark_text(align='left',dx=5).encode(text='BMI')

main_plot = (p1+p2+p3+p4+error_x+error_y).facet('Author_pmid',columns=4,align='all')
main_plot

# P = alt.Chart(df).encode(alt.X('meanBMI').scale(zero=False,domain=[10, 70]),
#                          alt.Y('meanDBP').scale(zero=False,domain=[28, 150]),
#                          color= alt.Color('Intervention_Control:N').scale(domain=['Control','Intervention'],range=['blue','red']),
#                          tooltip=list(df.columns))#,order=alt.Order('durationofstudy:N',sort='ascending'))
# p1 = P.mark_line(opacity=0.9,size=3).encode()
# p2 = P.mark_point(filled=True, size=200,opacity=0.9).encode(shape=alt.Shape('Study duration:N').scale(range=["circle","diamond"]))
# p3= alt.Chart(df).mark_rule(strokeDash=[10, 10],color='green',size=3).encode(y=alt.datum(80))
# p4 = alt.Chart(df).mark_rule(strokeDash=[10, 10],color='gray',size=3).encode(x=alt.datum(30))
# error_y = alt.Chart(df).mark_rule(strokeDash=[4, 4],color='gray',opacity=0.3,size=2).encode(
#     x='meanBMI',
#     y='lowerboundDBP',
#     y2='upperboundDBP'
# )

# # Horizontal error bars for BMI (x-axis)
# error_x = alt.Chart(df).mark_rule(strokeDash=[4, 4],color='green',opacity=0.3,size=2).encode(
#     y='meanDBP',
#     x='lowerboundBMI',
#     x2='upperboundBMI'
# )
# #p4.mark_text(align='left',dx=5).encode(text='BMI')

# # main_plot = (p1+p2+p3+p4+error_x+error_y).facet('Author_pmid',columns=4,align='all')
# # main_plot
# #p4.mark_text(align='left',dx=5).encode(text='BMI')

# main_plot = (p1+p2+p3+p4+error_x+error_y).facet('Author_pmid',columns = 4, align='all')

# Combine all plots
DBP_plot = main_plot
DBP_plot.configure_axis(
    labelFontSize=20,
    titleFontSize=20
).configure_title(
    fontSize=20
).configure_legend(
    titleFontSize=18,
    labelFontSize=18,
symbolSize = 300).configure_headerFacet(labelFontSize=20,labelFontWeight='bold', title= None)

	
with tab2:
	st.altair_chart(DBP_plot.configure_axis(
    labelFontSize=20,
    titleFontSize=20
).configure_title(
    fontSize=20
).configure_legend(
    titleFontSize=18,
    labelFontSize=18,
symbolSize = 300).configure_headerFacet(labelFontSize=20,labelFontWeight='bold', title= None)
,use_container_width=True)
	st.text('''The plot above shows BMI vs DBP for both treatment arms pre-post treatment.
The circles represent the baseline, and the diamonds show the twelve months measure.
The red and blue represent the intervention and control arm respectively.''')