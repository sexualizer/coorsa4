"""
Clickhouse queries.
Author: sexualizer
Date: 09.05.2025
Project: Stealer
"""

QUERIES = {
    'test_conn': """
    SELECT 1
    """,
    'insert_matches' : """
    INSERT INTO project.matches (
            id
            , area_name
            , competition_name
            , home_team
            , away_team
            , utc_date
            , status
            , home_score
            , away_score
            , winner
            , last_updated
        ) VALUES 
    """,
    'get_matches_id': f"""
    SELECT id FROM project.matches
    """,
    'insert_log': f"""
    INSERT INTO project.logs (
        time, log
    ) VALUES 
    """

}