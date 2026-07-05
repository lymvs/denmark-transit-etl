with routes as (
    select
        route_type,
        count(route_id) as routes
    from {{ ref('silver_routes') }}
    group by route_type
),

route_types as (
    select *
    from {{ ref('gtfs_route_types') }}
),

final as (
    select
        r.route_type,
        t.description,
        r.routes
    from routes as r
    left join route_types as t
    on r.route_type = t.route_type
    order by routes desc
)

select * from final