import pandas as pd
import collections


xls = pd.ExcelFile('../../../data/raw/f2g/TUcases_1 to150.xlsx')
df1 = pd.read_excel(xls, 'selected features', header=0).astype(str)
df2 = pd.read_excel(xls, 'selected syndromes', header=0).astype(str)

df_feature_name = df1.groupby("case_id")['feature_name'].apply(lambda feature_name: ';'.join(feature_name)).to_frame()
df_feature_id = df1.groupby("case_id")['hpo_id'].apply(lambda hpo_id: ';'.join(hpo_id)).to_frame()
df_is_present = df1.groupby("case_id")['is_present'].apply(lambda is_present: ';'.join(is_present)).to_frame()
df_syndrome_name = df2.groupby("case_id")['syndrome_name'].apply(lambda syndrome_name: ';'.join(syndrome_name)).to_frame()
df_omim_id = df2.groupby("case_id")['omim_id'].apply(lambda omim_id: ';'.join(omim_id)).to_frame()
df_diagnosis = df2.groupby("case_id")['diagnosis'].apply(lambda diagnosis: ';'.join(diagnosis)).to_frame()

df_merged = df_feature_name \
    .merge(df_feature_id, on='case_id') \
    .merge(df_is_present, on='case_id') \
    .merge(df_syndrome_name, on='case_id') \
    .merge(df_omim_id, on='case_id') \
    .merge(df_diagnosis, on='case_id')

export_csv = df_merged.to_csv('../../../data/processed/f2g/TUcases_1to150_transformed.csv', index=True, header=True, sep='\t')


