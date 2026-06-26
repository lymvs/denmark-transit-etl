select
    {{ cast_columns({
        'shape_id': 'text',
        'shape_pt_lat': 'float',
        'shape_pt_lon': 'float',
        'shape_pt_sequence': 'integer',
        'feed_version': 'text',
        'ingested_at': 'date'
    }) }}
from (
    {{ select_latest_batch('bronze', 'shapes', 'ingested_at') }}
)
