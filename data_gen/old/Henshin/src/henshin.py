import argparse
import os
from Henshin.src.transform_metadata import transform_to_metadata
from Henshin.src.create_asmt_outcome_2 import transform_to_realdata


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
METADATA_FILE_PATTERN = 'METADATA_ASMT_ID_{0}.json'
FACT_OUTCOME_FILE_PATTERN = 'REALDATA_ASMT_ID_{0}.csv'


def henshin(dim_asmt, username, password, server, database, schema, output_path='output'):
    '''
    Main method
    @param dim_asmt: the filename of the dim_asmt.csv file to use
    @keyword output_path: the name of the output directory to use
    '''
    # check for an output path, if it is not set it to be the working directory
    # if it does not exist, create it
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    # generate METADATA files
    asmt_id_list = transform_to_metadata(dim_asmt, output_path, METADATA_FILE_PATTERN)
    if asmt_id_list:
        file_pattern = os.path.join(output_path, FACT_OUTCOME_FILE_PATTERN)
        transform_to_realdata(file_pattern, username, password, server, database, schema, asmt_guid_list=None, port=5432)

    print("Henshin is completed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start transform metadata and outcome files')

    parser.add_argument("-d", "--dim_asmt", default="dim_asmt.csv", help="name of dim_asmt csv file")
    parser.add_argument("-o", "--out_path", default="output", help="output directory")
    parser.add_argument('--password', help='password for the user. default: edware2013', default='edware2013')
    parser.add_argument('--schema', help='schema to use. default: mayuat_4', default='mayuat_4')
    parser.add_argument('--host', help='host path default: edwdbsrv1.poc.dum.edwdc.net', default='edwdbsrv1.poc.dum.edwdc.net')
    parser.add_argument('--database', help='name of the database. default: edware', default='edware')
    parser.add_argument('-u', '--username', help='username for the db. default: edware', default='edware')
    parser.add_argument('-p', '--port', type=int, help='port to connect to. Default: 5432', default=5432)

    # get arguments
    args = parser.parse_args()
    dim_asmt_file = args.dim_asmt
    out_path = args.out_path
    username = args.username
    password = args.password
    host = args.host
    database = args.database
    schema = args.schema
    port = args.port

    henshin(dim_asmt_file, username, password, host, database, schema, out_path)
