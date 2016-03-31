-- (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
-- below.
--
-- Education agencies that are members of the Smarter Balanced Assessment
-- Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
-- paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
-- display, distribute, perform and create derivative works of the software
-- included in the Reporting Platform, including the source code to such software.
-- This license includes the right to grant sublicenses by such consortium members
-- to third party vendors solely for the purpose of performing services on behalf
-- of such consortium member educational agencies.

select distinct(f.student_guid), f.state_code, f.asmt_type,a.effective_date,s.last_name 
from (select student_guid, state_code, asmt_type,asmt_rec_id from edware_es_1_10.fact_asmt_outcome_vw limit 200 offset 909999) f 
join edware_es_1_10.dim_asmt a on f.asmt_type=a.asmt_type and f.asmt_rec_id=a.asmt_rec_id 
join edware_es_1_10.dim_student s on s.student_guid=f.student_guid limit 100;