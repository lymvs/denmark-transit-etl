select
    {{ cast_columns({
        'trip_id': 'text',
        'arrival_time': 'interval',
        'departure_time': 'interval',
        'stop_id': 'text',
        'stop_sequence': 'integer',
        'pickup_type': 'integer',
        'drop_off_type': 'integer',
        'stop_headsign': 'text',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'stop_times', 'ingested_at') }}
)
