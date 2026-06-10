import pandas as pd

def clean_events(df_events):
    events = df_events.drop_duplicates()
    events["event_name"] = events["event_name"].str.strip().str.lower()
    events["event_date"] = pd.to_datetime(events["event_date"], format="mixed", errors="coerce")
    events.fillna({"event_name": "Unknown"})
    print(events.head())
    return events

def clean_attendees(df_attendees):
    attendees = df_attendees.drop_duplicates()
    attendees["email"] = attendees["email"].str.strip().str.lower()
    return attendees


def merge_data(events_cleaned, attendees_cleaned):
    '''This function will merge the cleaned events and attendees data on the event_id key. '''
    merged = pd.merge(events_cleaned, attendees_cleaned, on="event_id", how="inner")
    return merged

def validate_merged_results(merged_data):
    ''' Checking the merged data for consistency'''
    print(merged_data.head())
    print(merged_data.info())
    print(merged_data.shape)
    print("Missing values", merged_data.isna().sum())
    print("Duplicated rows", merged_data.duplicated().sum())
    print("Unmatched rows", merged_data[merged_data["event_name"].isna()])



   

def main():
    try:
        df_events = pd.read_csv("data/events.csv")
        df_attendees = pd.read_csv("data/attendees.csv")
        events_cleaned = clean_events(df_events)
        attendees_cleaned = clean_attendees(df_attendees)
        merged_data = merge_data(events_cleaned, attendees_cleaned)
        validate_merged_results(merged_data)


    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    
    

if __name__ == "__main__":
    main()

