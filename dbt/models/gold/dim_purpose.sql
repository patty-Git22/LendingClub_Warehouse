select distinct
    md5(purpose) as purpose_key,
    purpose
from {{ ref('stg_loans') }}