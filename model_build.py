from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import xgboost as xgb
from catboost import CatBoostClassifier
import os
import pickle
import sys


def evaluate_model(model, x_test, y_test):
    y_pred = model.predict(x_test)
    return accuracy_score(y_test, y_pred), precision_score(y_test, y_pred), recall_score(y_test, y_pred)

if not os.path.exists("model"):
    os.makedirs("model")

with open(sys.argv[2], "rb") as f:
    embedding = pickle.load(f)

x = embedding["data"]
y = embedding["labels"]

name=""
file_name=""
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1905)

if "xgb" in sys.argv[1]:
    xgb_params = {"tree_method": "gpu_hist", "gpu_id": 0}
    model = xgb.XGBClassifier(**xgb_params)
    name="XGBoost Model Performance:"
    file_name= "model/xgb_model.pkl"
elif "cat" in sys.argv[1]:
    model = CatBoostClassifier(task_type="GPU")
    name="CatBoost Model Performance:"
    file_name= "model/catboost_model.pkl"
else:
    print("error")
    exit(0)


model.fit(x_train, y_train)
with open(file_name, 'wb') as model_file:
    pickle.dump(model, model_file)
accuracy, precision, recall = evaluate_model(model, x_test, y_test)

print(name)
print("Accuracy:"+str(accuracy))
print("Precision:"+str(precision))
print("Recall:"+str(recall))
