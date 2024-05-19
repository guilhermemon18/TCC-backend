from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from imblearn.under_sampling import RandomUnderSampler, NearMiss, OneSidedSelection
from src.pre_processamento_dados.codificacao import codificar_dataframe
from src.pre_processamento_dados.pre_processamento_GR_30 import get_dataframe_gr30

# Carregar e preprocessar os dados
df = get_dataframe_gr30()
df = codificar_dataframe(df)

# Separar features (X) e target (y)
X = df.drop('Situação', axis=1).values
y = df['Situação'].values

# Random Undersampler
# rus = RandomUnderSampler(random_state=42)
# X, y = rus.fit_resample(X, y)

# NearMiss
nm = NearMiss(version=2)
X, y = nm.fit_resample(X, y)

# # OneSidedSelection (Algoritmo tipo KNN)
# oss = OneSidedSelection(random_state=42)
# X, y = oss.fit_resample(X, y)

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
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    scores = cross_validate(model, X, y, cv=cv, scoring=scoring, return_train_score=False)

    # Exibir resultados para cada métrica
    print(f'{name}:')
    print(f"   Média da Acurácia: {scores['test_accuracy'].mean():.2f} ± {scores['test_accuracy'].std():.2f}")
    print(f"   Média da Precisão: {scores['test_precision'].mean():.2f} ± {scores['test_precision'].std():.2f}")
    print(f"   Média do Recall: {scores['test_recall'].mean():.2f} ± {scores['test_recall'].std():.2f}")
    print(f"   Média do F1-score: {scores['test_f1'].mean():.2f} ± {scores['test_f1'].std():.2f}")
    print(f"   Média da Área sob a Curva ROC: {scores['test_roc_auc'].mean():.2f} ± {scores['test_roc_auc'].std():.2f}")
    print()
