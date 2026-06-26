select
    {{ cast_columns({
        'service_id': 'text',
        'date': 'date',
        'exception_type': 'integer',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'calendar_dates', 'ingested_at') }}
)
