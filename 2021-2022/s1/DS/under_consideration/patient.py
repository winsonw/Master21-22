import pandas as pd


def pre_patient_data_early_2018_adult():
    data_table_adult = pd.read_csv("input_data/nhs-dent-stat-eng-17-18-anx3-clin.csv")
    filter_by_geo = data_table_adult[data_table_adult["Geography"] == "NHS"]
    filter_by_quarter = filter_by_geo[filter_by_geo["Quarter"] == 2]
    filter_by_type = filter_by_quarter[filter_by_quarter["Patient_Type"] == "Adult"]
    important_data = filter_by_type.drop(columns=['FY_Ending', 'Quarter', 'Geography', 'Parent_Code1',
       'Parent_Code2', 'Treatment_Band', 'Clinical_Treatment'])
    patient_early_2018_adult = important_data.rename(columns={"Org_Code": "CCG code", "Patient_Type": "patient type",
                                                              "Count": "patient seen"})
    patient_early_2018_adult["patient age band"] = "18+"
    return patient_early_2018_adult


def pre_patient_data_early_2018_child():
    data_table_child = pd.read_csv("input_data/nhs-dent-stat-eng-17-18-anx3-child-ps.csv")
    filter_by_geo = data_table_child[data_table_child["GEOGRAPHY"] == "NHS"]
    filter_by_meas = filter_by_geo[filter_by_geo['MEASURE'] == "CHILD_PSEEN"]
    allowed_date = ["30-Apr-18", "31-May-18", "30-Jun-18"]
    filter_by_date_list = []
    for i in allowed_date:
        filter_by_date_list.append(filter_by_meas[filter_by_meas["PATIENT_SEEN_END_DATE"] == i])
    filter_by_date = pd.concat(filter_by_date_list)
    important_data = filter_by_date.drop(columns=['PATIENT_SEEN_END_DATE', 'GEOGRAPHY',  'PARENTCODE1',
       'PARENTCODE2', 'MEASURE'])
    patient_child = important_data.rename(columns={"ORG_CODE": "CCG code", "AGE": "patient age band",
                                                   "VALUE": "patient seen"})
    patient_child["patient type"] = "Child"
    return patient_child


def pre_patient_data_late_2018():
    data_table_18 = pd.read_csv("input_data/nhs-dent-stat-eng-jul-dec-18-anx3-ps-prac.csv")
    filter_by_geo_type_18 = data_table_18[data_table_18["GEOTYPE"] == "CCG"]
    allowed_date_18 = ["31/07/2018", "31/08/2018", "30/09/2018", "31/10/2018", "30/11/2018", "31/12/2018"]
    filter_by_date_list_18 = []
    for i in allowed_date_18:
        filter_by_date_list_18.append(filter_by_geo_type_18[filter_by_geo_type_18["PSEEN_END_DATE"] == i])
    filter_by_date_18 = pd.concat(filter_by_date_list_18)
    important_data = filter_by_date_18.drop(columns=['PSEEN_END_DATE', 'GEOTYPE', 'PRACTICE_CODE', 'PRACTICE_NAME',
       'PRAC_POSTCODE', 'CCG_ONS_CODE', 'CCG_NAME', 'LA_CODE',
       'LA_NAME', 'REGION_LO_CODE', 'REGION_LO_ONS_CODE', 'REGION_LO_NAME',
       'REGION_CODE', 'REGION_ONS_CODE', 'REGION_NAME', 'POPULATION'])

    patient_table_2018 = important_data.rename(columns={"CCG_CODE": "CCG code", "PATIENT_TYPE": "patient type",
                                                   "AGE_BAND": "patient age band", "PATIENTS_SEEN": "patient seen"})
    return patient_table_2018


def pre_patient_data_2019():
    data_table_19 = pd.read_csv("input_data/nhs-dent-stat-eng-jan-jun-19-anx3-ps-prac.csv")
    filter_by_geo_type_19 = data_table_19[data_table_19["GEOG_TYPE"] == "CCG"]
    allowed_date_19 = ["31/01/2019", "28/02/2019", "31/03/2019"]
    filter_by_date_list_19 = []
    for i in allowed_date_19:
        filter_by_date_list_19.append(filter_by_geo_type_19[filter_by_geo_type_19["PSEEN_END_DATE"] == i])
    filter_by_date_19 = pd.concat(filter_by_date_list_19)
    important_data = filter_by_date_19.drop(columns=['PSEEN_END_DATE', 'GEOG_TYPE', 'PRACTICE_CODE', 'PRACTICE_NAME',
       'PRAC_POSTCODE', 'CCG_ONS_CODE', 'CCG_NAME', 'LA_CODE',
       'LA_NAME', 'REGION_LO_CODE', 'REGION_LO_ONS_CODE', 'REGION_LO_NAME',
       'REGION_CODE', 'REGION_ONS_CODE', 'REGION_NAME', 'POPULATION'])

    patient_table_2019 = important_data.rename(columns={"CCG_CODE": "CCG code", "PATIENT_TYPE": "patient type",
                                                   "AGE_BAND": "patient age band", "PATIENTS_SEEN": "patient seen"})

    return patient_table_2019


def get_patient_data_early_2018():
    patient_adult = pre_patient_data_early_2018_adult()
    patient_child = pre_patient_data_early_2018_child()

    patient_early_2018 = pd.concat([patient_adult, patient_child])

    return patient_early_2018


def accumulate_patient_data(patient_table):
    accumulate_patient_dict = dict()
    age_groups = set()
    for _, row in patient_table.iterrows():
        code = row["CCG code"]
        if code not in accumulate_patient_dict:
            accumulate_patient_dict[code] = dict()
        age_group = row["patient age band"]
        age_groups.add(age_group)
        if age_group not in accumulate_patient_dict[code]:
            count = 0
            filter_ccg = patient_table[(patient_table["CCG code"] == code)]
            filter_ag = filter_ccg[filter_ccg["patient age band"] == age_group]
            for _, i in filter_ag.iterrows():
                count += int(i["patient seen"])

            accumulate_patient_dict[code][age_group] = count

    print(accumulate_patient_dict)

    print(age_groups)

    ccg_codes = list(accumulate_patient_dict)
    accumulate_table_dict = {"CCG code": [], "patient age band": [], "number of patients seen": [], "patient type": []}
    for i in ccg_codes:
        for j in age_groups:
            accumulate_table_dict["CCG code"].append(i)
            accumulate_table_dict["patient age band"].append(j)
            accumulate_table_dict["patient type"].append("Adult" if j == "18+" else "Child")
            accumulate_table_dict["number of patients seen"].append(accumulate_patient_dict[i][j])

    accumulate_patient_table = pd.DataFrame(data=accumulate_table_dict)
    return accumulate_patient_table


def get_patient_data():
    filter_by_date_18_early = get_patient_data_early_2018()
    filter_by_date_18 = pre_patient_data_late_2018()
    filter_by_date_19 = pre_patient_data_2019()

    patient_table = pd.concat([filter_by_date_18_early, filter_by_date_18, filter_by_date_19])
    patient_table["patient age band"] = patient_table["patient age band"].astype(str)
    return patient_table


def generate_patient_table():
    patient_table = get_patient_data()
    accumulate_patient_table = accumulate_patient_data(patient_table)
    return accumulate_patient_table
