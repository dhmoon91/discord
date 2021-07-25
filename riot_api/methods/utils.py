from db.db import Session

session = Session()


# Check if we have the summoner record in our db.
def check_cached(target_param, table, target_column):
    """
    Check if we have a record matching name in our db.
    name (str): name of the summoner

    """
    try:
        # Create query; TODO: check for update_time
        cached_data = (
            session.query(table).filter(target_column == target_param).one_or_none()
        )
    except Exception as e_values:
        session.rollback()
        raise e_values
    finally:
        session.close()

    if cached_data:
        query_result = {}
        query_result["dict"] = dict(cached_data.__dict__)
        query_result["raw"] = cached_data
        return query_result

    return None
