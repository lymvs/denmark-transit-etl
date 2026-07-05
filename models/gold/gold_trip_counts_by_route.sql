with trips as (
    select
        route_id,
        count(trip_id) as trips
    from {{ ref('silver_trips') }}
    group by route_id
),

routes as (
    select
        route_id,
        agency_id,
        route_short_name
    from {{ ref('silver_routes') }}
),

agency as (
    select
        agency_id,
        agency_name
    from {{ ref('silver_agency') }}
),

final as (
    select
        r.route_id as route_id,
        r.route_short_name as route_name,
        t.trips,
        a.agency_name
    from routes as r
    left join trips as t
    on r.route_id = t.route_id
    left join agency as a
    on r.agency_id = a.agency_id
    order by t.trips desc
)

select * from final