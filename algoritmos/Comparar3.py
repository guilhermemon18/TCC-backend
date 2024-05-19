from collections import Counter

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

from src.pre_processamento_dados.codificacao import codificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30

df = get_dataframe_gr30()
df = codificar_dataframe(df)

X = df.drop('Situação', axis=1).values
y = df['Situação'].values


print('Original dataset shape %s' % Counter(y))

# # NearMiss
# nm = NearMiss()
# X, y = nm.fit_resample(X, y)

# ada = ADASYN(random_state=42)
# X, y = ada.fit_resample(X, y)

# # OneSidedSelection (Algoritmo tipo KNN)
# oss = OneSidedSelection(random_state=42)
# X, y = oss.fit_resample(X, y)
#
# # Random Undersampler
# rus = RandomUnderSampler(random_state=42)
# X, y = rus.fit_resample(X, y)

# SMOTE
smote = SMOTE(random_state=42)
X, y = smote.fit_resample(X, y)

print('Resampled dataset shape %s' % Counter(y))

# Criar instâncias dos modelos
decision_tree = DecisionTreeClassifier(random_state=42)
random_forest = RandomForestClassifier(random_state=42)
logistic_regression = LogisticRegression(max_iter=10000, random_state=42)  # ajuste o número máximo de iterações conforme necessário

# Lista dos modelos
models = [decision_tree, random_forest, logistic_regression]
model_names = ['Decision Tree', 'Random Forest', 'Logistic Regression']

# Realizar validação cruzada para cada modelo
for model, name in zip(models, model_names):
    scores = cross_val_score(model, X, y, cv=5)  # cv é o número de folds para validação cruzada
    print(f'{name}: Média da acurácia = {scores.mean():.2f}, Desvio padrão da acurácia = {scores.std():.2f}')
