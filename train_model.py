import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
df = pd.read_csv("datasets/Crop_recommendation.csv")

print(df.head())

# Split input/output
X = df.drop("label", axis=1).values
y = df["label"]

# Encode output (crop names)
y_encoder = LabelEncoder()
y = y_encoder.fit_transform(y)

# Ensure numeric type
X = X.astype(float)

# Build model
model = Sequential()
model.add(Dense(64, activation='relu', input_dim=X.shape[1]))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(len(set(y)), activation='softmax'))

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Train
model.fit(X, y, epochs=80, batch_size=16,validation_split=0.2)

# Save model
model.save("model.h5")

# Save encoder
with open("encoders.pkl", "wb") as f:
    pickle.dump(y_encoder, f)

print("✅ Model trained and saved successfully.")
print(df['label'].value_counts())