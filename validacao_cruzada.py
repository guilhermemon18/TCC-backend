from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
#Realizando validação cruzada:
#CV : função que mistura as informações, pode ser passsada como parametro para cross_val-score
#cv = KFold(n_splits = 5, shuffle = True)

#a função StratifiedKFold, que garante que em todos os folds a proporção de informações de evadido e não evadido será a mesma.
from sklearn.model_selection import cross_val_score, StratifiedKFold

from src.main import Funcao_Logistica, x_treino

SEED = 42
np.random.seed(SEED)
cv = StratifiedKFold(n_splits = 5, shuffle = True)
results = cross_val_score(Funcao_Logistica, x_treino,
                          y_treino, cv = cv, scoring='accuracy')
def intervalo(results):
    mean = results.mean()
    dv = results.std()
    print('Acurácia média: {:.2f}%'.format(mean*100))
    print('Intervalo de acurácia: [{:.2f}% ~ {:.2f}%]'
           .format((mean - 2*dv)*100, (mean + 2*dv)*100))
#testando a acurácia.
intervalo(results)



def intervalo_prec(results):
    mean = results.mean()
    dv = results.std()
    print('Precisão média: {:.2f}%'.format(mean*100))
    print('Intervalo de Precisão: [{:.2f}% ~ {:.2f}%]'
          .format((mean - 2*dv)*100, (mean + 2*dv)*100))
results = cross_val_score(Funcao_Logistica, x_treino, y_treino, cv = cv,
                          scoring = 'precision')
#testando precisão do modelo
intervalo_prec(results)

#testando recall do modelo
def intervalo_recall(results):
    mean = results.mean()
    dv = results.std()
    print('Recall médio: {:.2f}%'.format(mean*100))
    print('Intervalo de Recall: [{:.2f}% ~ {:.2f}%]'
          .format((mean - 2*dv)*100, (mean + 2*dv)*100))
cv = StratifiedKFold(n_splits = 5, shuffle = True)
model = LogisticRegression(solver='liblinear')
results = cross_val_score(model, x_treino, y_treino, cv = cv, scoring = 'recall')
intervalo_recall(results)

y_pred = cross_val_predict(model, x_treino, y_treino, cv = cv)
print('Relatório de classificação:\n', classification_report(y_treino, y_pred, digits=4))



model = LogisticRegression(solver='liblinear')
y_scores = cross_val_predict(model, x_treino, y_treino, cv = cv,
                             method = 'decision_function')
precisions, recalls, thresholds = precision_recall_curve(y_treino,
                                                         y_scores)
fig, ax = plt.subplots(figsize = (12,3))
plt.plot(thresholds, precisions[:-1], 'b--', label = 'Precisão')
plt.plot(thresholds, recalls[:-1], 'g-', label = 'Recall')
plt.xlabel('Threshold')
plt.legend(loc = 'center right')
plt.ylim([0,1])
plt.title('Precisão x Recall', fontsize = 14)
plt.subplot()
#plt.show()


#matriz de confusão mais bonitinha em forma de gráficos:
np.random.seed(SEED)
cv = StratifiedKFold(n_splits = 5, shuffle = True)
model = LogisticRegression(solver='liblinear')
y_pred = cross_val_predict(model, x_treino, y_treino, cv = cv)
fig, ax = plt.subplots()
sns.heatmap(confusion_matrix(y_treino, y_pred), annot=True,
            ax=ax, fmt='d', cmap='Reds')
ax.set_title("Matriz de Confusão", fontsize=18)
ax.set_ylabel("True label")
ax.set_xlabel("Predicted Label")
plt.tight_layout()
plt.subplot()
#plt.show()

#Curva ROC
fpr, tpr, thresholds = roc_curve(y_treino, y_scores)
fig, ax = plt.subplots(figsize = (12,4))
plt.plot(fpr, tpr, linewidth=2, label = 'Logistic Regression')
plt.plot([0,1], [0,1], 'k--')
plt.axis([0, 1, 0, 1])
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.legend(loc = 'lower right')
plt.title('Curva ROC', fontsize = 14)
plt.subplot
#plt.show()

