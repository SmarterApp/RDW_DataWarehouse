from edudl2.udl2.W_load_from_integration_to_star import explode_to_dims, explode_to_facts
from celery import chain
import argparse


def main():
    '''
    Main function to start the stage of moving data from integration tables to target tables
    '''
    parser = argparse.ArgumentParser(description='Move to Target Worker')
    parser.add_argument("-b", "--guid_batch", type=str, default='8866c6d5-7e5e-4c54-bf4e-775abc4021b2', help="Batch id")
    args = parser.parse_args()

    batch = {'guid_batch': args.guid_batch}

    # First, explode the data into dim tables by celery group
    # Then, explode the data into fact table
    # These two steps are connected by celery chain
    result_uuid = chain(explode_to_dims.s(batch), explode_to_facts.s())()
    result_value = result_uuid.get()
    print(result_value)

if __name__ == '__main__':
    main()
