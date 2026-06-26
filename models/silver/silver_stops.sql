select
    {{ cast_columns({
        'stop_id': 'text',
        'stop_code': 'text',
        'stop_name': 'text',
        'stop_desc': 'text',
        'stop_lat': 'float',
        'stop_lon': 'float',
        'location_type': 'integer',
        'parent_station': 'text',
        'wheelchair_boarding': 'integer',
        'platform_code': 'text',
        'stop_timezone': 'text',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'stops', 'ingested_at') }}
)
