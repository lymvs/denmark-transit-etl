with stops as (
    select 
        stop_id,
        stop_name 
    from {{ ref('silver_stops') }}
),

stop_times as (
    select
        stop_id,
        count(departure_time) as departures
    from {{ ref('silver_stop_times') }}
    group by stop_id
),

final as (
    select
        t.stop_id as stop_id,
        t.departures,
        s.stop_name
    from stop_times as t
    left join stops as s
    on t.stop_id = s.stop_id
    order by t.departures desc
)

select * from final