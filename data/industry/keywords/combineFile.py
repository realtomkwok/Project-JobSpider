from pandas import ExcelWriter
import glob
import os
import pandas as pd

writer = ExcelWriter("keywords_combined.xlsx")

for filename in glob.glob("separated/*.xlsx"):
    excelFile = pd.ExcelFile(filename)
    (_, f_name) = os.path.split(filename)
    (f_short_name, _) = os.path.splitext(f_name)
    (language, _) = f_short_name.split('_')
    print(language)
    for sheet_name in excelFile.sheet_names:
        df_excel = pd.read_excel(filename, sheet_name=sheet_name)
        df_excel.to_excel(writer, language, index=False)

writer.save()