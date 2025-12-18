#Loading the libraries
import streamlit as st
import pandas as pd
import numpy as np
import scipy
from scipy.stats import ttest_ind_from_stats

st.markdown(":blue[Hypothesis testing]")
st.text("""We are trying to answer the question of is the observed euclidean distance at baseline significant,
        why because on adding the CIs there is sgnificant overlap of the imprecuise CIs.
        We performed an independent t-test to try and estimate whether indeed the observed differences are true or just by chance.
        We estimated these using normalised Euclidena distance and are reorting P-values for both the BMI and the DBP""")

st.sidebar.markdown("Hypothesistesting results")

#Create the tabs later

# Read in the data first and preprocess using pandas
BMI_DBP_Euc = pd.read_csv('Data/DBP_baseline_normalizedeucdist.csv') # Read in the dataset using relative paths
st.write("First 5 rows:")
st.dataframe(BMI_DBP_Euc.head()) # view the firts five rows of the data
st.write("\nColumn names of the data:")
BMI_DBP_Euc.columns # retrieve the column names for the next step

# Check the data structure
#st.write("Dataframe info:")
#st.dataframe(BMI_DBP_Euc.info())

st.write("Slice specific columns and rename:")
BMI_DBP_norm_EUC = BMI_DBP_Euc[['Author_pmid', 'standardizedeucl_dist']] # slice data and just extract the two columns only
BMI_DBP_norm_EUC.rename(columns={'standardizedeucl_dist':'Euc_dist'}, inplace=True) # renaming one of the column names
st.write("\nView first 5 rows")
st.dataframe(BMI_DBP_norm_EUC.head())

# Load the data with all baseline measures
# Load the previous dataset for BMI and DBP measures at baseline
BMI_DBP = pd.read_csv("Data/Study_Pop_BMI_DBP_V1.csv")
st.dataframe(BMI_DBP.head()) # view the first 5 rows
 # Choose a few columns
df = BMI_DBP[['Author_pmid', 'intervention_control', 'totalsamplesize','meanBMI', 'meanBMI_sd', 'meanDBP',
              'meanDBP_sd','durationofstudy']] # select a few desired columns
st.dataframe(df)

# Read in the population characteristics and extract exact sample sizes for each arm
study_pop =pd.read_csv("Data/study_population.csv")
study_pop.columns
dat =study_pop[['Sample(n)','pmid','author', 'extracted_portion','intervention_control']]
# dat
# 1. Split the author column
dat.loc[:, 'lname'] = dat['author'].str.strip().str.split(' ').str[-1] # Remove white spaces,split by space and extract last section
dat = dat.copy() # Explicitly copy the dataset
# 2. Merge lname with pmid separated by underscore (_)
dat.loc[:,'Author_pmid'] = dat['lname'] + '_'+ dat['pmid'].astype(str)
dat
# Duplicate rows
rows_to_duplicate = dat.loc[[4, 20, 37]]

# Append to original DataFrame
dat = pd.concat([dat, rows_to_duplicate], ignore_index=True)

dat=dat.copy()
# 3. Update the labels for 3-arm studies
# row[4-a,5-a,6-b,19-a,20-a,21-b,37-a,38-b,39-a,44-b,45-b,46-b]
# use suffix
# Indexes to update and corresponding suffixes
index_suffix_map = {
    4: '_a', 5: '_a', 6:'_b',19:"_a",20:"_a",21:"_b",
    37:"_a",38:"_b",39:"_a",44:"_b",45:"_b",46:"_b"
}

# Apply suffix updates
for idx, suffix in index_suffix_map.items():
    dat.loc[idx, 'Author_pmid'] = f"{dat.loc[idx, 'Author_pmid']}{suffix}"

#dat

# Subset the two columns to be merged with BMI_DBP_baseline 
# dat = dat[['Author_pmid','Sample(n)','intervention_control']]

#dat
dat_treat =  dat[dat['intervention_control']=='intervention'] # Extract the treated
#dat_treat
dat_control =  dat[dat['intervention_control']=='control'] # Extract the treated
#dat_control 

