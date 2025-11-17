with base as (
  select
    p.product_id,
    p.prod_name
  from {{ ref('stg_olist_product_src') }} p
),
joined as (
  select
    b.product_id,
    b.prod_name as product_pt_raw,
    t.prod_name_en
  from base b
  left join {{ ref('stg_translated_product_name_src') }} t
    on {{ norm_key('b.prod_name') }} = {{ norm_key('t.prod_name_pt') }}
)
select * from joined
