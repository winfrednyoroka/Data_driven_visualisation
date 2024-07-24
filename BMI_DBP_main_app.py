# Importing necessary libraries

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.markdown(":blue[BMI vs DBP pre-post treatment]")
st.write('''We visualise the body mass index (BMI) and 
         diastolic blood pressure (DBP) at baseline. If the treatment arms started the same, we expect the
		 datapoints to overlap.''')
st.sidebar.markdown(":blue[**Data visualisation of BMI vs DBP pre-post**]")

# Read in the data
DBP = pd.read_csv('./Data/Study_Pop_BMI_DBP.csv')	
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

P = alt.Chart(df).encode(alt.X('meanBMI').scale(zero=False,domain=[25, 56]),
                         alt.Y('meanDBP').scale(zero=False,domain=[67, 96]),
                         color= alt.Color('Intervention_Control:N').scale(domain=['Control','Intervention'],range=['blue','red']),
                         tooltip=list(df.columns))#,order=alt.Order('durationofstudy:N',sort='ascending'))
p1 = P.mark_line(opacity=0.9,size=3).encode()
p2 = P.mark_point(filled=True, size=200,opacity=0.9).encode(shape=alt.Shape('Study duration:N').scale(range=["circle","diamond"]))
p3= alt.Chart(df).mark_rule(strokeDash=[10, 10],color='green',size=3).encode(y=alt.datum(80))
p4 = alt.Chart(df).mark_rule(strokeDash=[10, 10],color='gray',size=3).encode(x=alt.datum(30))
#p4.mark_text(align='left',dx=5).encode(text='BMI')

main_plot = (p1+p2+p3+p4).facet('Author_pmid',columns = 4, align='all')

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
The circles represent baseline and diamonds show the twelve months measure.
The red and blue represent the intervention and control arm respectively.''')