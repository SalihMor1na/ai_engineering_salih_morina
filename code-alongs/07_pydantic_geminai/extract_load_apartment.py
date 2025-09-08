import duckdb
import dlt
import pandas as pd
from pathlib import Path
df = pd.read_csv()
@dlt.resource(write_disposition="replace", table_name="apartment")
def load_data():
    yield df
    
pipeline = dlt.pipeline(
    pipeline_name="apartments",
    destination= "duckdb",
    dataset_name="staging",
)

load_info = pipeline.run(load_data())
print(load_info)
