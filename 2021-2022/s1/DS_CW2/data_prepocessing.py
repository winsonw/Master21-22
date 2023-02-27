import pandas as pd
from ccg_imd import generate_ccg_img_table
from dentist import generate_dentist_table
from patient import generate_patient_table
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
import numpy as np



def merge_patient_ccg_data(patient_table, ccg_imd_table):
    patient_ccg_table = pd.merge(patient_table, ccg_imd_table, on="CCG code", how="outer")
    return patient_ccg_table


def merge_dentist_patient(dentist_table, patient_table):
    single_table = pd.merge(patient_table, dentist_table, on="CCG code", how="outer")
    return single_table


def read_with_input():
    dentist_table = pd.read_csv("output_data/dentist.csv")
    patient_table = pd.read_csv("output_data/patient.csv")
    return dentist_table, patient_table


def main(has_processed=False):
    if has_processed:
        dentist_table, patient_table = read_with_input()
    else:
        dentist_table, patient_table = read_from_unprocessed_data()

    print(len(dentist_table))
    print(len(patient_table))
    single_table = merge_dentist_patient(dentist_table, patient_table)
    print(len(single_table))
    single_table.to_csv("output_data/single_table.csv", index=False)


def data_analysis_1():
    single_table = pd.read_csv("output_data/single_table.csv")

    old_dentist_dict = dict()
    total_dentist_dict= dict()
    imd_dict = dict()
    ccg_dict = set()
    for _, row in single_table.iterrows():
        ccg_code = row["CCG code"]
        if ccg_code != "Unallocated":
            ccg_dict.add(ccg_code)
            if ccg_code not in total_dentist_dict:
                total_dentist_dict[ccg_code] = 0.0
                old_dentist_dict[ccg_code] = 0.0
            total_dentist_dict[ccg_code] += float(row["number of dentists"])
            if row["dentist age group"] == "55+":
                old_dentist_dict[ccg_code] += float(row["number of dentists"])
            imd_dict[ccg_code] = row["average IMD score"]

    x = []
    y = []
    cluster = None
    for ccg_code in ccg_dict:
        p = old_dentist_dict[ccg_code] / total_dentist_dict[ccg_code]
        imd = imd_dict[ccg_code]
        x.append(p)
        y.append(imd)
        if cluster is None:
            cluster = np.array([[p, imd]])
        else:
            cluster = np.append(cluster, [[p,imd]], axis=0)
    kmean = SpectralClustering(n_clusters=3).fit(cluster)

    c = [[[], []], [[], []], [[], []]]
    label = kmean.labels_
    print(cluster)
    print(label)
    print(len(label))
    print(len(x))
    for i in range(len(label)):
        c[label[i]][0].append(x[i])
        c[label[i]][1].append(y[i])

    plt.plot(c[0][0], c[0][1], "ob", color="g")
    plt.plot(c[1][0], c[1][1], "ob", color="r")
    plt.plot(c[2][0], c[2][1], "ob", color="b")

    plt.xlabel("%")
    plt.ylabel("imd")
    plt.show()
    plt.close()

import pandas

def data_analysis():
    patient_num_dict()

def patient_num_dict():
    single_table = pd.read_csv("output_data/single_table.csv")
    total=[]
    age=sorted(single_table['patient age band'].unique(),key=str.lower)
    patient_total=single_table.copy()
    for a in age:
      df_ccg = patient_total[(patient_total['patient age band']==a) & (patient_total["CCG code"] != "Unallocated")]
      sum_ccg = df_ccg['number of patients seen'].sum()
      df_una = patient_total[(patient_total['patient age band']==a) & (patient_total["CCG code"] == "Unallocated")]
      sum = sum_ccg/4 + df_una['number of patients seen'].sum()
      b=[]
      b.append(a)
      b.append(sum/4)
      total.append(b)
    df1 = pandas.DataFrame(total, columns=['patient age band', 'total num'])
    df1['patient age band']=pandas.to_numeric( df1['patient age band'], errors='coerce')
    df2 = df1.sort_values(by="patient age band",kind='mergesort')
    # df2[["patient age band"]] = df2[["patient age band"]].astype(str)
    # df2.loc[10,'patient age band']='18+'
    #加上这两行就是加上18+的数据


    return df2



def read_from_unprocessed_data():
    ccg_imd_table = generate_ccg_img_table()
    dentist_table = generate_dentist_table()
    patient_table = generate_patient_table()

    patient_ccg_table = merge_patient_ccg_data(patient_table, ccg_imd_table)
    # patient_ccg_table.to_csv("output_data/test.csv", index=False)

    dentist_table.to_csv("output_data/dentist.csv", index=False)
    patient_ccg_table.to_csv("output_data/patient.csv", index=False)

    return dentist_table, patient_ccg_table



if __name__ == "__main__":
    # main()
    # main(True)
    # test()
    data_analysis()
