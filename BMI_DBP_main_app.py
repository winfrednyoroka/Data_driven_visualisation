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
DBP = pd.read_csv('./Data/Study_Pop_BMI_DBP.csv')
tab1,tab2,tab3 = st.tabs(['Data', 'BMI_DBP visualisation pre-post treatment no CIs','BMI_DBP visualisation pre-post treatment'])

with tab1:
	# view the data on the web app
	st.dataframe(DBP)
	st.text('''The dataframe above details pre-post average BMI and DBP in each study.''')
	
	
DBP.rename(columns={'durationofstudy': 'Study duration','intervention_control':'Intervention_Control'}, inplace=True) # rename columns in place

# Update the entries in Intervention_control
DBP['Intervention_Control'] = DBP['Intervention_Control'].str.capitalize() # Make the first letter of the entries capital

	
with tab2:
	##### Visualize baseline and post-intervention at 12 months - DBP and split some studies with more than 2 treatment groups
    df = DBP.loc[DBP['Study duration'].isin ([12,0])]
    df = df.loc[~df['pmid'].isin([34554379,194696,25919069,30471927,32805133,1234567,23706413,28000425])]# Exclude papers without 12 month measures
    P = alt.Chart(df).encode(
    x= alt.X('meanBMI',
            title='Mean BMI (kg/m²)',
            scale=alt.Scale(zero=False, domain=[10, 70]),axis=alt.Axis(domain=True,domainWidth=2, domainColor='black')),
    y=alt.Y('meanDBP',
            title='Mean Diastolic Blood Pressure (mmHg)',
            scale=alt.Scale(zero=False, domain=[28, 150]),axis=alt.Axis(domain=True,domainWidth=2, domainColor='black')),
    color=alt.Color('Intervention_Control:N')
        .scale(domain=['Control', 'Intervention'], range=['blue', 'red']),
    tooltip=list(df.columns)
    )
    p1 = P.mark_line(opacity=0.9,size=3).encode()
    p2 = P.mark_point(filled=True, size=100,opacity=0.9).encode(shape=alt.Shape('Study duration:N').scale(range=["circle","diamond"]))
    p3= alt.Chart(df).mark_rule(strokeDash=[10, 10],color='black',size=3).encode(y=alt.datum(80))
    p4 = alt.Chart(df).mark_rule(strokeDash=[10, 10],color='green',size=3).encode(x=alt.datum(30))
    # Vertical error bars for DBP (y-axis) and end markers
    error_y = alt.Chart(df).mark_rule(color='black',opacity=0.3,size=2).encode(
    x='meanBMI',
    y='lowerboundDBP',
    y2='upperboundDBP'
    )
    # End markers and or ticks
    # End markers for vertical error bars (top and bottom ticks)

    tick_y_lower = alt.Chart(df).transform_filter(
        "datum.lowerboundDBP > 0"
        ).mark_tick(thickness=2, size=10, color='black', orient='horizontal').encode(
              x='meanBMI',
              y='lowerboundDBP'
              )

    # Upperbound tick for horizontal error bar — only if both exist
    tick_y_upper = alt.Chart(df).transform_filter(
        "datum.upperboundDBP > 0"
        ).mark_tick(thickness=2, size=10, color='black', orient='horizontal').encode(
               x='meanBMI',
               y='upperboundDBP'
               )
    # Combine
    ticks_y = tick_y_lower + tick_y_upper

    # Horizontal error bars for BMI (x-axis)
    error_x = alt.Chart(df).mark_rule(color='purple',opacity=0.3,size=2).encode(
    y='meanDBP',
    x='lowerboundBMI',
    x2='upperboundBMI'
    )
     # End markers and or ticks
    # End markers for horizontal error bars (top and bottom ticks)
    tick_x_lower = alt.Chart(df).transform_filter(
        "datum.lowerboundBMI > 0"
        ).mark_tick(thickness=2, size=10, color='purple', orient='vertical').encode(
            x='lowerboundBMI',
            y='meanDBP'
        )

    # Upperbound tick for horizontal error bar — only if both exist
    tick_x_upper = alt.Chart(df).transform_filter(
        "datum.upperboundBMI > 0"
          ).mark_tick(thickness=2, size=10, color='purple', orient='vertical').encode(
        x='upperboundBMI',
        y='meanDBP'
        )
    # Combine
    ticks_x = tick_x_lower + tick_x_upper

    # Combine all plots
    main_plot = (p1+p2+p3+p4).facet('Author_pmid',columns=4,align='all')
    #main_plot

    # Rename the plot all plots
    # BMI_DBP_plot = main_plot

    # st.altair_chart(BMI_DBP_plot.configure_axis(
	# 	grid=False,
    # labelFontSize=20,
    # titleFontSize=20
	# ).configure_title(
    # fontSize=20
	# ).configure_legend(
    # titleFontSize=18,
    # labelFontSize=18,
	# symbolSize = 300).configure_headerFacet(labelFontSize=20,labelFontWeight='bold')
	# ,use_container_width=True)
    # Apply configurations — only valid keys
    BMI_DBP_plot = main_plot.configure_axis(
        grid=False,
        labelFontSize=20,
        titleFontSize=20
    ).configure_title(
        fontSize=20
    ).configure_headerFacet(
        labelFontSize=20,
        labelFontWeight='bold'
    )

    # Display chart
    st.altair_chart(BMI_DBP_plot, use_container_width=True)
    st.text('''The plot above shows BMI vs DBP for both treatment arms pre-post treatment.    
            The circles represent the baseline, and the diamonds show the twelve months measure.    
            The red and blue represent the intervention and control arm respectively.''')
    


