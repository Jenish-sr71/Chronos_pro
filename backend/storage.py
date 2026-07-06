import os

import pandas as pd

from .constants import DATA_FILE


def save_session(category, task, start_dt, end_dt):
    """Appends one completed session to the CSV log. Returns the resolved task name."""
    duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
    if duration_minutes == 0:
        duration_minutes = 1

    task_name = task if task else category

    new_row = pd.DataFrame(
        {
            "Date": [start_dt.strftime("%Y-%m-%d")],
            "Category": [category],
            "Task": [task_name],
            "Start": [start_dt.strftime("%H:%M")],
            "End": [end_dt.strftime("%H:%M")],
            "Duration_Min": [duration_minutes],
        }
    )

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row
    df.to_csv(DATA_FILE, index=False)
    return task_name


def load_all():
    """Returns the full session log as a DataFrame, or None if there's no data yet."""
    if not os.path.exists(DATA_FILE):
        return None
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        return None
    df["Date"] = pd.to_datetime(df["Date"])
    df["Category"] = df["Category"].fillna("Work")
    df["Task"] = df["Task"].fillna(df["Category"])
    return df


def load_for_date(target_date):
    """Returns sessions for a single date, or None if there are none."""
    df = load_all()
    if df is None:
        return None
    day_df = df[df["Date"].dt.date == target_date].copy()
    return day_df if not day_df.empty else None


def clear_all():
    """Deletes the entire session log. Irreversible."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
