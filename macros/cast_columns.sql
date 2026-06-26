{% macro cast_columns(schema_dict) %}
    {% set metadata = ["feed_version", "ingested_at"] %}
    {% for k, v in schema_dict.items() %}
        {% if k in metadata %}
            cast({{ k }} as {{ v }}) as {{ k }}{% if not loop.last %}, {% endif %}
        {% else %}
        cast(nullif(nullif({{ k }}, ''), 'NaN') as {{ v }}) as {{ k }}{% if not loop.last %}, {% endif %}
        {% endif %}
    {% endfor %}
{% endmacro %}