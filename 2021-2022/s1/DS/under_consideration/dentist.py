import pandas as pd


def pre_dentist_data():
    data_table = pd.read_csv("input_data/NHS Dental Statistics for England 2018-19 Annex3_Workforce.csv")
    filter_by_year = data_table[data_table["Year"] == "2018-19"]
    filter_by_ccg = filter_by_year[filter_by_year["Geography"] == "4.Clinical Commissioning Group"]
    important_data = filter_by_ccg.drop(columns=['Year', 'Geography', 'Parent_Code_1', 'Parent_Code_2',
       'Contract_Type', 'Gender'])
    dentist_table = important_data.rename(columns={"Org_Code": "CCG code", "Age_Group": "dentist age group"})
    return dentist_table


def accumulate_dentist_data(dentist_table):
    accumulate_dentist_dict = dict()
    for _, row in dentist_table.iterrows():
        code = row["CCG code"]
        if code not in accumulate_dentist_dict:
            accumulate_dentist_dict[code] = dict()
        age_group = row["dentist age group"]
        if age_group not in accumulate_dentist_dict[code]:
            count = 0
            filter_ccg_ag = dentist_table[(dentist_table["CCG code"] == code) &
                                          (dentist_table["dentist age group"] == age_group)]
            for _, i in filter_ccg_ag.iterrows():
                count += int(i["Dentist_Count"])

            accumulate_dentist_dict[code][age_group] = count

    ccg_codes = list(accumulate_dentist_dict)
    age_groups = ["Under 35", "35-44", "45-54", "55+"]
    accumulate_table_dict = {"CCG code": [], "dentist age group": [], "number of dentists": []}
    for i in ccg_codes:
        for j in age_groups:
            accumulate_table_dict["CCG code"].append(i)
            accumulate_table_dict["dentist age group"].append(j)
            accumulate_table_dict["number of dentists"].append(accumulate_dentist_dict[i][j])

    accumulate_dentist_table = pd.DataFrame(data=accumulate_table_dict)
    return accumulate_dentist_table


def generate_dentist_table():
    dentist_table = accumulate_dentist_data(pre_dentist_data())
    return dentist_table
