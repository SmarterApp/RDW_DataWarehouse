select d.district_name
, f.district_id
, d.state_code
, s.school_name
, s.school_id
, count(f.school_id)
from fact_asmt_outcome f
join dim_inst_hier d on (f.inst_hier_rec_id = d.inst_hier_rec_id)
join dim_inst_hier s on (f.school_id = s.school_id)
group by 1
, 2
, 3
, 4
, 5
;
