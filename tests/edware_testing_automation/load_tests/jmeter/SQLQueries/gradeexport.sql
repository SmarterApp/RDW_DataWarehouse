select max(state_code),district_guid,school_guid,asmt_grade from edware.edware_es_1_10.fact_asmt_outcome_vw 
group by asmt_grade,district_guid,school_guid order by school_guid DESC LIMIT 100;