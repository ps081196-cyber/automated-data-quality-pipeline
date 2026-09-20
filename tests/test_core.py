import pandas as pd
from core import demo_data,validate

def test_demo_detects_quality_problems():
    report,score=validate(demo_data())
    assert len(report)>=5
    assert score<100

def test_clean_data_passes():
    df=pd.DataFrame({"order_id":["A1"],"customer_email":["a@example.com"],"order_date":["2026-01-01"],"quantity":[2],"unit_price":[10]})
    report,score=validate(df)
    assert report.empty
    assert score==100
