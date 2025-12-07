import os
import pandas as pd

USER_DB = "../data/users.csv"

COLUMNS = [
    "username",
    "password",
    "first_name",
    "last_name",
    "birth_date"
    "books_read"
]

def save_users(df: pd.DataFrame):
    """
    Save a dataframe to a CSV file
    :param df: Dataframe to save
    """
    df.to_csv(USER_DB, index=False)

def load_users():
    """
    Function to load the users from the CSV file, if it do not exists it creates an empty df
    :return: Returns a dataframe with the users
    """
    if os.path.exists(USER_DB):
        df = pd.read_csv(USER_DB, dtype=str)
        # Check all columns exist
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNS]
    else:
        # Create empty df
        df = pd.DataFrame(columns=COLUMNS)
        save_users(df)
        return df

def get_user(username: str):
    """
    Return a dict with user info if username exists, else None.
    """
    df = load_users()

    match = df[df["username"] == username]
    if match.empty:
        return None

    # Take the first row (there should only be one)
    return match.iloc[0].to_dict()


def add_user(user_data: dict) -> None:
    """
    Append a new user to the DataFrame and save.da
    """
    df = load_users()

    # Check for non empty username
    username = user_data.get("username", "").strip()
    if not username:
        raise ValueError("Username is required")

    # Check duplicate
    if not df[df["username"] == username].empty:
        raise ValueError("Username already exists")

    # Normalize to DataFrame row with correct columns [Add empty strings for missing columns]
    row = {col: user_data.get(col, "") for col in COLUMNS}
    # Use concat to add row to end of df
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    # Save the dataframe
    save_users(df)