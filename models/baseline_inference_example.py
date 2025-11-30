
# 베이스라인 모델 로드 및 추론 예제 코드
import pickle
import pandas as pd
import numpy as np

# 1. 모델 및 스케일러 로드
with open('models/best_baseline_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

print(f"✓ 모델 로드 완료: DecisionTree")
print(f"✓ Sampling 기법: RUS")

# 2. Core Features (순서 중요!)
core_features = ['sensor_065', 'sensor_154', 'sensor_585', 'sensor_288', 'sensor_426', 'sensor_060', 'sensor_421', 'sensor_104', 'sensor_292', 'sensor_206', 'sensor_406', 'sensor_430', 'sensor_342', 'sensor_407', 'sensor_575', 'sensor_495', 'sensor_211', 'sensor_568', 'sensor_064', 'sensor_052', 'sensor_584', 'sensor_367', 'sensor_349', 'sensor_041', 'sensor_171', 'sensor_011', 'sensor_332', 'sensor_574', 'sensor_078', 'sensor_249', 'sensor_072', 'sensor_351', 'sensor_434', 'sensor_353', 'sensor_068', 'sensor_097', 'sensor_552', 'sensor_201']

# 3. 새로운 데이터 로드 (예시)
# new_data = pd.read_csv('new_sensor_data.csv')
# X_new = new_data[core_features]

# 4. 스케일링
# X_new_scaled = scaler.transform(X_new)

# 5. 예측
# y_pred = model.predict(X_new_scaled)  # 0 or 1

# LinearSVM의 경우 decision_function 사용 가능
# if hasattr(model, 'decision_function'):
#     y_score = model.decision_function(X_new_scaled)
# else:
#     y_proba = model.predict_proba(X_new_scaled)[:, 1]
#     y_score = y_proba

# 6. 결과 해석
# defect_indices = [i for i, pred in enumerate(y_pred) if pred == 1]
# print(f"불량 탐지: {len(defect_indices)}건")
# print(f"불량 비율: {len(defect_indices)/len(y_pred)*100:.2f}%")

# 7. 예측 결과 저장
# result_df = pd.DataFrame({
#     'prediction': y_pred,
#     'score': y_score
# })
# result_df.to_csv('prediction_results.csv', index=False)
