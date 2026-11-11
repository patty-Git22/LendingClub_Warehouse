with src as (
    select *
    from {{ source('bronze', 'loans_raw') }}
    where try_cast(id as bigint) is not null
),

typed as (
    select
        cast(id as bigint) as loan_id,
        try_strptime(issue_d, '%b-%Y')::date as issue_date,
        try_cast(loan_amnt as double) as loan_amnt,
        try_cast(trim(replace(term, 'months', '')) as integer) as term_months,
        try_cast(replace(int_rate, '%', '') as double) as int_rate,
        try_cast(installment as double) as installment,
        grade,
        sub_grade,
        purpose,
        home_ownership,
        verification_status,
        emp_length,
        try_cast(annual_inc as double) as annual_inc,
        try_cast(dti as double) as dti,
        (try_cast(fico_range_low as double) + try_cast(fico_range_high as double)) / 2 as fico_avg,
        try_cast(replace(revol_util, '%', '') as double) as revol_util,
        loan_status,
        case
            when loan_status in ('Fully Paid', 'Does not meet the credit policy. Status:Fully Paid') then 0
            when loan_status in ('Charged Off', 'Default', 'Late (31-120 days)', 'Late (16-30 days)','Does not meet the credit policy. Status:Charged Off') then 1
            End as is_default,
        _loaded_at
    from src
)

select *
from typed
where is_default is not null    -- filter out null values to avoid skewing the model
qualify row_number() over (partition by loan_id order by _loaded_at desc) = 1