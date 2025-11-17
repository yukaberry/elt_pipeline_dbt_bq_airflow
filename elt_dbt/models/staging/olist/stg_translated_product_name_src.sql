-- only this stg model is for 'table', otherwise 'view'

{{ config(materialized='table') }}

select
  trim(string_field_0) as prod_name_pt,
  trim(string_field_1) as prod_name_en
from {{ source('olist_raw', 'product_name_translation') }}
