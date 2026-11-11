select distinct
    md5(sub_grade) as grade_key,
    grade,
    sub_grade
from {{ ref('stg_loans') }}