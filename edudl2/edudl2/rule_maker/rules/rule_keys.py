# @PydevCodeAnalysisIgnore

# referenced from POC code
INSTRUCTION = 'instruction'
CANON = 'canon'
ALLOWED = 'allowed'
TWO_LISTS = 'two_lists'
ONE_LIST = 'one_list'
CHECK_N = 'check_n'
COMPARE_LENGTH = 'check_length'

LOOK_UP = 'look_up'
INLIST_COMPARE_LENGTH = 'inlist_compare_length'
INLIST_WITH_OUTLIST = 'inlist_with_outlist'


# Transformation Notations.
UPPER = 'upper'
LOWER = 'lower'
REMNL = 'remnl'
TRIM = 'trim'
PCLEAN = 'pclean'
DATE = 'date'
DATEIN = 'datein'
DATEOUT = 'dateout'
LOOKUP = 'lookup'
INLIST = 'inlist'
OUTLIST = 'outlist'
COMPARE_LENGTH = 'compare_length'
CALCULATE = 'calculate'
VCLEAN = 'vclean'
RCLEAN = 'rclean'
TO_CHAR = 'TO_CHAR'
MIN0 = 'MIN0'


# Validation Notations.
IsNotNull = 'IsNotNull'  # Validate if data value(s) are Not Null or are not blank/empty strings
IsUnique = 'IsUnique'  # Validate if the data in the indicated column list is unique across the guid_batch
IsUniqueWithin = 'IsUniqueWithin'  # Validate if the data in the indicated column list is unique across the guid_batch and the indicated field
HasMaxLength = 'HasMaxLength'  # Validate if the length for the data in the indicated column is within the indicated max length.
IsInList = 'IsInList'  # Validate if the data in the indicated column (column1) is in the list of values defined.
IsInRange = 'IsInRange'  # Validate is the number is within the given min and max values.
IsLessThan = 'IsLessThan'  # Validate if the data in the indicated column is less than the provided value.
IsMoreThan = 'IsMoreThan'  # Validate if the data in the given column is greater than the provided value.
IsBefore = 'IsBefore'  # Validate if the date in the given column exists before the provided date.
IsAfter = 'IsAfter'  # Validate if the date in the given column exists after the provided date.
IsGoodDate = 'IsGoodDate'  # Validate if the provided date is an actual calendar date.
Assert = 'Assert'  # Validate if the Assert condition evaluates to true.
IsNumber = 'IsNumber'  # Validate if the input is a Number
IsText = 'IsText'  # Validate if the input is Text
IsSQLSafe = 'IsSQLSafe'  # Validate if the Text does not have any restricted special characters
IsGoodGUID = 'IsGoodGUID'  # Validate if the GUID is valid

NAME = 'Name'
