"""
Clickhouse queries.
Author: sexualizer
Date: 09.05.2025
Project: Stealer
"""

QUERIES = {
    'init_db': """
    CREATE TABLE IF NOT EXISTS project.matches
    (
        id UInt32,
        area_name String,
        competition_name String,
        home_team String,
        away_team String,
        utc_date DateTime,
        status String,
        home_score Nullable(Int64),
        away_score Nullable(Int64),
        winner Nullable(String),
        last_updated DateTime DEFAULT now()
    )
    ENGINE = MergeTree()
    ORDER BY (utc_date, id);
    """,
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