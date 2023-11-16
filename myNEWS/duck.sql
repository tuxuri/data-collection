copy (
    select 'mynews' as feature_name,
        'convenience_store' as feature_tag,
        name as Name,
        address as Address,
        lng as Longitude,
        lat as Latitude
    from read_json_auto('stores.json')
) to 'output.csv' (header, delimiter ',');