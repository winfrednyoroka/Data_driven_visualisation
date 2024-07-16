# Importing necessary libraries

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Read in the data
DBP = pd.read_csv('./Data/Study_Pop_BMI_DBP.csv')
result_df = pd.read_csv('./Data/DBP_baseline_normalizedeucdist.csv')
range_df = pd.read_csv('./Data/BMI_DBP_scenariorange.csv')

# Set the side bar
with st.sidebar:
	st.title('Data driven visualisation')
	

# Make two columns one to hold the data and another for actual visualisations

col1,col2 = st.columns([4,1])
# 
with col1:
	st.info('Data loaded')
with col2:
	st.info('Vis')
	
	
tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(['Data', 'BMI vs DBP @baseline','Euc_dist_dataframe','Euc_dist@baseline','Scenario_range_dataframe','Range'])

with tab1:
	st.dataframe(DBP) # view the data on the web app
	#st.dataframe(result_df)
	
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

main_plot = (p1+p2+p3+p4).facet('Author_pmid',columns = 2, align='all')

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


# Plot the Euclidean distances
# Visualize the Euclidean distance and how far it deviates from 0


T1C1_Eucdist =alt.Chart(result_df).mark_point(filled=True,size =500,color='red').encode(
    x=alt.X('standardizedeucl_dist').scale(zero=True, domain=[0.0,2]),
    y = alt.Y('Author_pmid:N'),tooltip=list(result_df.columns)
).properties( title = 'A plot showing standardized euclidean distance between baseline intervention and control (DBP)')
T1C1_Eucdist_ref = alt.Chart(result_df).mark_rule(strokeDash=[10, 10],color='green',size=3).encode(x=alt.datum(0))
eline = T1C1_Eucdist.mark_rule(size = 5).encode( y='Author_pmid:N',x='standardizedeucl_dist',x2=alt.datum(0)) # adding lines to show how far the range is from reference (0)
T1C1_Eucdist_plot = (eline + T1C1_Eucdist_ref + T1C1_Eucdist)
T1C1_Eucdist_DBP_plot= T1C1_Eucdist_plot.configure_axis(
    labelFontSize=15,
    titleFontSize=20
).configure_title(fontSize=22)

with tab3:
	#st.dataframe(DBP) # view the data on the web app
	st.dataframe(result_df)
with tab4:
	st.altair_chart(T1C1_Eucdist_DBP_plot, use_container_width=True)

# Visualise the Range
# Visualize the ranges with reference to zero and draw the lines connecting the dots

DBPrange =alt.Chart(range_df).mark_point(filled=True,size =500,color='red').encode(
    x=alt.X('DBP_scenariorange').scale(zero=True, domain=[0.0,27]),
    y = alt.Y('Author_pmid:N'),tooltip=list(range_df.columns)
).properties( title = 'A plot showing how far the range between max and min scenario is from zero')
DBPrange_ref = alt.Chart(range_df).mark_rule(strokeDash=[10, 10],color='green',size=3).encode(x=alt.datum(0))
line = DBPrange.mark_rule(size = 5).encode( y='Author_pmid:N',x='DBP_scenariorange',x2=alt.datum(0)) # adding lines to show how far the range is from reference (0)
DBPrange_plot = (line + DBPrange_ref + DBPrange)
DBPrange_plot.configure_axis(
    labelFontSize=15,
    titleFontSize=20   
).configure_title(fontSize=22)
	
with tab5:
	st.dataframe(range_df) # Display the range dataframe
	
with tab6:
	st.altair_chart(DBPrange_plot.configure_axis(
    labelFontSize=15,
    titleFontSize=20   
).configure_title(fontSize=22),use_container_width=True)
		


