
select
  cast(seller_id as string) as seller_id,
  seller_city,
  seller_state
from {{ source('olist_raw','sellers') }}
