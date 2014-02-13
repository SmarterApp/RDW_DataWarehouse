from config import ref_table_data as ref_constants

LZ_CSV = 'LZ_CSV'
SR_STAGING_CSV = 'STG_SBAC_STU_REG'

ref_table_conf = {
    'column_definitions': ref_constants.COLUMNS,
    'column_mappings': [
        # Columns:
        # column_map_key, phase, source_table, source_column, target_table, target_column, transformation_rule, stored_proc_name, stored_proc_created_date, created_date

        # CSV to staging
        ('1', LZ_CSV, 'StateName', SR_STAGING_CSV, 'name_state', ref_constants.CLEAN, None),
    ]
}