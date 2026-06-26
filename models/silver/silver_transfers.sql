select
    {{ cast_columns({
        'from_stop_id': 'text',
        'to_stop_id': 'text',
        'transfer_type': 'integer',
        'min_transfer_time': 'integer',
        'from_route_id': 'text',
        'to_route_id': 'text',
        'from_trip_id': 'text',
        'to_trip_id': 'text',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'transfers', 'ingested_at') }}
)