#area sob a curva:
print('Área sob a curva ROC: {:.4f}'
      .format(roc_auc_score(y_treino, y_scores)))

# relatório do modelo
print('Relatório de classificação:\n', classification_report(y_treino, y_pred, digits=4))


#comparando com floresta:

np.random.seed(SEED)
cv = StratifiedKFold(n_splits = 5, shuffle = True)
model_rf = RandomForestClassifier(n_estimators=100)
y_prob_forest = cross_val_predict(model_rf, x_treino, y_treino,
                                  cv = cv, method = 'predict_proba')
y_scores_forest = y_prob_forest[:,1]
fpr_forest, tpr_forest, thresholds_forest = roc_curve(
                                           y_treino, y_scores_forest)
print('Área sob a curva ROC - Logistic Regression: {:.4f}'
      .format(roc_auc_score(y_treino, y_scores)))
print('Área sob a curva ROC - Random Forest: {:.4f}'
      .format(roc_auc_score(y_treino, y_scores_forest)))
fig, ax = plt.subplots(figsize = (12,4))
plt.plot(fpr, tpr, linewidth=2, label = 'Logistic Regression')
plt.plot(fpr_forest, tpr_forest, linewidth=2,
         label = 'Random Forest')
plt.plot([0,1], [0,1], 'k--')
plt.axis([0, 1, 0, 1])
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.legend(loc = 'lower right')
plt.title('Curva ROC', fontsize = 14)
plt.show()


#testando finalmente com os dados de teste:
print('modelo final com os dados de teste!')
np.random.seed(SEED)
final_model = LogisticRegression(solver='liblinear')
final_model.fit(x_treino, y_treino)
y_pred = final_model.predict(x_teste)
y_prob = final_model.predict_proba(x_teste)
# imprimir relatório de classificação
print("Relatório de Classificação:\n",
       classification_report(y_teste, y_pred, digits=4))
# imprimir a área sob a curva
print("AUC: {:.4f}\n".format(roc_auc_score(y_teste,y_prob[:,1])))
print(confusion_matrix(y_teste, y_pred))



#final:


#Realizando validação cruzada:
#CV : função que mistura as informações, pode ser passsada como parametro para cross_val-score
#cv = KFold(n_splits = 5, shuffle = True)

#a função StratifiedKFold, que garante que em todos os folds a proporção de informações de evadido e não evadido será a mesma.
SEED = 42
np.random.seed(SEED)
cv = StratifiedKFold(n_splits = 5, shuffle = True)
results = cross_val_score(Funcao_Logistica, x_treino,
                          y_treino, cv = cv, scoring='accuracy')
def intervalo(results):
    mean = results.mean()
    dv = results.std()
    print('Acurácia média: {:.2f}%'.format(mean*100))
    print('Intervalo de acurácia: [{:.2f}% ~ {:.2f}%]'
           .format((mean - 2*dv)*100, (mean + 2*dv)*100))
#testando a acurácia.
intervalo(results)



def intervalo_prec(results):
    mean = results.mean()
    dv = results.std()
    print('Precisão média: {:.2f}%'.format(mean*100))
    print('Intervalo de Precisão: [{:.2f}% ~ {:.2f}%]'
          .format((mean - 2*dv)*100, (mean + 2*dv)*100))
results = cross_val_score(Funcao_Logistica, x_treino, y_treino, cv = cv,
                          scoring = 'precision')
#testando precisão do modelo
intervalo_prec(results)

#testando recall do modelo
def intervalo_recall(results):
    mean = results.mean()
    dv = results.std()
    print('Recall médio: {:.2f}%'.format(mean*100))
    print('Intervalo de Recall: [{:.2f}% ~ {:.2f}%]'
          .format((mean - 2*dv)*100, (mean + 2*dv)*100))
cv = StratifiedKFold(n_splits = 5, shuffle = True)
model = LogisticRegression(solver='liblinear')
results = cross_val_score(model, x_treino, y_treino, cv = cv, scoring = 'recall')
intervalo_recall(results)

