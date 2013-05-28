from udl2.W_move_to_target import explode_to_dims, explode_to_fact
from celery import chain
import argparse


def main():
    '''
    Main function to start the stage of moving data from integration tables to target tables
    '''
    parser = argparse.ArgumentParser(description='Move to Target Worker')
    parser.add_argument("-b", "--batch_id", type=str, default='8866c6d5-7e5e-4c54-bf4e-775abc4021b2', help="Batch id")
    args = parser.parse_args()

    batch = {'batch_id': args.batch_id}

    # First, explode the data into dim tables by celery group
    # Then, explode the data into fact table
    # These two steps are connected by celery chain
    result_uuid = chain(explode_to_dims.s(batch), explode_to_fact.s())()
    result_value = result_uuid.get()
    print(result_value)

if __name__ == '__main__':
    main()
