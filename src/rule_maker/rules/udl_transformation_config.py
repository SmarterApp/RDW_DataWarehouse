from rule_maker.rules.rule_keys import *


transform_rules = {
                   'clean'      : { PCLEAN  : [REMNL, TRIM] },
                   
                   'cleanUpper' : { PCLEAN  : [UPPER, REMNL, TRIM] },
                   
                   'cleanLower' : { PCLEAN  : [LOWER, REMNL, TRIM] },
                   
                   'date'       : { DATE    : { DATEIN : ['DD Month YYYY', 'DD Mon YY', 'DDMMYYYY', 'MM-DD-YYYY'], 
                                                DATEOUT: 'YYYYMMDD'}   },
                   
                   'schoolType' : {  PCLEAN  : [UPPER, REMNL, TRIM], 
                                     LOOKUP  : { 'High School'   : ['HS', 'HIGH SCHOOL'],
                                                 'Middle School' : ['MS', 'MIDDLE SCHOOL'],
                                                 'Elementary School' : ['ES' 'ELEMENTARY SCHOOL'] } },
                   
                   'yn'          : { PCLEAN  : [UPPER, REMNL, TRIM], 
                                     LOOKUP  : {'Y': ['Y', '1', 'T'], 'N': ['N', '0', 'F'] } },
                   
                   'gender'      : { PCLEAN  : [UPPER, REMNL, TRIM], 
                                     INLIST  : ['M', 'B', 'MALE', 'BOY','F', 'G','FEMALE', 'GIRL' , 'NS', 'NOT_SPECIFIED', 'NOT SPECIFIED'], 
                                     OUTLIST : ['male','male','male','male','female','female','female','female','NS','NS','NS']     },
                   
                   'staffType'   : { PCLEAN  : [UPPER, REMNL, TRIM], 
                                     LOOKUP  : {'Y': ['Y', '1', 'T'], 'N': ['N', '0', 'F'] } },
                   
                   'calcWeight'  : { CALCULATE  : '( 1 - ( {claim_1} + {claim_2} + {claim_3} ) )' ,  
                                     PCLEAN : [ TRIM, REMNL], 
                                     VCLEAN : UPPER, 
                                     RCLEAN : [ 'TO_CHAR', 'MIN0' ],  
                                                     }
                }