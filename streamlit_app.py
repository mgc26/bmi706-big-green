import altair as alt
import pandas as pd
import streamlit as st
from PIL import Image


@st.cache

def load_data():
    raw_df = pd.read_csv('all_data.csv')
    covid_df = pd.read_csv('covid_data.csv')
    
    return df

# Load the data in the same working directory

# df = load_data()

tab1, tab2, tab3, tab4, tab5= st.tabs(["📣 Start", "📈 Plot 1", "📈 Plot 2", "📈 Plot 3", "🗃 Data"])

raw_df = pd.read_csv('all_data.csv')
covid_df = pd.read_csv('covid_data.csv')

#create a drop-down selector for state
states = raw_df['state'].unique()
state_dropdown = alt.binding_select(options=states)
state_select = alt.selection_single(
    fields=['state'], bind=state_dropdown, name="State")

#create a drop-down selector for date
dates = raw_df['date'].unique()
date_dropdown = alt.binding_select(options=dates)
date_select = alt.selection_single(
    fields=['date'], bind=date_dropdown, name="Date")

#create a drop-down selector for age_group
ages = raw_df['patient_variable'].unique()
age_dropdown = alt.binding_select(options=ages)
age_select = alt.selection_single(
    fields=['age'], bind=age_dropdown, name="Age")


#calculate mortality rate ([deaths / new cases] *100)
raw_df['Death_Rate']=(raw_df['new_deaths']/raw_df['new_cases']) * 100


#test with five states (MD, CT, NY, NJ, CA)
state_sub = ['Maryland', 'Connecticut', 'New York', 'New Jersey', 'California']
raw_df = raw_df[raw_df['state'].isin(state_sub)]

with tab1:

    image = Image.open('title.jpeg')
    st.image(image, caption='COVID-19 virus image is creative commons license')

    st.header("Welcome to our COVID-19 Healthcare Utilization Analysis App")
    st.markdown("In this repo, we have produced several dynamic figures using data pertaining to hospital utilization and the COVID-19 pandemic.")
    st.markdown("The COVID-19 pandemic has had a significant impact on healthcare utilization. While some patients have continued to seek emergency care for urgent medical needs, others have been hesitant to go to the health care institutions due to fears of contracting COVID-19. This has resulted in a change in healthcare utilization. The pandemic has also led to changes in the way care is delivered, including increased use of telemedicine and a greater focus on infection prevention and control measures. As the COVID-19 pandemic continues to evolve and in preparation for future public health crises, an analysis of healthcare utilization is prudent.")
    st.markdown("We will utilize two primary data sources to investigate the impact of the coronavirus pandemic on healthcare utilization in the US. Data on coronavirus cases and deaths will be obtained from the Centers for Disease Control and Prevention (CDC), which maintains geographic and temporal incidence data. Data on emergency department utilization and inpatient admissions will be derived from the Healthcare Cost and Utilization Project (HCUPnet): https://datatools.ahrq.gov/hcupnet. HCUP is a collection of healthcare databases developed through a public/private partnership and sponsored by the Agency for Healthcare Research and Quality (AHRQ). Data is collected by individual states and aggregated by AHRQ. Details regarding HCUP are available: https://www.hcup-us.ahrq.gov/") 
    st.markdown("Authors: Brendin Beaulieu-Jones & Matthew Crowson")

with tab2:
    st.header("Plot 1")

    #Visualization (X)
    #Issues - trying to unstack bar chart
    #Issues - trying to add a second selection so that you can compare state A to state B

    upper = alt.Chart(raw_df).mark_line().properties(
        width=550
    ).encode(
        x = alt.X("date:O", sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
        y = "Death_Rate:Q",
        color = 'state:N'
    )
    upper

    lower = alt.Chart(raw_df).mark_bar().properties(
        width=550
    ).encode(
        x=alt.X("date:O", sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
        y=alt.Y("new_deaths:Q"),
        color = 'state:N',
    )
    lower

    plot1 = upper & lower
    plot1 = plot1.add_selection(
        state_select
    ).transform_filter(
        state_select
    )

    st.text('First Plot')

    plot1


#Visualization (Z)
#Issues - when stratify by age_group, data appears to disappear

with tab3:
    st.header("Plot 2")

    upper2 = alt.Chart(raw_df).mark_point().properties(
        width=550
    ).encode(
        x = alt.X("date:O", sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
        y = "mean(Death_Rate)",
        color = "state:N"
    )
    upper2

    lower2 = alt.Chart(raw_df).mark_point().properties(
        width=550
    ).encode(
        x=alt.X("date:O", sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
        y=alt.Y("mean(LOS)"),
        color = 'state:N',
    )
    lower2

    plot2 = upper2 & lower2
    plot2 = plot2.add_selection(
        age_select
    ).transform_filter(
        age_select
    ).add_selection(
        state_select
    ).transform_filter(
        state_select
    )

    st.text('Second Plot')

    plot2

#Visualization (Z)
#Issues: would be nice to add total deaths or death rate to upper chart
#Issues: would be nice for donut plots to show % rather than raw numbers 

with tab4:
    st.header("Plot 3")

    base2 = alt.Chart(raw_df
                    ).add_selection(
                        state_select
                    ).transform_filter(
                        state_select
                    )
                    
    bar1 = base2.mark_bar().encode(
            x = alt.X("date:O", sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
            y='sum(tot_cases):Q',
    ).properties(
        width=500
    )

    #bar2 = base2.mark_bar().encode(
    #        x = alt.X("date:O", sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
    #        y='sum(tot_deaths):Q',
    #).properties(
    #    width=500
    #)

    #c = alt.layer(bar1, bar2)

    ages = ['Age: 0-17 years', 'Age: 18-44 years', 'Age: 45-64 years', 'Age:65-79 years', 'Age: 80+ years']

    donut1 = base2.mark_arc(innerRadius=50, outerRadius=90).encode(
        theta=alt.Theta(field="new_cases", aggregate="sum", type="quantitative"),
        color=alt.Color('patient_variable', sort=ages),
        tooltip= [
            alt.Tooltip(shorthand="sum(new_cases):Q", title="New Cases"),
            alt.Tooltip("state:N", title="State"),
            alt.Tooltip("ages:O", title="Age Group")
        ]
    ).transform_filter(
        state_select
        ).properties(
            width=250
        )

    donut2 = base2.mark_arc(innerRadius=50, outerRadius=90).encode(
        theta=alt.Theta(field="new_deaths", aggregate="sum", type="quantitative"),
        color=alt.Color('patient_variable', sort=ages),
        tooltip= [
            alt.Tooltip(shorthand="sum(new_deaths):Q", title="New Deaths"),
            alt.Tooltip("state:N", title="State"),
            alt.Tooltip("ages:O", title="Age Group")
        ]
    ).transform_filter(
        state_select
        ).properties(
            width=250
        )

    donut=alt.hconcat(donut1, donut2)

    chart3 = alt.vconcat(bar1, donut
                        ).resolve_scale(
                            color='independent'
                        )

    st.text('Third Plot')

    chart3

with tab5:

    st.header("Data")

    st.markdown("In the spirit of reproducibility, we have included out curated database here.")

    st.dataframe(data=raw_df)