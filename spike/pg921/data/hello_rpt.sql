--hello_rpt.sql

select now() as _bm_start_;

select assmt_code, assmt_name, count(0)
from edware.dim_assmt_outcome_type
group by assmt_code, assmt_name;

select now() as _bm_end_;
