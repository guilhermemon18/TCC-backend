from collections import Counter

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import NearMiss, OneSidedSelection, RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import cross_validate, StratifiedKFold, train_test_split, cross_val_predict
from sklearn.tree import DecisionTreeClassifier
from src.pre_processamento_dados.codificacao import codificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30


# Carregar e preprocessar os dados
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


# Definir modelos
models = {
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Logistic Regression': LogisticRegression(solver='liblinear', max_iter=10000, random_state=42)
}

# Definir métricas para avaliação
scoring = {
    'accuracy': 'accuracy',
    'precision': 'precision_weighted',
    'recall': 'recall_weighted',
    'f1': 'f1_weighted',
    'roc_auc': 'roc_auc_ovr_weighted'
}

# Realizar validação cruzada para cada modelo
for name, model in models.items():
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    cv_results = cross_validate(model, X, y, cv=skf, scoring=scoring, return_train_score=False)

    # Exibir resultados da validação cruzada
    print(f'{name}:')
    print(f"   Média da Acurácia: {np.mean(cv_results['test_accuracy']):.4f}")
    print(f"   Média da Acurácia: {cv_results['test_accuracy'].mean():.2f} ± {cv_results['test_accuracy'].std():.2f}")
    print(f"   Média da Precisão: {cv_results['test_precision'].mean():.2f} ± {cv_results['test_precision'].std():.2f}")
    print(f"   Média do Recall: {cv_results['test_recall'].mean():.2f} ± {cv_results['test_recall'].std():.2f}")
    print(f"   Média do F1-score: {cv_results['test_f1'].mean():.2f} ± {cv_results['test_f1'].std():.2f}")
    print(f"   Média da Área sob a Curva ROC: {cv_results['test_roc_auc'].mean():.2f} ± {cv_results['test_roc_auc'].std():.2f}")
    print()

    # Calcular e imprimir métricas para cada classe prevista usando classification_report
    y_pred = cross_val_predict(model, X, y, cv=skf)
    class_report = classification_report(y, y_pred)
    print(class_report)
    print()

