import pandas as pd


def pre_patient_data():
    data_table = pd.read_csv("input_data/nhs-dent-stat-eng-jan-jun-19-anx3-ps-prac.csv")
    filter_by_geo = data_table[data_table["GEOG_TYPE"] == "CCG"]
    filter_by_date = filter_by_geo[filter_by_geo["PSEEN_END_DATE"] == "31/01/2019"]
    important_data = filter_by_date.drop(columns=['PSEEN_END_DATE', 'GEOG_TYPE', 'PRACTICE_CODE', 'PRACTICE_NAME',
       'PRAC_POSTCODE', 'CCG_ONS_CODE', 'CCG_NAME', 'LA_CODE',
       'LA_NAME', 'REGION_LO_CODE', 'REGION_LO_ONS_CODE', 'REGION_LO_NAME',
       'REGION_CODE', 'REGION_ONS_CODE', 'REGION_NAME'])
    patient_table = important_data.rename(columns={"CCG_CODE": "CCG code", "PATIENT_TYPE": "patient type",
                                                   "AGE_BAND": "patient age band",
                                                   "PATIENTS_SEEN": "number of patients seen",
                                                   "POPULATION": "population estimate"})
    return patient_table


def generate_patient_table():
    patient_table = pre_patient_data()
    return patient_table
