select
    loan_id,
    issue_date,
    md5(sub_grade) as grade_key,
    md5(purpose) as purpose_key,
    md5(concat_ws('|', coalesce(home_ownership, 'NA'),
                       coalesce(emp_length, 'NA'),
                       coalesce(verification_status, 'NA'))) as borrower_profile_key,
    loan_amnt,
    term_months,
    int_rate,
    installment,
    annual_inc,
    dti,
    fico_avg,
    revol_util,
    is_default
from {{ ref('stg_loans') }}