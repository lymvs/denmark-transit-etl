select
    {{ cast_columns({
        'agency_id': 'text',
        'agency_name': 'text',
        'agency_url': 'text',
        'agency_timezone': 'text',
        'agency_lang': 'text',
        'agency_phone': 'text',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'agency', 'ingested_at') }}
)
