from udl2.W_load_from_integration_to_star import explode_to_dims, explode_to_fact
from celery import chain
import argparse


def main():
    parser = argparse.ArgumentParser(description='Move to Target Worker')
    parser.add_argument("-b", "--batch_id", type=int, default=1369321935, help="Batch id")
    args = parser.parse_args()

    batch = {'batch_id': args.batch_id}

    """
    # execute by group for explode_to_dims only
    print("****Start explode_to_dims by Celery Group****")
    result = explode_to_dims.apply_async([batch], queue='Q_copy_to_target', routing_key='udl2')
    print("****Finished moving to target %s by Celery Group****" % str(result))
    """

    result_uuid = chain(explode_to_dims.s(batch), explode_to_fact.s())()
    result_value = result_uuid.get()
    print(result_value)

if __name__ == '__main__':
    main()