with tab3:
	##### Visualize baseline and post-intervention at 12 months - DBP and split some studies with more than 2 treatment groups
    df = DBP.loc[DBP['Study duration'].isin ([12,0])]
    df = df.loc[~df['pmid'].isin([34554379,194696,25919069,30471927,32805133,1234567,23706413,28000425])]# Exclude papers without 12 month measures
    P = alt.Chart(df).encode(
    x= alt.X('meanBMI',
            title='Mean BMI (kg/m²)',
            scale=alt.Scale(zero=False, domain=[10, 70]),axis=alt.Axis(domain=True,domainWidth=2, domainColor='black')),
    y=alt.Y('meanDBP',
            title='Mean Diastolic Blood Pressure (mmHg)',
            scale=alt.Scale(zero=False, domain=[28, 150]),axis=alt.Axis(domain=True,domainWidth=2, domainColor='black')),
    color=alt.Color('Intervention_Control:N')
        .scale(domain=['Control', 'Intervention'], range=['blue', 'red']),
    tooltip=list(df.columns)
    )
    p1 = P.mark_line(opacity=0.9,size=3).encode()
    p2 = P.mark_point(filled=True, size=100,opacity=0.9).encode(shape=alt.Shape('Study duration:N').scale(range=["circle","diamond"]))
    p3= alt.Chart(df).mark_rule(strokeDash=[10, 10],color='black',size=3).encode(y=alt.datum(80))
    p4 = alt.Chart(df).mark_rule(strokeDash=[10, 10],color='green',size=3).encode(x=alt.datum(30))
    # Vertical error bars for DBP (y-axis) and end markers
    error_y = alt.Chart(df).mark_rule(color='black',opacity=0.3,size=2).encode(
    x='meanBMI',
    y='lowerboundDBP',
    y2='upperboundDBP'
    )
    # End markers and or ticks
    # End markers for vertical error bars (top and bottom ticks)

    tick_y_lower = alt.Chart(df).transform_filter(
        "datum.lowerboundDBP > 0"
        ).mark_tick(thickness=2, size=10, color='black', orient='horizontal').encode(
              x='meanBMI',
              y='lowerboundDBP'
              )

    # Upperbound tick for horizontal error bar — only if both exist
    tick_y_upper = alt.Chart(df).transform_filter(
        "datum.upperboundDBP > 0"
        ).mark_tick(thickness=2, size=10, color='black', orient='horizontal').encode(
               x='meanBMI',
               y='upperboundDBP'
               )
    # Combine
    ticks_y = tick_y_lower + tick_y_upper

    # Horizontal error bars for BMI (x-axis)
    error_x = alt.Chart(df).mark_rule(color='purple',opacity=0.3,size=2).encode(
    y='meanDBP',
    x='lowerboundBMI',
    x2='upperboundBMI'
    )
     # End markers and or ticks
    # End markers for horizontal error bars (top and bottom ticks)
    tick_x_lower = alt.Chart(df).transform_filter(
        "datum.lowerboundBMI > 0"
        ).mark_tick(thickness=2, size=10, color='purple', orient='vertical').encode(
            x='lowerboundBMI',
            y='meanDBP'
        )

    # Upperbound tick for horizontal error bar — only if both exist
    tick_x_upper = alt.Chart(df).transform_filter(
        "datum.upperboundBMI > 0"
          ).mark_tick(thickness=2, size=10, color='purple', orient='vertical').encode(
        x='upperboundBMI',
        y='meanDBP'
        )
    # Combine
    ticks_x = tick_x_lower + tick_x_upper

    # Combine all plots
    plot2 = (p1+p2+p3+p4+error_x+ticks_x+error_y+ticks_y).facet('Author_pmid',columns=4,align='all')
    #main_plot

    # Rename the plot all plots
    #BMI_DBP_plot_CI = plot2

    BMI_DBP_plot_CI=plot2.configure_axis(
		grid=False,
    labelFontSize=20,
    titleFontSize=20
	).configure_title(
    fontSize=20
	).configure_headerFacet(labelFontSize=20,labelFontWeight='bold')
    #.configure_legend(
    #titleFontSize=18,
    #labelFontSize=18,
	#symbolSize = 300).configure_headerFacet(labelFontSize=20,labelFontWeight='bold')
    st.altair_chart(BMI_DBP_plot_CI,use_container_width=False)
    st.text('''The plot above shows BMI vs DBP for both treatment arms pre-post treatment with confidence intervals.    
            The circles represent the baseline, and the diamonds show the twelve months measure.    
            The red and blue represent the intervention and control arm respectively.''')