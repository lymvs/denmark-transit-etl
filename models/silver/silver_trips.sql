select
    {{ cast_columns({
        'route_id': 'text',
        'service_id': 'text',
        'trip_id': 'text',
        'trip_headsign': 'text',
        'trip_short_name': 'text',
        'direction_id': 'text',
        'block_id': 'text',
        'shape_id': 'text',
        'wheelchair_accessible': 'integer',
        'bikes_allowed': 'integer',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'trips', 'ingested_at') }}
)
