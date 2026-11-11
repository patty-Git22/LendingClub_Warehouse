{{ config(materialized = 'view') }}
select
    f.*,
    g.grade,
    g.sub_grade,
    p.purpose,
    b.home_ownership,
    b.emp_length,
    b.verification_status
from {{ ref('fct_loans') }} f
join {{ ref('dim_grade') }} g using (grade_key)
join {{ ref('dim_purpose') }} p using (purpose_key)
join {{ ref('dim_borrower_profile') }} b using (borrower_profile_key)