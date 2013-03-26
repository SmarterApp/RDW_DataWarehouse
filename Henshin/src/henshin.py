import argparse
import os
from transform_metadata import transform_to_metadata
from transform_asmt_outcome import transform_to_realdata


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start transform metadata and outcome files')
    # Three input arguments:
    # dim_asmt file, fact_asmt_file, output directory
    parser.add_argument("-d", "--dim_asmt", default="dim_asmt.csv", help="name of dim_asmt csv file")
    parser.add_argument("-f", "--fact_asmt_outcome", default="fact_asmt_outcome.csv", help="name of fact_asmt_outcome csv file")
    parser.add_argument("-o", "--out_path", default="output", help="output directory")

    # metadata file name pattern, fact_asmt_outcome file name pattern
    metadata_file_pattern = 'METADATA_ASMT_ID_{0}.json'
    fact_asmt_outcome_file_pattern = 'REALDATA_ASMT_ID_{0}.csv'

    # get arguments
    args = parser.parse_args()
    dim_asmt_file = args.dim_asmt
    fact_asmt_outcome_file = args.fact_asmt_outcome
    out_path = args.out_path

    # check for an output path, if it is not set it to be the working directory
    # if it does not exist, create it
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    # generate METADATA files
    asmt_id_list = transform_to_metadata(dim_asmt_file, out_path, metadata_file_pattern)
    if asmt_id_list:
        # generate REALDATA files
        transform_to_realdata(fact_asmt_outcome_file, asmt_id_list, os.path.join(out_path, fact_asmt_outcome_file_pattern))
