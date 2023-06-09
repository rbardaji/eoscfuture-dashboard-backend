from dotenv import dotenv_values
from bson.objectid import ObjectId

#dotenv_values reads the values from the .env file and create a dictionary object
config = dotenv_values(".env")


def title_is_unique(title: str, request) -> bool:
    """
    Check on the MongoDB if the title is unique

    Parameters
    ----------
    title : str
        The title to check
    
    Returns
    -------
    bool
        True if the title is unique, False otherwise
    """
    record = request.app.database[
        config["RECORD_TWO_NAME"]].find_one({"title": title})
    # If the record is None, the title is unique
    if record is None:
        return True
    else:
        return False


def create_record_two(record_two: dict, username: str, request) -> dict:
    """
    Create a new record

    Parameters
    ----------
    record_two: dict
        The record to create
    username: str
        The username of the owner

    Returns
    -------
    new_record: dict
        The new record
    """
    # Add the visible field to the record with the default value True
    # if it is not present
    if "visible" not in record_two:
        record_two["visible"] = True
    # Add the owner to the record
    record_two["owner"] = username
    # Insert the record in the database
    record = request.app.database[
        config["RECORD_TWO_NAME"]].insert_one(record_two)
    # Get the record from the database
    new_record = request.app.database[config["RECORD_TWO_NAME"]].find_one(
        {"_id": record.inserted_id}
    )
    return new_record


def get_records_two(username, title, request) -> list:
    """
    Get all the records

    Parameters
    ----------
    username: str
        The username of the owner
    title: str
        The title to search in the title
    request: Request
        The request object

    Returns
    -------
    list
        The list of records
    """
    if username:
        if title:
            # Get all records from the database with the owner username or visible
            # True and the title contains the title string or visible is not
            # present
            records = list(request.app.database[config["RECORD_TWO_NAME"]].find(
                {
                    "$or": [
                        {"owner": username},
                        {"editors": username},
                        {"viewers": username},
                        {"visible": True},
                        {"visible": {"$exists": False}}
                    ],
                    "title": {
                        "$regex": title
                    }
                }
            ))
        else:
            # Get all records from the database with the owner username or visible
            # True
            records = list(request.app.database[config["RECORD_TWO_NAME"]].find(
                {
                    "$or": [
                        {"owner": username},
                        {"editors": username},
                        {"viewers": username},
                        {"visible": True},
                        {"visible": {"$exists": False}}
                    ]
                }
            ))
    else:
        if title:
            # Get all records from the database with visible True
            records = list(request.app.database[config["RECORD_TWO_NAME"]].find(
                {
                    "$or": [
                        {"visible": True},
                        {"visible": {"$exists": False}}
                    ],
                    "title": {
                        "$regex": title
                    }
                }
            ))
        else:
            # Get all records from the database with visible True
            records = list(request.app.database[config["RECORD_TWO_NAME"]].find(
                {
                    "$or": [
                        {"visible": True},
                        {"visible": {"$exists": False}}
                    ]
                }
            ))
    # Convert the ObjectId to string
    for record in records:
        record["id"] = str(record["_id"])
        del record["_id"]
    return records


def get_record_two(record_id: str, request) -> dict:
    """
    Get a record

    Parameters
    ----------
    record_id: str
        The id of the record

    Returns
    -------
    dict
        The record
    """
    record = request.app.database[config["RECORD_TWO_NAME"]].find_one(
        {"_id": ObjectId(record_id)}
    )
    if record:
        # Convert the ObjectId to string
        record["id"] = str(record["_id"])
        del record["_id"]
    return record


