import pandas as pd
from ccg_imd import generate_ccg_img_table
from dentist import generate_dentist_table
from patient import generate_patient_table


def merge_dentist_ccg_data(accumulate_dentist_table, ccg_imd_table):
    dentist_ccg_table = pd.merge(accumulate_dentist_table, ccg_imd_table, on="CCG code")
    return dentist_ccg_table


def merge_dentist_patient(dentist_table, patient_table):
    single_table = pd.merge(patient_table, dentist_table, on="CCG code", how="outer")
    return single_table


def single_table_finalisation(dentist_table, patient_table):
    single_table = merge_dentist_patient(dentist_table, patient_table)
    population_estimate = population_estimation(single_table)
    single_table["population estimate"] = population_estimate

    single_table = single_table.drop(columns=['Adult', 'Child'])
    return single_table


def population_estimation(single_table):
    population_estimate = []
    for i, row in single_table.iterrows():
        p_e = float(row["number of patients seen"]) / (float(row[row["patient type"]]) / 100 / (2 if row["patient type"] == "Adult " else 1))
        population_estimate.append(p_e)
    return population_estimate


def read_from_unprocessed_data():
    ccg_imd_table = generate_ccg_img_table()
    dentist_table = generate_dentist_table()

    dentist_ccg_table = merge_dentist_ccg_data(dentist_table, ccg_imd_table)
    dentist_ccg_table.to_csv("output_data/dentist.csv", index=False)

    patient_table = generate_patient_table()
    patient_table.to_csv("output_data/patient.csv", index=False)
    return dentist_ccg_table, patient_table


def read_with_input():
    dentist_table = pd.read_csv("output_data/dentist.csv")
    patient_table = pd.read_csv("output_data/patient.csv")
    return dentist_table, patient_table


def main(has_processed=False):
    if has_processed:
        dentist_table, patient_table = read_with_input()
    else:
        dentist_table, patient_table = read_from_unprocessed_data()

    single_table = single_table_finalisation(dentist_table, patient_table)
    single_table.to_csv("output_data/single_table.csv", index=False)
    print(single_table)


def data_analysis():
    single_table = pd.read_csv("output_data/single_table.csv")
    null_table = single_table[single_table["ONS code"].isnull()]
    null_set = set()
    for _, row in null_table.iterrows():
        null_set.add(row["CCG code"])

    print(null_set)


if __name__ == "__main__":
    main()
    # main(True)
    # test()
    # data_analysis()
