import altair as alt
import pandas as pd
import streamlit as st
from PIL import Image
from vega_datasets import data


@st.cache

def load_data():
    raw_df = pd.read_csv('all_data.csv')
    covid_df = pd.read_csv('covid_data.csv')
    
    return df

# Load the data in the same working directory

# df = load_data()

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9= st.tabs(["📣 Start", "📈 Plot 1", "📈 Plot 2",
                                                                "📈 Plot 3", "📈 Plot 4", "📈 Plot 5",
                                                                  "📈 Plot 6", "📈 Plot 7", "🗃 Data"])

raw_df = pd.read_csv('all_data.csv')
covid_df = pd.read_csv('covid_data.csv')

#create a drop-down selector for state
states = raw_df['state'].unique()
state_dropdown1 = alt.binding_select(options=states)
state_select1 = alt.selection_single(
    fields=['state'], bind=state_dropdown1, name="State1", init={'state':'New Jersey'})

state_dropdown2 = alt.binding_select(options=states)
state_select2 = alt.selection_single(
    fields=['state'], bind=state_dropdown2, name="State2", init={'state':'Maryland'})

states2 = covid_df['state'].unique()
state2_dropdown1 = alt.binding_select(options=states2)
state2_select1 = alt.selection_single(
    fields=['state'], bind=state2_dropdown1, name="State1", init={'state':'New Jersey'})

state2_dropdown2 = alt.binding_select(options=states2)
state2_select2 = alt.selection_single(
    fields=['state'], bind=state2_dropdown2, name="State2", init={'state':'Maryland'})

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
#, init={'patient_variable':'Age: 45-64 years'}


#calculate mortality rate ([deaths / new cases] *100)
raw_df['Death_Rate']=(raw_df['new_deaths']/raw_df['new_cases']) * 100
covid_df['Death_Rate']=(covid_df['new_deaths']/covid_df['new_cases']) * 100


#test with 10 states
#state_sub = ['Maryland', 'Connecticut', 'New York', 'New Jersey', 'California', 'Colorado', 'Texas', 'Florida', 'Michigan']
#raw_df = raw_df[raw_df['state'].isin(state_sub)]

with tab1:

    image = Image.open('title.jpeg')
    st.image(image, caption='COVID-19 virus image is creative commons license')

    st.header("Welcome to our COVID-19 Healthcare Utilization Analysis App")
    st.markdown("In this repo, we have produced several dynamic figures using data pertaining to hospital utilization and the COVID-19 pandemic.")
    st.markdown("The COVID-19 pandemic has had a significant impact on healthcare utilization. While some patients have continued to seek emergency care for urgent medical needs, others have been hesitant to go to the health care institutions due to fears of contracting COVID-19. This has resulted in a change in healthcare utilization. The pandemic has also led to changes in the way care is delivered, including increased use of telemedicine and a greater focus on infection prevention and control measures. As the COVID-19 pandemic continues to evolve and in preparation for future public health crises, an analysis of healthcare utilization is prudent.")
    st.markdown("We will utilize two primary data sources to investigate the impact of the coronavirus pandemic on healthcare utilization in the US. Data on coronavirus cases and deaths will be obtained from the Centers for Disease Control and Prevention (CDC), which maintains geographic and temporal incidence data. Data on emergency department utilization and inpatient admissions will be derived from the Healthcare Cost and Utilization Project (HCUPnet): https://datatools.ahrq.gov/hcupnet. HCUP is a collection of healthcare databases developed through a public/private partnership and sponsored by the Agency for Healthcare Research and Quality (AHRQ). Data is collected by individual states and aggregated by AHRQ. Details regarding HCUP are available: https://www.hcup-us.ahrq.gov/") 
    st.markdown("Authors: Brendin Beaulieu-Jones & Matthew Crowson")

