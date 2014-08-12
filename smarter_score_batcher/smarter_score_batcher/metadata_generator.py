'''
Created on Aug 12, 2014

@author: tosako
'''
import argparse
from smarter_score_batcher.utils.metadata_generator import metadata_generator_top_down,\
    metadata_generator_bottom_up


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Metadata generator')
    parser.add_argument('-p', '--path', help='directory/file path to read', required=True)
    parser.add_argument('-r', '--recursive', help='generate metadata recursively', action='store_true', default=True)
    parser.add_argument('-m', '--metadata', help='metadata filename', default='.metadata')
    parser.add_argument('-f', '--force', help='force generate metadata if exists', action='store_true', default=False)
    parser.add_argument('-u', '--up', help='update metadat from bottom to up', action='store_true', default=False)
    args = parser.parse_args()
    __path = args.path
    __recursive = args.recursive
    __metadata = args.metadata
    __force = args.force
    __up = args.up

    if __up:
        metadata_generator_top_down(__path, metadata_filename=__metadata, recursive=__recursive, force=__force)
    else:
        metadata_generator_bottom_up(__path, metadata_filename=__metadata, recursive=__recursive)
