import pandas as pd

# cancatenate 6 disease excel and choose columns of case_id, syndrome_name, omim_id, diagnosis
df1 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases1_disease.xlsx', header=0, converters={'case_id':str, 'omim_id':str})[['case_id', 'syndrome_name', 'omim_id', 'diagnosis']]
df2 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases2_disease.xlsx', header=0, converters={'case_id':str, 'omim_id':str})[['case_id', 'syndrome_name', 'omim_id', 'diagnosis']]
df3 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases3_disease.xlsx', header=0, converters={'case_id':str, 'omim_id':str})[['case_id', 'syndrome_name', 'omim_id', 'diagnosis']]
df4 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases4_disease.xlsx', header=0, converters={'case_id':str, 'omim_id':str})[['case_id', 'syndrome_name', 'omim_id', 'diagnosis']]
df5 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases5_disease.xlsx', header=0, converters={'case_id':str, 'omim_id':str})[['case_id', 'syndrome_name', 'omim_id', 'diagnosis']]
df6 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases6_disease.xlsx', header=0, converters={'case_id':str, 'omim_id':str})[['case_id', 'syndrome_name', 'omim_id', 'diagnosis']]
df_diseases = pd.concat([df1, df2, df3, df4, df5, df6])

# remove duplicated
df_diseases = df_diseases.drop_duplicates()

# remove patients with multiple diseases
df_diseases = df_diseases.groupby('case_id').filter(lambda x: len(x) == 1)

# remove patient with a disease from differential diagnosis
df_diseases = df_diseases.loc[df_diseases['diagnosis'] != 'DIFFERENTIAL_DIAGNOSIS']

#fillna of omim id
df_diseases[['omim_id']]=  df_diseases[['omim_id']].fillna('unknown')

#seperate patients with known and unknown omim disease
unknownOmim = ['unknown', '0']
df_unknownOmim = df_diseases.loc[df_diseases['omim_id'].isin(unknownOmim)]
df_knownOmim = df_diseases.loc[~df_diseases['omim_id'].isin(unknownOmim)]

# cancatenate 6 feature excel and delect unpresent features
df1 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases1_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df1 = df1.loc[df1['is_present'] == '1'].drop(columns=['is_present'])
df2 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases2_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df2 = df2.loc[df2['is_present'] == '1'].drop(columns=['is_present'])
df3 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases3_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df3 = df3.loc[df3['is_present'] == '1'].drop(columns=['is_present'])
df4 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases4_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df4 = df4.loc[df4['is_present'] == '1'].drop(columns=['is_present'])
df5 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases5_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df5 = df5.loc[df5['is_present'] == '1'].drop(columns=['is_present'])
df6 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases6_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df6 = df6.loc[df6['is_present'] == '1'].drop(columns=['is_present'])
df_features = pd.concat([df1, df2, df3, df4, df5, df6])
# join features of a patient into a new column
df_features = df_features.groupby(by="case_id", as_index=False).agg(','.join)

# cancatenate 6 feature excel of unpresent features
df1 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases1_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df1 = df1.loc[df1['is_present'] == '0'].drop(columns=['is_present'])
df2 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases2_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df2 = df2.loc[df2['is_present'] == '0'].drop(columns=['is_present'])
df3 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases3_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df3 = df3.loc[df3['is_present'] == '0'].drop(columns=['is_present'])
df4 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases4_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df4 = df4.loc[df4['is_present'] == '0'].drop(columns=['is_present'])
df5 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases5_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df5 = df5.loc[df5['is_present'] == '0'].drop(columns=['is_present'])
df6 = pd.read_excel('../../../../../../data/raw/patients/f2g/TUcases6_features.xlsx', header=0, converters={'case_id':str, 'is_present':str})[['case_id', 'hpo_id', 'is_present']]
df6 = df6.loc[df6['is_present'] == '0'].drop(columns=['is_present'])
df_absent_features = pd.concat([df1, df2, df3, df4, df5, df6])
df_absent_features = df_absent_features.groupby(by="case_id", as_index=False).agg(','.join)

# merge disease and feature information of patients of known omim disease!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
df_combined_knownOmim = pd.merge(df_knownOmim, df_features, how='left', on='case_id').dropna()
df_combined_knownOmim['Gene'] = 'unknown'
df_combined_knownOmim = pd.merge(df_combined_knownOmim, df_absent_features, how='left', on='case_id').fillna('unknown')
df_combined_knownOmim.to_csv('../../../../../../data/raw/patients/f2g/tucases_patient_disease_feature.tsv', sep='\t', index=False, header=False)

df_combined_knownOmim.iloc[:, 0] = 'Patient:' + df_combined_knownOmim.iloc[:, 0]
df_combined_knownOmim.iloc[:, 2] = 'OMIM:' + df_combined_knownOmim.iloc[:, 2]

df_combined_knownOmim.iloc[:, [0, 2, 4, 5, 6]].to_csv('../../../../../../data/processed/patients/reform/f2g/f2g_tucases.tsv', sep ='\t', index=False, header=False)

#merge disease and feature information of patients of unknown omim disease
df_combined_unknownOmim = pd.merge(df_unknownOmim, df_features, how='left', on='case_id').dropna()
df_combined_unknownOmim['Gene'] = 'unknown'
df_combined_knownOmim = pd.merge(df_combined_unknownOmim, df_absent_features, how='left', on='case_id').fillna('unknown')
df_combined_unknownOmim.to_csv('../../../../../../data/raw/patients/f2g/tucases_patient_unknownOmimDisease_feature.tsv', sep='\t', index=False)