def update_record_two(record_id: str, record_two: dict, request) -> dict:
    """
    Update a record

    Parameters
    ----------
    record_id: str
        The id of the record
    record_two: dict
        The record to update

    Returns
    -------
    updated_record: dict
        The updated record
    """
    # Get the record from the database
    actual_record = request.app.database[config["RECORD_TWO_NAME"]].find_one(
        {"_id": ObjectId(record_id)}
    )
    # Update the actual record with the new values
    for key, value in record_two.items():
        if value is not None:
            actual_record[key] = value
    del actual_record["_id"]
    # Update the record in the database
    request.app.database[config["RECORD_TWO_NAME"]].update_one(
        {"_id": ObjectId(record_id)},
        {"$set": actual_record}
    )
    updated_record = request.app.database[config["RECORD_TWO_NAME"]].find_one(
        {"_id": ObjectId(record_id)}
    )
    # Convert the ObjectId to string
    updated_record["id"] = str(updated_record["_id"])
    del updated_record["_id"]
    return updated_record


def delete_record_two(record_id: str, request) -> dict:
    """
    Delete a record

    Parameters
    ----------
    record_id: str
        The id of the record

    Returns
    -------
    bool
        True if the record is deleted, False otherwise
    """
    record = request.app.database[
        config["RECORD_TWO_NAME"]].find_one({"_id": ObjectId(record_id)})
    # Check if the record exists
    if record is None:
        return False
    else:
        # Delete the record if there are not editors
        if record["editors"] is None or len(record["editors"]) == 0:
            request.app.database[config["RECORD_TWO_NAME"]].delete_one(
                {"_id": ObjectId(record_id)}
            )
        else:
            # Change the owner of the record to the first editor
            request.app.database[config["RECORD_TWO_NAME"]].update_one(
                {"_id": ObjectId(record_id)},
                {"$set": {"owner": record["editors"][0]}}
            )
            # Delete the first editor
            request.app.database[config["RECORD_TWO_NAME"]].update_one(
                {"_id": ObjectId(record_id)},
                {"$pop": {"editors": -1}}
            )
        return True


def is_editable(record_id: str, username: str, request) -> bool:
    """
    Check if the record is editable

    Parameters
    ----------
    record_id: str
        The id of the record
    username: str
        The username of the owner

    Returns
    -------
    bool
        True if the record is editable, False otherwise
    """
    record = request.app.database[config["RECORD_TWO_NAME"]].find_one(
        {"_id": ObjectId(record_id)}
    )
    # Check if the record exists
    if record is None:
        return False
    # Check if the username is the owner
    if record["owner"] == username:
        return True
    else:
        # Check if the username is in the editors
        if username in record["editors"]:
            return True
        else:
            return False


def is_owned(record_id: str, username: str, request) -> bool:
    """
    Check if the record is owned

    Parameters
    ----------
    record_id: str
        The id of the record
    username: str
        The username of the owner

    Returns
    -------
    bool
        True if the record is owned, False otherwise
    """
    record = request.app.database[config["RECORD_TWO_NAME"]].find_one(
        {"_id": ObjectId(record_id)}
    )
    # Check if the record exists
    if record is None:
        return False
    # Check if the username is the owner
    if record["owner"] == username:
        return True
    else:
        return False


def get_records_two_me(username, title, request) -> list:
    """
    Get all the records of the user

    Parameters
    ----------
    username: str
        The username of the owner, editor or viewer
    title: str
        String to search in the title

    Returns
    -------
    list
        The list of records
    """
    if title:
        # Get the records of the owner, editor or viewer
        records = list(request.app.database[config["RECORD_TWO_NAME"]].find(
            {
                "$and": [
                    {
                        "$or": [
                            {"owner": username},
                            {"editors": username},
                            {"viewers": username}
                        ]
                    },
                    {"title": {"$regex": title}}
                ]
            }
        ))
    else:
        # Get the records of the owner, editor or viewer
        records = list(request.app.database[config["RECORD_TWO_NAME"]].find(
            {
                "$or": [
                    {"owner": username},
                    {"editors": username},
                    {"viewers": username}
                ]
            }
        ))
    # Convert the ObjectId to string
    for record in records:
        record["id"] = str(record["_id"])
        del record["_id"]
    return records
