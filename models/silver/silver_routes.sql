select
    {{ cast_columns({
        'route_id': 'text',
        'agency_id': 'text',
        'route_short_name': 'text',
        'route_long_name': 'text',
        'route_type': 'integer',
        'route_color': 'text',
        'route_text_color': 'text',
        'route_desc': 'text',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'routes', 'ingested_at') }}
)
