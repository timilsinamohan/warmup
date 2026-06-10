import pandas as pd
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EventRecord:
    event_id: str
    event_name:str | None
    attendee_email:str 
    registration_date:datetime | None
    ticket_type:str
    attended:bool | None
    check_in_time:datetime | None
    session_name:str

def clean_text(value):
    if value is None:
        return None
    value = value.strip().lower()
    return value
    

def clean_date(value):
    value = pd.to_datetime(value, format="mixed", errors="coerce")
    return value

def clean_email(value):
    """"
        This function will clean and standardize email
        addresses by stripping whitespace and converting to lowercase.
    """
    value = value.strip().lower()
    return value

def clean_event_id(value):
    """"
        This function will clean event ID
        by stripping whitespace and converting to uppercase.
    """
    if value is None:
        return None
    else:
        value = value.strip().upper()
    return value


def clean_registration_data(df):
    """ 
        Clean the registration data
    """
    df = df.copy()
    df["event_id"] = df["event_id"].apply(clean_event_id)
    df["event_name"] = df["event_name"].apply(clean_text)
    df["attendee_email"] = df["attendee_email"].apply(clean_email)
    df["registration_date"] = df["registration_date"].apply(clean_date)
    df["ticket_type"] = df["ticket_type"].apply(clean_text)
    df = df.drop_duplicates()
    df = df.dropna(subset=["event_id", "attendee_email"])
    return df

def clean_attendance_data(df):
    """ 
        Clean the attendance data
    """
    df = df.copy()
    df["event_id"] = df["event_id"].apply(clean_event_id)
    df["attendee_email"] = df["attendee_email"].apply(clean_email)
    df["check_in_time"] = df["check_in_time"].apply(clean_date)
    df["session_name"] = df["session_name"].apply(clean_text)
    df = df.drop_duplicates()
    df = df.dropna(subset=["event_id", "attendee_email"])
    return df


def merge_data(cleaned_registrations, cleaned_attendance):
    """ 
        Merge the cleaned attendance and registration data on event_id and attendee_email
    """
    merged = pd.merge(cleaned_registrations, cleaned_attendance,
                       on=["event_id", "attendee_email"],
                         how="left",
                         validate="one_to_one")
    return merged

def main(): 
    registrations = pd.DataFrame({
        "event_id": [" event-101 ", "EVENT-101", None],
        "event_name": [" Spring Gala ", "Spring Gala", "Tech Talk"],
        "attendee_email": ["John@GMAIL.COM ", " mary@test.com", "bob@test.com"],
        "registration_date": ["2026/04/01", "04-01-2026", "bad_date"],
        "ticket_type": ["VIP", "General", None]
    })

    attendance = pd.DataFrame({
            "event_id": [
                "EVENT-101",
                " event-101 ",
                "EVENT-102",
                None
            ],
            "attendee_email": [
                "john@gmail.com",
                "MARY@TEST.COM ",
                "alice@test.com",
                "bob@test.com"
            ],
            "attended": [
                True,
                True,
                None,
                True
            ],
            "check_in_time": [
                "2026-04-15 18:05",
                "04/15/2026 18:10",
                "",
                "2026-05-01 09:00"
            ],
            "session_name": [
                "Opening Session",
                "Opening Session ",
                "Tech Workshop",
                "Closing Session"
            ]
        })
    print("Original Registration Data", registrations.shape[0])
    cleaned_registrations = clean_registration_data(registrations)
    print("Cleaned Registration Data", cleaned_registrations.shape[0])
    print(cleaned_registrations.head())

    print("Original Attendance Data", attendance.shape[0])
    cleaned_attendance = clean_attendance_data(attendance)
    print("Cleaned Attendance Data", cleaned_attendance.shape[0])
    print(cleaned_attendance.head())

    merged_data = merge_data(cleaned_registrations, cleaned_attendance)
    print("Merged data")
    print(merged_data.head())
    records = [
        EventRecord(**record)
        for record in merged_data.to_dict(orient="records")
    ]
    print(records)

    # print(clean_event_id("  EV12345  "))
    # print(clean_email("  JOHN@GMAIL.COM  "))
    # print(clean_date("2025/1/5"))
    

if __name__ == "__main__":
    main()
