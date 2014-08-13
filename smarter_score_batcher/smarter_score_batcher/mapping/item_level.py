class ItemLevelCsvColumns:
    '''
    Constants for item level csv file
    '''
    # In the order of csv headers
    KEY = 'key'
    SEGMENT_ID = 'segmentId'
    POSTITION = 'position'
    CLIENT_ID = 'clientId'
    OPERATIONAL = 'operational'
    ISSELECTED = 'isSelected'
    FORMAT = 'format'
    SCORE = 'score'
    SCORE_STATUS = 'scoreStatus'
    ADMIN_DATE = 'adminDate'
    NUMBER_VISITS = 'numberVisits'
    STRAND = 'strand'
    CONTENT_LEVEL = 'contentLevel'
    PAGE_NUMBER = 'pageNumber'
    PAGE_VISITS = 'pageVisits'
    PAGE_TIME = 'pageTime'
    DROPPED = 'dropped'

    def get_item_level_csv_keys(self):
        return [ItemLevelCsvColumns.KEY,
        ItemLevelCsvColumns.SEGMENT_ID,
        ItemLevelCsvColumns.POSTITION,
        ItemLevelCsvColumns.CLIENT_ID,
        ItemLevelCsvColumns.OPERATIONAL,
        ItemLevelCsvColumns.ISSELECTED,
        ItemLevelCsvColumns.FORMAT,
        ItemLevelCsvColumns.SCORE,
        ItemLevelCsvColumns.SCORE_STATUS,
        ItemLevelCsvColumns.ADMIN_DATE,
        ItemLevelCsvColumns.NUMBER_VISITS,
        ItemLevelCsvColumns.STRAND,
        ItemLevelCsvColumns.CONTENT_LEVEL,
        ItemLevelCsvColumns.PAGE_NUMBER,
        ItemLevelCsvColumns.PAGE_VISITS,
        ItemLevelCsvColumns.PAGE_TIME,
        ItemLevelCsvColumns.DROPPED]
