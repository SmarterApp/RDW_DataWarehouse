from udl2.W_load_to_integration_table import task
from celery import chain
import argparse


def main():
    parser = argparse.ArgumentParser(description='Move to Integration Driver')
    parser.add_argument("-b", "--guid_batch", type=str, default='00000000-0000-0000-0000-000000000000', help="Batch id")
    args = parser.parse_args()

    batch = {'guid_batch': args.guid_batch, 'load_to_integration_table_type': 'staging_to_integration_sbac_asmt_outcome'}

    """
    # execute by group for explode_to_dims only
    print("****Start explode_to_dims by Celery Group****")
    result = explode_to_dims.apply_async([batch], queue='Q_copy_to_target', routing_key='udl2')
    print("****Finished moving to target %s by Celery Group****" % str(result))
    """

    result_uuid = chain(task.s(batch),)()
    result_value = result_uuid.get()
    print(result_value)

if __name__ == '__main__':
    main()
