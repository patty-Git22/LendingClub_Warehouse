{{ config(serverity = 'warn') }}
select count(*) as row_count
from {{ ref('fct_loans') }}
having count(*) <> 1373915