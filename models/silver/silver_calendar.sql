select
    {{ cast_columns({
        'service_id': 'text',
        'monday': 'boolean',
        'tuesday': 'boolean',
        'wednesday': 'boolean',
        'thursday': 'boolean',
        'friday': 'boolean',
        'saturday': 'boolean',
        'sunday': 'boolean',
        'start_date': 'date',
        'end_date': 'date',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'calendar', 'ingested_at') }}
)
