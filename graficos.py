import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import preprocessing
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold, StratifiedKFold, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_recall_curve, roc_curve, roc_auc_score
from sklearn.metrics import classification_report
import statsmodels.api as sm

from openpyxl import Workbook, load_workbook
# If you need to get the column letter, also import this
from openpyxl.utils import get_column_letter
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

base = '../'
#dadosFinais2007_6Mat nmome da planilha principal
df = pd.read_excel(base + 'DADOS_0704.xlsx', 'dadosFinais2007_5Mat')
print(df.columns)


#gráficos
print(df)
plt.title('Grafico Nota LMD')
plt.hist(df["nota LMD"], bins= 20)
plt.savefig('C:\\Users\\guilh\\Desktop\\Iniciação Científica\\prints\\graficos1995\\grafico-lmd')
plt.close()
