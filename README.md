# Data-driven visualisation tool to guide sensitivity analysis for Randomised Controlled Trial evidence synthesis

## Motivation
Increasingly, randomisation to a treatment or placebo is being used for instrumental variable (IV) analysis in Randomized Controlled Trials (RCTs) for evidence triangulation.
In our applied example of triangulating Mendelian randomisation (Mr) and RCTs evidence, we noted a high level of heterogeneity among surgical trials in which we were synthesising evidence. Our main assumption is that randomisation ought to be done correctly so that we can use it as an IV instrument. Variables of interest that would be useful for metaregression analysis are poorly reported across the studies, a good example being antihypertensive drug use for participants with hypertension. As a result, we envisioned visualising the baseline characteristics. Specifically the exposure and the outcome, which is our key measure to compute the estimand of interest, would provide interesting findings to guide researchers with further work.

Despite RCTs reporting in the publications that randomisation was done, we have observed many differences within and between studies. 
We acknowledge that bias could arise from so many other areas, not just failed randomisation. 

## Relevance
However, we aim to provide a data-driven visualisation approach that will help other researchers make careful considerations about whether to progress with metaanalysis and will also be useful in guiding sensitivity analysis.


##  Implementation
We used Pandas for data wrangling and altair for visualisation.
We have implemented the code and deployed it as a web app using streamlit v1.36.0, where the data is provided side by side with the visualisations showing the baseline measures for the treatment arms.
We have provided the data from our work for reproducibility.
We have deposited all scripts that we used in this repository, including the Jupyter Notebook and streamlit web app. 
The figures we generated are also in the repo. However, they are available in the app.


## Software
NB: Use the latest versions of the software.

`Pandas v2.2.2`

`Altair v5.3.0`

`Streamlit v1.36.0`

`Python 3.12.0`

`Jupyter Notebook or jupyter lab`

## Usage

#### Web
Use the link here to access the deployed app showing the data and the resultant figures {*To embed a hyperlink once we agree on deploying the app*}.

#### Locally

1. Git clone the repository to target OS.

2. Create a conda environment as follows.
   
   `conda env create -f data_vis.yml`
   
4. Activate the conda environment
   
   `Conda activate env_name`
   
- Launch the jupyter lab or notebook run the `.ipynb file` and run the cells.
- Use the streamlit `streamlit run BMI_DBP_main_app.py` to launch the multipage web app.


   


**Authors**
- Winfred N Gatua
- Maria Sobczyk
- Yi Liu
- Deborah Lawlor
- Tom Gaunt
