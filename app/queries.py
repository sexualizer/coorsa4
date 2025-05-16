QUERIES = {
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
    """
}