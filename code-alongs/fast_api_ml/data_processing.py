import pandas as pd
from constants import DATA_PATH
from pydantic import BaseModel, Field
df = pd.read_csv(DATA_PATH / "iris.csv", index_col=0)

class IrisData:
    def __init__(self):
        self.df = df

    def to_json(self):
        return self.df.to_dict(orient="records")

# request/response schemas

class IrisInput(BaseModel):
    SepalLengthCm: float = Field(gt = 4, lt = 8.2)
    SepalWidthCm: float = Field(gt = 1.7, lt = 4.8)
    PetalLengthCm: float = Field(gt = 0.8, lt = 7.1)
    PetalWidthCm: float = Field(gt = 0.05, lt = 2.7)

class PredictionOutput(BaseModel):
    predicted_flower: str


if __name__ == "__main__":
    irirs = IrisData()
    print(irirs.to_json())