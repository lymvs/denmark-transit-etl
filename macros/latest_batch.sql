{% macro select_latest_batch(schema_name, table_name, ingested_column) %}
    select *
    from {{ source(schema_name, table_name) }}
    where {{ ingested_column }} = (
        select max({{ ingested_column }})
        from {{ source(schema_name, table_name) }}
    )
{% endmacro %}