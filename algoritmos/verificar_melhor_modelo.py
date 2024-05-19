from collections import Counter

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from src.pre_processamento_dados.codificacao import codificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


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

# Dividir os dados em conjunto de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Instanciar os modelos
decision_tree = DecisionTreeClassifier(random_state=42)
random_forest = RandomForestClassifier(random_state=42)
logistic_regression = LogisticRegression(solver='liblinear', max_iter=10000, random_state=42)  # ajuste o número máximo de iterações conforme necessário

# Treinar os modelos
decision_tree.fit(X_train, y_train)
random_forest.fit(X_train, y_train)
logistic_regression.fit(X_train, y_train)

# Fazer previsões nos dados de teste
y_pred_dt = decision_tree.predict(X_test)
y_pred_rf = random_forest.predict(X_test)
y_pred_lr = logistic_regression.predict(X_test)

# Avaliar a acurácia dos modelos
accuracy_dt = accuracy_score(y_test, y_pred_dt)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
accuracy_lr = accuracy_score(y_test, y_pred_lr)

# Imprimir as acurácias
print("Acurácia da Árvore de Decisão:", accuracy_dt)
print("Acurácia da Floresta Aleatória:", accuracy_rf)
print("Acurácia da Regressão Logística:", accuracy_lr)

# Verificar o melhor modelo
best_model = max(accuracy_dt, accuracy_rf, accuracy_lr)

if best_model == accuracy_dt:
    print("A melhor acurácia foi obtida pela Árvore de Decisão.")
elif best_model == accuracy_rf:
    print("A melhor acurácia foi obtida pela Floresta Aleatória.")
else:
    print("A melhor acurácia foi obtida pela Regressão Logística.")


# Calcular precision, recall e F1-score para cada modelo
precision_dt = precision_score(y_test, y_pred_dt, average='weighted')
recall_dt = recall_score(y_test, y_pred_dt, average='weighted')
f1_dt = f1_score(y_test, y_pred_dt, average='weighted')

precision_rf = precision_score(y_test, y_pred_rf, average='weighted')
recall_rf = recall_score(y_test, y_pred_rf, average='weighted')
f1_rf = f1_score(y_test, y_pred_rf, average='weighted')

precision_lr = precision_score(y_test, y_pred_lr, average='weighted')
recall_lr = recall_score(y_test, y_pred_lr, average='weighted')
f1_lr = f1_score(y_test, y_pred_lr, average='weighted')

# Imprimir as métricas
print("Métricas para Árvore de Decisão:")
print("Precision:", precision_dt)
print("Recall:", recall_dt)
print("F1-score:", f1_dt)
print()

print("Métricas para Floresta Aleatória:")
print("Precision:", precision_rf)
print("Recall:", recall_rf)
print("F1-score:", f1_rf)
print()

print("Métricas para Regressão Logística:")
print("Precision:", precision_lr)
print("Recall:", recall_lr)
print("F1-score:", f1_lr)


# Calcular as probabilidades previstas para cada classe
y_prob_dt = decision_tree.predict_proba(X_test)
y_prob_rf = random_forest.predict_proba(X_test)
y_prob_lr = logistic_regression.predict_proba(X_test)

# Calcular a curva ROC e a área sob a curva para cada modelo
fpr_dt, tpr_dt, _ = roc_curve(y_test, y_prob_dt[:, 1])
auc_dt = auc(fpr_dt, tpr_dt)

fpr_rf, tpr_rf, _ = roc_curve(y_test, y_prob_rf[:, 1])
auc_rf = auc(fpr_rf, tpr_rf)

fpr_lr, tpr_lr, _ = roc_curve(y_test, y_prob_lr[:, 1])
auc_lr = auc(fpr_lr, tpr_lr)

# Plotar as curvas ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr_dt, tpr_dt, label=f'Árvore de Decisão (AUC = {auc_dt:.2f})')
plt.plot(fpr_rf, tpr_rf, label=f'Floresta Aleatória (AUC = {auc_rf:.2f})')
plt.plot(fpr_lr, tpr_lr, label=f'Regressão Logística (AUC = {auc_lr:.2f})')
plt.plot([0, 1], [0, 1], linestyle='--', color='grey', label='Aleatório')
plt.xlabel('Taxa de Falsos Positivos (FPR)')
plt.ylabel('Taxa de Verdadeiros Positivos (TPR)')
plt.title('Curva ROC')
plt.legend()
plt.grid(True)
plt.show()
