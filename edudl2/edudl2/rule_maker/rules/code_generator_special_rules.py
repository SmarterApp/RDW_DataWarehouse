'''
Created on July 26, 2013

@author: lichen
'''

# from rule_maker.rules.transformation_code_generator import FUNC_PREFIX

DERIVE_ETH_SQL = """
CREATE OR REPLACE FUNCTION sp_deriveEthnicity
-- The order of the input array: dmg_eth_blk, dmg_eth_asn, dmg_eth_hsp, dmg_eth_ami, dmg_eth_pcf, dmg_eth_wht, dmg_eth_2om
-- Input data type for all items in array is varchar, but they should be casted into bool.
(eth_arr IN varchar[])
RETURNS INTEGER AS
$$

DECLARE
    -- This is the code for hispanic. The hispanic will be checked first
    hispanic_code INTEGER := 3;
    -- This is the code for two or more. The two or more will be checked second
    two_or_more_code INTEGER := 7;
BEGIN
    -- check hispanic
    IF (CAST (eth_arr[hispanic_code] AS BOOL)) = true THEN
        return hispanic_code;
    END IF;

    -- check two or more
    IF (CAST (eth_arr[two_or_more_code] AS BOOL)) = true THEN
        RETURN two_or_more_code;
    END IF;

    FOR i in array_lower(eth_arr,1) .. array_upper(eth_arr,1)
    LOOP
        -- skip hispanic
        IF i = hispanic_code THEN
            CONTINUE;
        ELSIF (CAST (eth_arr[i] AS BOOL)) = true THEN
            RETURN i;
        END IF;
    END LOOP;

    RETURN 0;

EXCEPTION
    WHEN OTHERS THEN
        RETURN -1;
END;
$$ LANGUAGE plpgsql;
"""

# This is a dictionary for special rules
# key is the rule name
# value is a tuple (stored_procedule_expression, sql)
special_rules = {'deriveEthnicity': ('sp_deriveEthnicity(ARRAY[{src_column}])', DERIVE_ETH_SQL)}
