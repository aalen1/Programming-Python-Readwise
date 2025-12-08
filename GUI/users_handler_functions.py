import os
import pandas as pd
import json

USER_DB = "../data/users.csv"

COLUMNS = [
    "username",
    "password",
    "first_name",
    "last_name",
    "birth_date",
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
    user = match.iloc[0].to_dict()

    # Parse books_read JSON list into a set of tuples
    books_str = user.get("books_read", "")
    user["books_read"] = parse_books_read(books_str)

    return user


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

def serialize_books_read(books_read:set):
    """
    Convert a set or list of tuples into a JSON list string for storage
    :param books_read:
    :return: a json dump
    """

    if not books_read:
        return "[]"

    # Normalize the list of books
    books = []
    for item in books_read:
        if isinstance(item, tuple):
            title, isbn = item
            books.append([str(title), str(isbn)])

    return json.dumps(books)

def parse_books_read(books_str:str):
    """
    Parse the JSON string into a set of tuples
    :param books_str:
    :return: a set of tuples
    """

    if not isinstance(books_str,str) or not books_str.strip():
        return set()

    # Try using the json module to load the book str
    try:
        data = json.loads(books_str)
    except json.JSONDecodeError:
        return set()

    # Add each book to the set
    res = set()
    for book in data:
        title, isbn = book
        res.add((str(title), str(isbn)))

    return res

def update_books_read(username, books_read):
    """
    Update the books read for the user in the database
    :param username: username to be updated
    :param books_read: set of books read
    """

    df = load_users()

    if username in df["username"].values:
        books_str = serialize_books_read(books_read)
        df.loc[df['username'] == username, 'books_read'] = books_str
        save_users(df)