with tab2:
    st.header("Head-to-Head: COVID Cases and Mortality by State")

    #Visualization (1) - THIS IS THE COVID DATAFRAME AND WORKS ON ALL 50 STATES
    upper = alt.Chart(covid_df).mark_line(point=True).properties(
        width=550,
    ).encode(
        x = alt.X("date:O", axis=alt.Axis(title=None),sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
        y = alt.Y("Death_Rate:Q", axis=alt.Axis(title="COVID Mortality Rate")),
        color = 'state:N'
    )
    #upper

    lower = alt.Chart(covid_df).mark_bar().properties(
        width=60
    ).encode(
        x=alt.X('state:N', axis=alt.Axis(title=None)),
        y=alt.Y("new_deaths:Q", axis=alt.Axis(title="Number of New Cases")),
        color = 'state:N',
        column=alt.Column("date:O", title=None, sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
    )
    #lower

    plot1 = upper & lower
    plot1 = plot1.add_selection(
        state2_select1, state2_select2
    ).transform_filter(
        state2_select1 | state2_select2
    )
    plot1

with tab3:
    st.header("Head-to-Head: COVID Mortality & Hospital Length of Stay")

    #Visualization (2)

    upper2 = alt.Chart(raw_df).mark_line(point=True).properties(
        width=550
    ).encode(
        x = alt.X("date:O", axis=alt.Axis(title=None), sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
        y = alt.Y("Death_Rate:Q", axis=alt.Axis(title="COVID Mortality Rate")),
        color = "state:N"
    )
    #upper2

    lower2 = alt.Chart(raw_df).mark_point().properties(
        width=550
    ).encode(
        x=alt.X("date:O", axis=alt.Axis(title=None), sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
        y=alt.Y('mean(LOS):Q', axis=alt.Axis(title="Hospital Length of Stay (Days)")),
        color = 'state:N',
    )
    #lower2

    plot2 = upper2 & lower2
    plot2 = plot2.add_selection(
        state_select1, state_select2
    ).transform_filter(
        state_select1 | state_select2
    )
    plot2

#Visualization (Z)
#Issues: would be nice to add total deaths or death rate to upper chart
#Issues: would be nice for donut plots to show % rather than raw numbers 

with tab4:
    st.header("Head-to-Head: COVID Mortality & Age")

    #Visualization (3)
    upper6 = alt.Chart(raw_df).mark_point().properties(
        width=550
    ).encode(
        x = alt.X("patient_variable", axis=alt.Axis(title=None)),
        y = alt.Y("mean(Death_Rate):Q", axis=alt.Axis(title="COVID Mortality Rate")),
        color = "state:N"
    )

    upper6 = upper6.add_selection(
        state_select1, state_select2
    ).transform_filter(
        state_select1 | state_select2
    )
    upper6

with tab5:
    #t.header("COVID Mortality Rates by Age")
    viz5 = raw_df[raw_df['discharge_variable'].str.contains("COVID-19-Related Inpatient Stays")]
    #Visualization (4a)
    viz = alt.Chart(viz5,title="Comparing COVID-19 Discharges to Total COVID Deaths, by Age").mark_point().properties(
        width=1000
    ).encode(
        x=alt.X('sum(discharge_n):Q', title="COVID-19 Hospital Discharges"),
        y=alt.Y('tot_deaths:Q', title="Total COVID Deaths"),
        color='patient_variable:N',
        tooltip=['patient_variable:N']
    )
    viz

    #st.header("Hospital Length of Stay by Age")

    #Visualization (4b)
    lower3 = alt.Chart(raw_df, title="Hospital Length of Stay by Age").mark_point().properties(
        width=150
    ).encode(
        x=alt.X("date:O", axis=alt.Axis(title=None), sort= ["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]),
        y=alt.Y('mean(LOS):Q', axis=alt.Axis(title="Hospital Length of Stay (Days)")),
        color = 'state:O',
        column=alt.Column('patient_variable:N', title=None),
    )

    lower3 = lower3.add_selection(
        state_select1, state_select2
    ).transform_filter(
        state_select1 | state_select2
    )
    lower3

with tab6:
    st.header("Case Counts and Mortality Rate by State")

    #Visualization (5)
    base = alt.Chart(covid_df).encode(alt.X('date:O', title=None, sort=["Dec-2020", "Jan-2021", "Feb-2021", "Mar-2021", "Apr-2021", "May-2021", "Jun-2021"]))

    bar = base.mark_bar().encode(y=alt.Y('sum(tot_cases):Q', axis=alt.Axis(title="Total Cases")))


    line = base.mark_point(color='red').encode(
        y=alt.Y('sum(Death_Rate):Q', axis=alt.Axis(title="COVID Mortality Rate"))
    )

    plot4 = (bar + line).properties(width=600).resolve_scale(y='independent')
    plot4 = plot4.add_selection(
                        state_select1
                    ).transform_filter(
                        state_select1
                    )

    ages = ['Age: 0-17 years', 'Age: 18-44 years', 'Age: 45-64 years', 'Age:65-79 years', 'Age: 80+ years']

    base2 = alt.Chart(raw_df
                    ).add_selection(
                        state_select1
                    ).transform_filter(
                        state_select1
                    )

    donut1 = base2.mark_arc(innerRadius=50, outerRadius=90).encode(
        theta=alt.Theta(field="tot_cases", aggregate="sum", type="quantitative"),
        color=alt.Color('patient_variable', sort=ages),
        tooltip= [
            alt.Tooltip(shorthand="sum(tot_cases):Q", title="Total Cases"),
            alt.Tooltip("state:N", title="State"),
            alt.Tooltip("patient_variable:O", title="Age Group")
        ]
        ).properties(
            width=250
        )
    

    lower2 = alt.Chart(raw_df).mark_line(point=True).properties(
        width=250
    ).encode(
        x = alt.X('patient_variable:O', axis=alt.Axis(title=None)),
        y = alt.Y('sum(1st_dose):Q', axis=alt.Axis(title="First Dose of COVID-19")),
    ).add_selection(
                        state_select1
    ).transform_filter(
        state_select1
    )
    
    #lower2

    donut=alt.hconcat(lower2, donut1)

    chart5 = alt.vconcat(plot4, donut
                        ).resolve_scale(
                            color='independent'
                        )
    chart5

with tab7:
   #st.header("Plot 6")

    #Visualization (6)
    
    covid_new1 = covid_df.groupby(['state', 'date', 'Unnamed: 0']).sum().reset_index()
    covid_new1['tot_cases'] = covid_df.groupby(['state', 'date']).sum().groupby(['state', 'date', 'Unnamed: 0']).first().reset_index()['tot_cases']
    covid_new1['Death_Rate']=(covid_new1['new_deaths']/covid_new1['new_cases']) * 100

    #from vega_datasets import data

    source = alt.topo_feature(data.us_10m.url, 'states')

    date = 'Dec-2020'
    covid_new1 = covid_new1[covid_new1['date']==date]

    covid_new1 = covid_new1.sort_values(by='state', ascending=True)
    covid_new1['id']=covid_new1.reset_index().index
    covid_new1['id']=covid_new1["id"] +1

    width = 600
    height = 300
    project = 'albersUsa'

    background = alt.Chart(source
    ).mark_geoshape(
        fill='#aaa',
        stroke='white'
    ).properties(
        width=width,
        height=height
    ).project(project)

    selector = alt.selection_single(
        empty='all', fields=['id']
        )

    chart_base = alt.Chart(source
        ).properties( 
            width=width,
            height=height
        ).project(project
        ).add_selection(selector
        ).transform_lookup(
            lookup="id",
            from_=alt.LookupData(covid_new1, "id", ["Death_Rate", 'state', 'tot_cases', 'date']),
        )
    
    rate_scale = alt.Scale(domain=[covid_new1['Death_Rate'].min(), covid_new1['Death_Rate'].max()], scheme='oranges')
    rate_color = alt.Color(field="Death_Rate", type="quantitative", scale=rate_scale)
    chart_rate = chart_base.mark_geoshape().encode(
        color=rate_color,
        tooltip=[alt.Tooltip("Death_Rate:Q", title="COVID-19 Death Rate"),
                 alt.Tooltip("state:N", title="State")
            ],
        ).transform_filter(
        selector
        ).properties(
            title=f'Death Rate by State in the United States {date}'
    )
        
    population_scale = alt.Scale(domain=[covid_new1['tot_cases'].min(), covid_new1['tot_cases'].max()], scheme='yellowgreenblue')
    chart_total = chart_base.mark_geoshape().encode(
        color=alt.Color(field="tot_cases", type="quantitative", scale=population_scale),
        tooltip=['tot_cases:Q', 'state:N']
        ).transform_filter(
        selector
    ).properties(
        title=f'Total Cases by State as of {date}'
    )

    chart8 = alt.vconcat(background + chart_rate, background + chart_total
    ).resolve_scale(
        color='independent'
    )


    chart8


with tab8:
    #st.header("Plot 7")

    #Visualization (7)
    covid_new2 = covid_df.groupby(['state', 'date']).sum().reset_index()
    covid_new2['tot_cases'] = covid_df.groupby(['state', 'date']).sum().groupby(['state', 'date']).first().reset_index()['tot_cases']
    covid_new2['Death_Rate']=(covid_new2['new_deaths']/covid_new2['new_cases']) * 100

    from vega_datasets import data
    source = alt.topo_feature(data.us_10m.url, 'states')

    date2 = 'May-2021'
    covid_new2 = covid_new2[covid_new2['date']==date2]

    covid_new2['id']=covid_new2.reset_index().index
    covid_new2['id']=covid_new2["id"] +1

    width = 600
    height = 300
    project = 'albersUsa'

    background = alt.Chart(source
    ).mark_geoshape(
        fill='#aaa',
        stroke='white'
    ).properties(
        width=width,
        height=height
    ).project(project)

    selector = alt.selection_single(
        empty='all', fields=['id']
        )

    chart_base = alt.Chart(source
        ).properties( 
            width=width,
            height=height
        ).project(project
        ).add_selection(selector
        ).transform_lookup(
            lookup="id",
            from_=alt.LookupData(covid_new2, "id", ["2nd_dose", 'state', 'new_deaths', 'date']),
        )
    
    first_scale = alt.Scale(domain=[covid_new2['2nd_dose'].min(), covid_new2['2nd_dose'].max()], scheme='oranges')
    first_color = alt.Color(field="2nd_dose", type="quantitative", scale=first_scale)
    chart_first = chart_base.mark_geoshape().encode(
        color=first_color,
        tooltip=['2nd_dose:Q', 'state:N']
        ).transform_filter(
        selector
        ).properties(
            title=f'Number of Individuals who Received 2 Doses of COVID Vaccine by State in the United States {date2}'
    )
        
    second_scale = alt.Scale(domain=[covid_new2['new_deaths'].min(), covid_new2['new_deaths'].max()], scheme='yellowgreenblue')
    chart_second = chart_base.mark_geoshape().encode(
        color=alt.Color(field="new_deaths", type="quantitative", scale=second_scale),
        tooltip=['new_deaths:Q', 'state:N']
        ).transform_filter(
        selector
    ).properties(
        title=f'Number of New Deaths by State in the United States {date2}'
    )

    chart9 = alt.vconcat(background + chart_first, background + chart_second
    ).resolve_scale(
        color='independent'
    )

    chart9

with tab9:

    st.header("Data")

    st.markdown("In the spirit of reproducibility, we have included out curated database here.")

    st.dataframe(data=raw_df)