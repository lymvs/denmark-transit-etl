select
    {{ cast_columns({
        'trip_id': 'text',
        'start_time': 'date',
        'end_time': 'date',
        'headway_secs': 'text',
        'exact_times': 'text',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'frequencies', 'ingested_at') }}
)
