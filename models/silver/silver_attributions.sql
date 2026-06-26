select
    {{ cast_columns({
        'attribution_id': 'text',
        'is_producer': 'integer',
        'organization_name': 'text',
        'attribution_url': 'text',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'attributions', 'ingested_at') }}
)