y_pred = cross_val_predict(model, x_treino, y_treino, cv = cv)
print('Relatório de classificação:\n', classification_report(y_treino, y_pred, digits=4))



model = LogisticRegression(solver='liblinear')
y_scores = cross_val_predict(model, x_treino, y_treino, cv = cv,
                             method = 'decision_function')
precisions, recalls, thresholds = precision_recall_curve(y_treino,
                                                         y_scores)
fig, ax = plt.subplots(figsize = (12,3))
plt.plot(thresholds, precisions[:-1], 'b--', label = 'Precisão')
plt.plot(thresholds, recalls[:-1], 'g-', label = 'Recall')
plt.xlabel('Threshold')
plt.legend(loc = 'center right')
plt.ylim([0,1])
plt.title('Precisão x Recall', fontsize = 14)
plt.subplot()
#plt.show()


#matriz de confusão mais bonitinha em forma de gráficos:
np.random.seed(SEED)
cv = StratifiedKFold(n_splits = 5, shuffle = True)
model = LogisticRegression(solver='liblinear')
y_pred = cross_val_predict(model, x_treino, y_treino, cv = cv)
fig, ax = plt.subplots()
sns.heatmap(confusion_matrix(y_treino, y_pred), annot=True,
            ax=ax, fmt='d', cmap='Reds')
ax.set_title("Matriz de Confusão", fontsize=18)
ax.set_ylabel("True label")
ax.set_xlabel("Predicted Label")
plt.tight_layout()
plt.subplot()
#plt.show()

#Curva ROC
fpr, tpr, thresholds = roc_curve(y_treino, y_scores)
fig, ax = plt.subplots(figsize = (12,4))
plt.plot(fpr, tpr, linewidth=2, label = 'Logistic Regression')
plt.plot([0,1], [0,1], 'k--')
plt.axis([0, 1, 0, 1])
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.legend(loc = 'lower right')
plt.title('Curva ROC', fontsize = 14)
plt.subplot
#plt.show()

#area sob a curva:
print('Área sob a curva ROC: {:.4f}'
      .format(roc_auc_score(y_treino, y_scores)))

# relatório do modelo
print('Relatório de classificação:\n', classification_report(y_treino, y_pred, digits=4))


#comparando com floresta:

np.random.seed(SEED)
cv = StratifiedKFold(n_splits = 5, shuffle = True)
model_rf = RandomForestClassifier(n_estimators=100)
y_prob_forest = cross_val_predict(model_rf, x_treino, y_treino,
                                  cv = cv, method = 'predict_proba')
y_scores_forest = y_prob_forest[:,1]
fpr_forest, tpr_forest, thresholds_forest = roc_curve(
                                           y_treino, y_scores_forest)
print('Área sob a curva ROC - Logistic Regression: {:.4f}'
      .format(roc_auc_score(y_treino, y_scores)))
print('Área sob a curva ROC - Random Forest: {:.4f}'
      .format(roc_auc_score(y_treino, y_scores_forest)))
fig, ax = plt.subplots(figsize = (12,4))
plt.plot(fpr, tpr, linewidth=2, label = 'Logistic Regression')
plt.plot(fpr_forest, tpr_forest, linewidth=2,
         label = 'Random Forest')
plt.plot([0,1], [0,1], 'k--')
plt.axis([0, 1, 0, 1])
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.legend(loc = 'lower right')
plt.title('Curva ROC', fontsize = 14)
plt.show()


#testando finalmente com os dados de teste:
print('modelo final com os dados de teste!')
np.random.seed(SEED)
final_model = LogisticRegression(solver='liblinear')
final_model.fit(x_treino, y_treino)
y_pred = final_model.predict(x_teste)
y_prob = final_model.predict_proba(x_teste)
# imprimir relatório de classificação
print("Relatório de Classificação:\n",
       classification_report(y_teste, y_pred, digits=4))
# imprimir a área sob a curva
print("AUC: {:.4f}\n".format(roc_auc_score(y_teste,y_prob[:,1])))
print(confusion_matrix(y_teste, y_pred))

