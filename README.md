# bmi706 - Final Project - Team Big_Green

## Introduction

In this repo, we have produced several dynamic figures using data pertaining to hospital utilization and the COVID-19 pandemic.

The COVID-19 pandemic has had a significant impact on healthcare utilization. While some patients have continued to seek emergency care for urgent medical needs, others have been hesitant to go to the health care institutions due to fears of contracting COVID-19. This has resulted in a change in healthcare utilization. The pandemic has also led to changes in the way care is delivered, including increased use of telemedicine and a greater focus on infection prevention and control measures. As the COVID-19 pandemic continues to evolve and in preparation for future public health crises, an analysis of healthcare utilization is prudent.

We will utilize two primary data sources to investigate the impact of the coronavirus pandemic on healthcare utilization in the US. Data on coronavirus cases and deaths will be obtained from the Centers for Disease Control and Prevention (CDC), which maintains geographic and temporal incidence data. Data on emergency department utilization and inpatient admissions will be derived from the Healthcare Cost and Utilization Project (HCUPnet): https://datatools.ahrq.gov/hcupnet. HCUP is a collection of healthcare databases developed through a public/private partnership and sponsored by the Agency for Healthcare Research and Quality (AHRQ). Data is collected by individual states and aggregated by AHRQ. Details regarding HCUP are available: https://www.hcup-us.ahrq.gov/

## Usage

This public Github repo includes the files for a `streamlit` application.




### Developing with `streamlit`

You'll need to set up a Python environment for working your Streamlit application locally. Streamlit's only officially-supported environment
manager on Windows, macOS, and linux is [Anaconda Navigator](https://docs.anaconda.com/anaconda/navigator/). Please make sure you 
have this installed. (The following is adapted from Streamlit's [documentation](https://docs.streamlit.io/library/get-started/installation).)

#### Create a new Python environment with Streamlit

1.) Follow the steps provided by Anaconda to
[set up and manage your environment](https://docs.anaconda.com/anaconda/navigator/getting-started/#managing-environments) 
using the Anaconda Navigator.

2.) Select the "▶" icon next to your new environment. Then select "Open terminal":

<img width="1024" src="https://i.stack.imgur.com/EiiFc.png">


3.) In the terminal that appears, type:

```bash
pip install streamlit
```

4.) Test that the installation worked:

```bash
streamlit hello
```

Streamlit's Hello app should appear in a new tab in your web browser.


#### Use your new environment

1.) In Anaconda Navigator, open a terminal in your environment (see step 2 above).

2.) In the terminal that appears, navigate to your local workspace and run:

```bash
streamlit run streamlit_app.py
```

This will open the template streamlit app in the web browser. You can now start editing the contents
of `streamlit_app.py`, and refresh the page in your web browser we see changes.
