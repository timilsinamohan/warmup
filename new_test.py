import pandas as pd
import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CleanLogData:
    """    This is the datamodel to represent a cleaned log event record.
    """
    user: str
    date: datetime | None
    time: datetime | None
    action: str
    event_id: int

def enforce_data_model_log_data(df):
    structured_log_data = []
    for _,row in df.iterrows():
        record = CleanLogData(
            user= str(row["user"]),
            date= row["date"],
            time= row["time"],
            action= row["action"],
            event_id= row["event_id"]
        )
        structured_log_data.append(record)
    structured_log_data = pd.DataFrame(structured_log_data)
    return structured_log_data
    

def clean_log_data(log_data):
    """
    cleaning the log event data
    """
    df = pd.read_json(log_data)
    df["user"] = df["user"].str.strip().str.lower()
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", errors="coerce")
    df["date"] = df["timestamp"].dt.date
    df["time"] = df["timestamp"].dt.time
    df = df.drop(columns=["timestamp"])
    df["action"] = df["action"].str.strip().str.lower()
    df = df.drop_duplicates()
    return df


def clean_user_data(user_data):
    df = pd.DataFrame(user_data)
    df["username"] = df["username"].str.strip().str.lower()
    df["signup_date"] = pd.to_datetime(df["signup_date"], format="mixed", errors="coerce")
    df = pd.DataFrame(user_data)
    return df
    
def merge_data(df1, df2):
   """ This function will merge the cleaned log data and user data on the username field.
   """
   merged_data = pd.merge(df1, df2, left_on = "user", right_on = "username", how = "inner").drop(columns=["username"])
   return merged_data
   

def main():    # Sample Data 1: Website Click Logs (JSON String)
    log_data = """
    [
        {"event_id": 101, "user": "  alice ", "action": "click", "timestamp": "2026-06-12 09:00:00"},
        {"event_id": 102, "user": "bob", "action": "view", "timestamp": "2026-06-12 09:05:00"},
        {"event_id": 103, "user": "ALICE", "action": "click", "timestamp": "INVALID_DATE"},
        {"event_id": 104, "user": "charlie", "action": "purchase", "timestamp": "2026-06-12 09:15:00"},
        {"event_id": 101, "user": "  alice ", "action": "click", "timestamp": "2026-06-12 09:00:00"}
    ]
    """

    # Sample Data 2: User Profiles (Dictionary)
    user_data = {
        "username": ["alice", "bob", "charlie"],
        "signup_date": ["2025-01-01", "2025-02-15", "2025-03-22"]
    }

    print("Environment ready! Data loaded.")

    log_data_clean = clean_log_data(log_data)
    user_data_clean = clean_user_data(user_data)
    model_log_data = enforce_data_model_log_data(log_data_clean)
    merged_data = merge_data(model_log_data, user_data_clean)
    # print(log_data_clean)
    print(user_data_clean)
    print(model_log_data)
    print("Final Merge Data")
    print(merged_data)
    # print(model_log_data.dtypes)

if __name__ == "__main__":
    main()