st.markdown("Data preparation for t-test")
st.write("1. Filter by duration of study, baseline = 0")
BMI_DBP_T0 = df[df['durationofstudy'] == 0].copy()
#BMI_DBP_T0_up = pd.merge(BMI_DBP_T0,dat,on='Author_pmid') #merge to obtain arm samplesize
#print(BMI_DBP_T0)
#print(BMI_DBP_T0)
st.write("2. Standardise the intervention-control entries to lowercase and no extra white spaces")
BMI_DBP_T0['intervention_control'] = df['intervention_control'].str.lower().str.strip()
#BMI_DBP_T0
df = BMI_DBP_T0.copy()
st.write("3. Rename columns to control and treated arm")
### Extract treated and rename the columns
BMI_DBP_T0_treat =  BMI_DBP_T0[BMI_DBP_T0['intervention_control']=='intervention'] # Extract the treated
BMI_DBP_T0_treat = pd.merge( BMI_DBP_T0_treat,dat_treat,how='inner',on='Author_pmid') # Merge with study characteristics
BMI_DBP_T0_treat = BMI_DBP_T0_treat.rename(columns={'Sample(n)':'n_treat','meanBMI':'mean_bmi_treat',
                                                    'meanBMI_sd':'sd_bmi_treat', 'meanDBP':'mean_dbp_treat',
                                                    'meanDBP_sd':'sd_dbp_treat'})
BMI_DBP_T0_treat.drop(['intervention_control_x','intervention_control_y','durationofstudy'], axis=1, inplace=True)
BMI_DBP_T0_treat
### Extract control
BMI_DBP_T0_control =  BMI_DBP_T0[BMI_DBP_T0['intervention_control']=='control']
BMI_DBP_T0_control= pd.merge(BMI_DBP_T0_control,dat_control,how='inner',on='Author_pmid') #merge with study characteristics

BMI_DBP_T0_control = BMI_DBP_T0_control.rename(columns={'Sample(n)':'n_ctrl','meanBMI':'mean_bmi_ctrl',
                                                    'meanBMI_sd':'sd_bmi_ctrl', 'meanDBP':'mean_dbp_ctrl',
                                                    'meanDBP_sd':'sd_dbp_ctrl'})
BMI_DBP_T0_control.drop(['intervention_control_x','intervention_control_y','durationofstudy'], axis=1, inplace=True)
BMI_DBP_T0_control

st.write("4. Merge the two dataframes side by side treated and control")

BMI_DBP_T0_trt_ctrl = pd.merge(BMI_DBP_T0_treat,BMI_DBP_T0_control, on='Author_pmid')
BMI_DBP_T0_trt_ctrl
st.write("5. Merge above dataset with the Euclidean distance")
BMI_DBP_T0_trt_ctrl_EUC=pd.merge(BMI_DBP_T0_trt_ctrl,BMI_DBP_norm_EUC,on='Author_pmid')
print(BMI_DBP_T0_trt_ctrl_EUC)
st.write("6. Perform independent t-test")

st.write('A function for calculating the independent t-test using scipy library')
#Function
# Optional loading of libraries since they are already loaded at the top of the script
# import pandas as pd
# import numpy as np
# from scipy.stats import ttest_ind_from_stats
def add_ttest_pvalues(df, 
                      mean1_col, std1_col, 
                      mean2_col, std2_col, 
                      n1, n2, 
                      new_col_name='p_value'):
    """
    Adds a column with t-test p-values based on group summary stats.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        mean1_col (str): Column name for group 1 mean.
        std1_col (str): Column name for group 1 SD.
        mean2_col (str): Column name for group 2 mean.
        std2_col (str): Column name for group 2 SD.
        n1 (str): Sample size for group 1.
        n2 (str): Sample size for group 2.
        new_col_name (str): Name for new p-value column.

    Returns:
        pd.DataFrame: DataFrame with additional column of p-values.
    """
    df[new_col_name] = df.apply(lambda row: ttest_ind_from_stats(
        mean1=row[mean1_col], std1=row[std1_col], nobs1=row[n1],
        mean2=row[mean2_col], std2=row[std2_col], nobs2=row[n2]
    ).pvalue if not pd.isnull(row[std1_col]) and not pd.isnull(row[std2_col]) else np.nan, axis=1)
    
    return df
st.write('Calculate the p-value for BMI covariate:')
df_pval = add_ttest_pvalues(
    df=BMI_DBP_T0_trt_ctrl_EUC,
    mean1_col='mean_bmi_treat',
    std1_col='sd_bmi_treat',
    mean2_col='mean_bmi_ctrl',
    std2_col='sd_bmi_ctrl',
    n1='n_treat',
    n2='n_ctrl',
    new_col_name='p_bmi'
)
df_pval
st.write('Use the dataframe from above to calculate the p-value associted with the DBP:')
df_pval = add_ttest_pvalues(
    df=df_pval,
    mean1_col='mean_dbp_treat',
    std1_col='sd_dbp_treat',
    mean2_col='mean_dbp_ctrl',
    std2_col='sd_dbp_ctrl',
   n1='n_treat',
    n2='n_ctrl',
    new_col_name='p_dbp'
)
df_pval

#df_pval.to_csv('./derived/BMI_DBP_EUC_pBMI_pDBP.csv')
st.write("\nFinal results including the Euc_dist, p-values for BMI and DBP covariates")
df_pval