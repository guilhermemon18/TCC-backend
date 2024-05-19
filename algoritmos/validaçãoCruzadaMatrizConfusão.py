from imblearn.under_sampling import OneSidedSelection
from sklearn.model_selection import cross_validate, StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from src.pre_processamento_dados.codificacao import codificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30
import numpy as np

# Carregar e preprocessar os dados
df = get_dataframe_gr30()
df = codificar_dataframe(df)

# Separar features (X) e target (y)
X = df.drop('Situação', axis=1).values
y = df['Situação'].values

# OneSidedSelection (Algoritmo tipo KNN)
oss = OneSidedSelection(random_state=42)
X, y = oss.fit_resample(X, y)

# Criar instâncias dos modelos
decision_tree = DecisionTreeClassifier(random_state=42)
random_forest = RandomForestClassifier(random_state=42)
logistic_regression = LogisticRegression(max_iter=10000, random_state=42)

# Lista dos modelos
models = [decision_tree, random_forest, logistic_regression]
model_names = ['Decision Tree', 'Random Forest', 'Logistic Regression']

# Definir métricas para avaliação
scoring = {
    'accuracy': 'accuracy',
    'precision': 'precision',
    'recall': 'recall',
    'f1': 'f1',
    'roc_auc': 'roc_auc'
}

# Realizar validação cruzada para cada modelo
for model, name in zip(models, model_names):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Obter previsões de cada fold
    y_pred = cross_val_predict(model, X, y, cv=cv)

    # Calcular métricas de avaliação
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    roc_auc = roc_auc_score(y, y_pred)

    # Calcular matriz de confusão
    cm = confusion_matrix(y, y_pred)

    # Exibir resultados para cada métrica e matriz de confusão
    print(f'{name}:')
    print(f"   Média da Acurácia: {accuracy:.2f}")
    print(f"   Média da Precisão: {precision:.2f}")
    print(f"   Média do Recall: {recall:.2f}")
    print(f"   Média do F1-score: {f1:.2f}")
    print(f"   Área sob a Curva ROC: {roc_auc:.2f}")
    print("   Matriz de Confusão:")
    print(cm)
    print()
