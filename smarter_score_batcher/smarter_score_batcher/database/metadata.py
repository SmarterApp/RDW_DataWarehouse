from sqlalchemy.schema import MetaData, CreateSchema, Sequence, UniqueConstraint
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import String, Text, BigInteger
import argparse
from sqlalchemy.engine import create_engine


DBDRIVER = "postgresql+pypostgresql"


def generate_tsb_metadata(schema_name=None, bind=None):

    metadata = MetaData(schema=schema_name, bind=bind)

    # Two-letter state - some countries have 3 or more, but two will do for US
    tsb_asmt = Table('tsb_asmt', metadata,
                     Column('tsb_asmt_rec_id', BigInteger, Sequence('tsb_asmt_rec_id_seq'), primary_key=True),
                     Column('StateAbbreviation', String(50), nullable=True),
                     Column('ResponsibleDistrictIdentifier', String(50), nullable=True),
                     Column('OrganizationName', String(50), nullable=True),
                     Column('ResponsibleSchoolIdentifier', String(50), nullable=True),
                     Column('NameOfInstitution', String(50), nullable=True),
                     Column('StudentIdentifier', String(50), nullable=True),
                     Column('ExternalSSID', String(50), nullable=True),
                     Column('FirstName', String(50), nullable=True),
                     Column('MiddleName', String(50), nullable=True),
                     Column('LastOrSurname', String(50), nullable=True),
                     Column('Sex', String(50), nullable=True),
                     Column('Birthdate', String(50), nullable=True),
                     Column('GradeLevelWhenAssessed', String(50), nullable=True),
                     Column('HispanicOrLatinoEthnicity', String(50), nullable=True),
                     Column('AmericanIndianOrAlaskaNative', String(50), nullable=True),
                     Column('Asian', String(50), nullable=True),
                     Column('BlackOrAfricanAmerican', String(50), nullable=True),
                     Column('NativeHawaiianOrOtherPacificIslander', String(50), nullable=True),
                     Column('White', String(50), nullable=True),
                     Column('DemographicRaceTwoOrMoreRaces', String(50), nullable=True),
                     Column('IDEAIndicator', String(50), nullable=True),
                     Column('LEPStatus', String(50), nullable=True),
                     Column('Section504Status', String(50), nullable=True),
                     Column('EconomicDisadvantageStatus', String(50), nullable=True),
                     Column('MigrantStatus', String(50), nullable=True),
                     Column('AssessmentGuid', String(50), ForeignKey('tsb_metadata.asmt_guid'), nullable=False),
                     Column('AssessmentSessionLocationId', String(50), nullable=True),
                     Column('AssessmentSessionLocation', String(50), nullable=True),
                     Column('AssessmentAdministrationFinishDate', String(50), nullable=True),
                     Column('AssessmentYear', String(50), nullable=True),
                     Column('AssessmentType', String(50), nullable=True),
                     Column('AssessmentAcademicSubject', String(50), nullable=True),
                     Column('AssessmentLevelForWhichDesigned', String(50), nullable=True),
                     Column('AssessmentSubtestResultScoreValue', String(50), nullable=True),
                     Column('AssessmentPerformanceLevelIdentifier', String(50), nullable=True),
                     Column('AssessmentSubtestMinimumValue', String(50), nullable=True),
                     Column('AssessmentSubtestMaximumValue', String(50), nullable=True),
                     Column('AssessmentSubtestResultScoreClaim1Value', String(50), nullable=True),
                     Column('AssessmentSubtestClaim1MinimumValue', String(50), nullable=True),
                     Column('AssessmentSubtestClaim1MaximumValue', String(50), nullable=True),
                     Column('AssessmentClaim1PerformanceLevelIdentifier', String(50), nullable=True),
                     Column('AssessmentSubtestResultScoreClaim2Value', String(50), nullable=True),
                     Column('AssessmentSubtestClaim2MinimumValue', String(50), nullable=True),
                     Column('AssessmentSubtestClaim2MaximumValue', String(50), nullable=True),
                     Column('AssessmentClaim2PerformanceLevelIdentifier', String(50), nullable=True),
                     Column('AssessmentSubtestResultScoreClaim3Value', String(50), nullable=True),
                     Column('AssessmentSubtestClaim3MinimumValue', String(50), nullable=True),
                     Column('AssessmentSubtestClaim3MaximumValue', String(50), nullable=True),
                     Column('AssessmentClaim3PerformanceLevelIdentifier', String(50), nullable=True),
                     Column('AssessmentSubtestResultScoreClaim4Value', String(50), nullable=True),
                     Column('AssessmentSubtestClaim4MinimumValue', String(50), nullable=True),
                     Column('AssessmentSubtestClaim4MaximumValue', String(50), nullable=True),
                     Column('AssessmentClaim4PerformanceLevelIdentifier', String(50), nullable=True),
                     Column('Group1Id', String(50), nullable=True),
                     Column('Group1Text', String(50), nullable=True),
                     Column('Group2Id', String(50), nullable=True),
                     Column('Group2Text', String(50), nullable=True),
                     Column('Group3Id', String(50), nullable=True),
                     Column('Group3Text', String(50), nullable=True),
                     Column('Group4Id', String(50), nullable=True),
                     Column('Group4Text', String(50), nullable=True),
                     Column('Group5Id', String(50), nullable=True),
                     Column('Group5Text', String(50), nullable=True),
                     Column('Group6Id', String(50), nullable=True),
                     Column('Group6Text', String(50), nullable=True),
                     Column('Group7Id', String(50), nullable=True),
                     Column('Group7Text', String(50), nullable=True),
                     Column('Group8Id', String(50), nullable=True),
                     Column('Group8Text', String(50), nullable=True),
                     Column('Group9Id', String(50), nullable=True),
                     Column('Group9Text', String(50), nullable=True),
                     Column('Group10Id', String(50), nullable=True),
                     Column('Group10Text', String(50), nullable=True),
                     Column('AccommodationAmericanSignLanguage', String(50), nullable=True),
                     Column('AccommodationClosedCaptioning', String(50), nullable=True),
                     Column('AccommodationBraille', String(50), nullable=True),
                     Column('AccommodationTextToSpeech', String(50), nullable=True),
                     Column('AccommodationStreamlineMode', String(50), nullable=True),
                     Column('AccommodationPrintOnDemand', String(50), nullable=True),
                     Column('AccommodationPrintOnDemandItems', String(50), nullable=True),
                     Column('AccommodationAbacus', String(50), nullable=True),
                     Column('AccommodationAlternateResponseOptions', String(50), nullable=True),
                     Column('AccommodationReadAloud', String(50), nullable=True),
                     Column('AccommodationCalculator', String(50), nullable=True),
                     Column('AccommodationMultiplicationTable', String(50), nullable=True),
                     Column('AccommodationScribe', String(50), nullable=True),
                     Column('AccommodationSpeechToText', String(50), nullable=True),
                     Column('AccommodationNoiseBuffer', String(50), nullable=True),
                     UniqueConstraint('StudentIdentifier', 'AssessmentGuid')
                     )

    tsb_metadata = Table('tsb_metadata', metadata,
                         Column('asmt_guid', String(50), primary_key=True),
                         Column('state_code', String(2), nullable=False),
                         Column('content', Text, nullable=True))

    tsb_error = Table('tsb_error', metadata,
                      Column('tsb_error_rec_id', BigInteger, Sequence('tsb_error_rec_id_seq'), primary_key=True),
                      Column('asmt_guid', String(50), nullable=False),
                      Column('state_code', String(2), nullable=False),
                      Column('err_code', String(50), nullable=False),
                      Column('err_source', String(50), nullable=True),
                      Column('err_code_text', String(50), nullable=True),
                      Column('err_source_text', String(50), nullable=True),
                      Column('err_input', String(50), nullable=True))

    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create New Schema for EdWare Test Score Batcher')
    parser.add_argument("-s", "--schema", default="edware_tsb", help="set schema name.  required")
    parser.add_argument("-d", "--database", default="edware", help="set database name default[edware]")
    parser.add_argument("--host", default="127.0.0.1:5432", help="postgre host default[127.0.0.1:5432]")
    parser.add_argument("-u", "--user", default="edware", help="postgre username default[edware]")
    parser.add_argument("-p", "--passwd", default="edware2013", help="postgre password default[edware]")
    args = parser.parse_args()

    __schema = args.schema
    __database = args.database
    __host = args.host
    __user = args.user
    __passwd = args.passwd

    if __schema is None:
        print("Please specifiy --schema option")
        exit(-1)
    __URL = DBDRIVER + "://" + __user + ":" + __passwd + "@" + __host + "/" + __database
    print("DB Driver:" + DBDRIVER)
    print("     User:" + __user)
    print("  Password:" + __passwd)
    print("      Host:" + __host)
    print("  Database:" + __database)
    print("    Schema:" + __schema)
    print("####################")
    engine = create_engine(__URL, echo=True)
    connection = engine.connect()
    connection.execute(CreateSchema(__schema))
    metadata = generate_tsb_metadata(schema_name=__schema, bind=engine)
    metadata.create_all(engine)
