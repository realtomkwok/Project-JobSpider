# -*- coding: UTF-8 -*-

import numpy
import pandas as pd
import jieba
import jieba.analyse
import codecs

def keywordFilter(language):
    filePath = 'data/data_sheets/processed/by_language/' + language + '.xlsx'
    #Import the Excel sheet and create a dataframe
    df = pd.read_excel(filePath, header=0, encoding='utf-8', dtype='str')
    #Create a dataframe for column 'industry'
    indDf = df[['industry']]
    #Create a temporate file to store these data for the next step
    tempDf = indDf.groupby('industry').size().reset_index(name='counts')
    tempDf.to_excel('temp.xlsx')

    rows = pd.read_excel('temp.xlsx', encoding='utf-8', dtype='str')
    segments = []

    for index, row in rows.iterrows():
        content = row[1]
        words = jieba.analyse.textrank(content, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
        splitedStr = ''

        for word in words:
            segments.append({'keyword': word, 'count': 1})
            splitedStr += word + ' '

    dfSg = pd.DataFrame(segments)
    dfWord = dfSg.groupby('keyword')['count'].sum()
    dfWord.to_excel('source_code/word_frequency/outputs/{}_keywords.xlsx'.format(language), encoding='utf-8')
    print("Keywords of {} has been sucessfully analysed!".format(language))

languages = ['C#', 'C++', 'Java', 'HTML+CSS', 'JavaScript', 'PHP', 'Python', 'Ruby', 'Swift', 'TypeScript']
for language in languages:
    keywordFilter(language)
