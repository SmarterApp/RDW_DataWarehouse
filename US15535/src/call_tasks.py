from tasks import file_splitter_mock_task
import time

if __name__ == "__main__":
    res = file_splitter_mock_task.delay(1)
    time.sleep(2)
    print(res.status)
    print(res)
