import pandas as pd


def pre_ccg_data():
    data_table = pd.read_excel("input_data/nhs-dent-stat-eng-18-19-anx2.xlsx", "A4")
    # notnull here is just for format issue, all info remains
    filter_by_notnull = data_table[data_table["Unnamed: 1"].notnull()]
    ccg_table = filter_by_notnull.drop(9)
    ccg_table = ccg_table.drop(columns=["Unnamed: 0", "Unnamed: 6", "Unnamed: 7", "Unnamed: 8",
                                        "Unnamed: 9", "Unnamed: 10"])
    ccg_table = ccg_table.rename(columns={"Unnamed: 1": "ONS code", "Unnamed: 2": "CCG code", "Unnamed: 3": "name",
                                          "Unnamed: 4": "Adult", "Unnamed: 5": "Child"})
    ccg_table = ccg_table.reset_index()

    return ccg_table


def pre_imd_data():
    data_table = pd.read_excel("input_data/File_13_-_IoD2019_Clinical_Commissioning_Group__CCG__Summaries.xlsx", "IMD")
    imd_table = data_table.rename(columns={"Clinical Commissioning Group Code (2019)": "ONS code",
                                           "IMD - Average score": "average IMD score"})
    imd_table = imd_table.drop(columns=['Clinical Commissioning Group Name (2019)', 'IMD - Average rank',
       'IMD - Rank of average rank',
       'IMD - Rank of average score',
       'IMD - Proportion of LSOAs in most deprived 10% nationally',
       'IMD - Rank of proportion of LSOAs in most deprived 10% nationally',
       'IMD 2019 - Extent', 'IMD 2019 - Rank of extent',
       'IMD 2019 - Local concentration',
       'IMD 2019 - Rank of local concentration'])
    return imd_table


def merge_ccg_img_table(ccg_table, imd_table):
    ccg_imd_table = pd.merge(ccg_table, imd_table, on="ONS code")
    ccg_imd_table = ccg_imd_table.drop(columns=["index"])
    return ccg_imd_table


def generate_ccg_img_table():
    ccg_table = pre_ccg_data()
    imd_table = pre_imd_data()
    ccg_imd_table = merge_ccg_img_table(ccg_table, imd_table)
    return ccg_imd_table
