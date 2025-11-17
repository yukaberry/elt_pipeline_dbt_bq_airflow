-- only this stg model is for 'table', otherwise 'view'

{{ config(materialized='table') }}

with src as (

select
  product_id,
  product_category_name --as prod_name

  -- macro --
  -- source() can get 'products'table from 'olist_raw' dataset
  -- it refers to sources_olist.yml
  -- souce(dataset , table )
  from {{ source('olist_raw','products' ) }}
),

clean as (

  select
    product_id,
    -- trim() :  Removes leading and trailing spaces.
    -- nullif(..., '') : empty string ('') real SQL NULL
    nullif(trim(src.product_category_name), '') as prod_name
  from src
)

select *
from clean
where prod_name is not null
