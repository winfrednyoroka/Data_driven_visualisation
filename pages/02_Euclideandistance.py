# Loading libraries
import streamlit as st
import pandas as pd 
import numpy as np 
import scipy
import altair as alt 

st.markdown(":blue[Euclidean distance visualisation at baseline]")
st.write('''We calculated the Euclidean distance at baseline of body mass index (BMI) and diastolic blood presure (DBP)
	at baseline between the treatment arms.
	If both treatment arms started the same the Euclidean distance should be zero, otherwise they started
	differently. Click the first tab to see the data and the second tab to see the visualisation.''')
st.sidebar.markdown("Euclidean distance data and visualisation")


tab1,tab2=st.tabs(['Data','Euclidean distance visualisation @baseline'])
# Read in the data (Euclidena distance at baseline)
result_df = pd.read_csv('/Users/qb21134/OneDrive - University of Bristol/Winfred_PhDApps/Data_driven_visualisation/Data/DBP_baseline_normalizedeucdist.csv')

# Display the dataframe


# Plot the Euclidean distances
# Visualize the Euclidean distance and how far it deviates from 0


T1C1_Eucdist =alt.Chart(result_df).mark_point(filled=True,size =200,color='red').encode(
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


with tab1:
	# Display the data
	st.dataframe(result_df)
	st.text(''' The dataframe shown above contains the data we have used to calculate the Euclidean 
distances. It has the average BMI and DBP for both treatment arms.

		''')

with tab2:
	# Display the visualisation
	st.altair_chart(T1C1_Eucdist_DBP_plot,use_container_width=True)

	st.text('''The figure above shows Euclidean distance between the treatment arms at baseline.
Euclidean distance equal to zero shows BMI and DBP at baseline was the same in both treatment arms
while more than zero shows that the two treatment arms started differently. All of the studies here
started differently with Euclidean distance greater than zero (0).''')




