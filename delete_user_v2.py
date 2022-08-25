"""

SR - CPU Design

"""

from dis import findlinestarts
import cron_guest_handler
import time
import my_logger


def measure_time(func):
    def wrapper(*arg):
        start = time.time()
        res = func(*arg)
        run_time = time.time()-start
        my_logger.main_logger.info(
            'Guest accounts were deleted successfully after: %s sec' % round(run_time, 2))
        return res
    return wrapper


@measure_time
def main():
    try:
        connect = cron_guest_handler.CPPM(
            "user", "key", "10.10.93.122")
        connect.token()
        client_id = connect.guest()
        total = client_id
        while client_id == 1000:
            client_id = connect.guest()
            total += client_id
        
    except OSError as err:
        my_logger.main_logger.error(f"Unexpected {err=}, {type(err)=}")
        raise RuntimeError from None
    except BaseException as err:
        my_logger.main_logger.error(f"Unexpected {err=}, {type(err)=}")
    finally:
        my_logger.main_logger.info(
            f'Total number of guest accounts removed : {total}')

if __name__ == "__main__":
    main()
