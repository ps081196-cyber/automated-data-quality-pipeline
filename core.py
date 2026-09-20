import re
import pandas as pd

EMAIL=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

def validate(df):
    issues=[]
    def add(mask,rule,column):
        for idx in df.index[mask]:
            issues.append({"row":int(idx)+2,"column":column,"rule":rule,"value":str(df.at[idx,column])})
    required=["order_id","customer_email","order_date","quantity","unit_price"]
    for col in required:
        if col not in df:
            issues.append({"row":0,"column":col,"rule":"missing_column","value":""})
            continue
        add(df[col].isna()|df[col].astype(str).str.strip().eq(""),"required",col)
    if "order_id" in df:
        add(df.order_id.duplicated(keep=False),"duplicate_key","order_id")
    if "customer_email" in df:
        add(~df.customer_email.fillna("").astype(str).str.match(EMAIL),"invalid_email","customer_email")
    for col,low,high in [("quantity",1,1000),("unit_price",0,1000000)]:
        if col in df:
            numeric=pd.to_numeric(df[col],errors="coerce")
            add(numeric.isna()|~numeric.between(low,high),f"range_{low}_{high}",col)
    if "order_date" in df:
        dates=pd.to_datetime(df.order_date,errors="coerce")
        add(dates.isna()|(dates>pd.Timestamp.today().normalize()),"invalid_date","order_date")
    report=pd.DataFrame(issues,columns=["row","column","rule","value"])
    affected=report.loc[report.row>0,"row"].nunique()
    score=max(0,100*(1-affected/max(len(df),1)))
    return report,round(score,1)

def demo_data():
    return pd.DataFrame({"order_id":["A1","A2","A2","A4"],"customer_email":["a@example.com","bad-email","c@example.com",None],"order_date":["2026-01-02","2026-02-04","2099-01-01","invalid"],"quantity":[2,0,4,3],"unit_price":[500,750,-2,900]})
