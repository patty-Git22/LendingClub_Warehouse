select distinct
    md5(concat_ws('|', coalesce(home_ownership, 'NA'), coalesce(emp_length, 'NA'), coalesce(verification_status, 'NA'))) as borrower_profile_key,
    home_ownership,
    emp_length,
    verification_status
from {{ ref('stg_loans') }}