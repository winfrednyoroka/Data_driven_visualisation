# In the event of different units, for instance, BMI (kg/m2) vs blood pressure (mmHg), then we have to standardize the values, that is, use sd scaling, where we maximize on the variance of 1, mean centred (mean = 0).

def standard_eucdist(df,muBMI=27.29,muBP =82.29,sdBMI=4.77,sdBP=10.79, x1='ctrlBMI',x2='trtBMI',y1='ctrlBP',y2='trtBP',normx1='norm_ctrlBMI',normx2='norm_trtBMI',normy1='norm_ctrlBP',normy2='norm_trtBP'):
    '''
    The above function takes in the coordinates of the two points with different units of scale
    Standardizes the coordinates before calculating the Euclidean distance using another function.
    It outputs the initial dataframe with an additional four columns
    BP - this will vary (DBP - SBP)
    Average values from UK Biobank

    Parameters:
        - df: - dataframe
        - muBMI: mean BMI in UK biobank
        - muBP: mean DBP/SBP in UK biobank
        - sdBMI: sd of BMI in Uk biobank
        - sdBP: sd of DBP/SBP in UK biobank
        - x1: mean BMI in control arm
        - x2: mean BMI in treatment arm
        - y1: mean DBP/SBP in the control arm
        - y2: mean DBP/SBP in the treatment arm
        - normx1: normalized mean BMI in the control arm
        - normx2: normalized mean BMI in standardized arm
        - normy1: normalized mean DBP/SBP in the control arm
        - normy2: normalized mean DBP/SBP in the treatment arm
    Return:
    A dataframe with four new columns consisting of standardized or normalized BMI and blood pressure in both intervention groups
    '''

    # # Calculate the normalized x1,x2,y1,y2 coordinates
    df[normx1] = df.apply(lambda row: ((row[x1]-muBMI)/sdBMI),axis=1)
    df[normx2] = df.apply(lambda row: ((row[x2]-muBMI)/sdBMI),axis =1)
    df[normy1] = df.apply(lambda row: ((row[y1]-muBP)/sdBP),axis=1)
    df[normy2] = df.apply(lambda row: ((row[y2]-muBP)/sdBP), axis=1)
    
    return df

# Application
# df = standard_eucdist(df,muBMI=27.29,muBP =138.37,sdBMI=4.77,sdBP=19.79,
#                       x1='x1',x2='x2',y1='y1',y2='y2',normx1='norm_ctrlBMI',normx2='norm_trtBMI',normy1='norm_ctrlBP',normy2='norm_trtBP')

# Calculates the Euclidean distances
def df_dist(df,eucl_dist='eucl_dist',normx1='x1',normx2='x2',normy1='y1',normy2='y2'):
    '''
    This function takes in a dataframe with rows and columns
    Computes Euclidean distance between two points

    Parameters:
        - df : Pandas dataframe
        - eucl_dist: new column to contain the Euclidean distances
        - normx1 : x1 coordinate for point 1
        - normx2 : x2 coordinate for point 2
        - normy1 : y1 coordinate for point 1
        - normy2: y2 coordinate for point 2
    Return:
    dataframe with an additional column of Euclidean distances computed from the standardized coordinates
    '''
    df[eucl_dist] = df.apply(lambda row: ((row[normx2]-row[normx1])**2 + (row[normy2]-row[normy1])**2)**(1/2),axis=1)
    return (df)