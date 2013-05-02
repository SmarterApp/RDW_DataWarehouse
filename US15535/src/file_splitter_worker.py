from tasks import file_splitter_mock_task


def main():
    # get parameters from command lines
    parm = get_parameters()

    # execute the file_splitter task
    split_file_result = file_splitter_mock_task.apply_async([parm], queue='Q_files_to_be_split')
    print("Status", split_file_result.status)


def get_parameters():
    return ['p1', 'p2', 'p3']

if __name__ == '__main__':
    main()
