#!/usr/bin/python3

import argparse
import json
import logging
import os
import threading
import time

SCRIPT_VERSION = '1.0.0'
SCRIPT_DESCRIPTION = "Common script that uses threading to make some actions. Version %s" % SCRIPT_VERSION

TAG_JOBS = 'jobs'
TAG_JOB_ID = 'id'
TAG_JOB_ACTION = 'action'

COLOURS_TAGS = {
    'GREY': "\x1b[38;20m",
    'GREEN': "\x1b[32;20m",
    'BLUE': "\x1b[34;20m",
    'YELLOW': "\x1b[33;20m",
    'RED': "\x1b[31;20m",
    'BOLD_RED': "\x1b[31;1m",
    'RESET': "\x1b[0m"
}

logging.basicConfig(format='%(asctime)s - %(threadName)s - %(message)s', level=logging.INFO)


def logging_info(msg, colour='GREY'):
    """
    Auxiliary function which prints a logging message with the chance of select a colour.
    :param msg: Message to be printed.
    :param colour: Optional parameter to print the message in this colour.
    """
    formatted_msg = msg if colour is None else COLOURS_TAGS[colour] + msg + COLOURS_TAGS['RESET']
    logging.info(formatted_msg)


def __parse_configuration_file(configuration_json):
    """
    Auxiliary method that parses the json configuration file that is selected in the script execution.
    :param configuration_json: Full path of the configuration file.
    :return: An object with the content of the configuration file.
    """
    with open(configuration_json) as f:
        data = json.load(f)
    return data


def run_main_worker(current_step, config_item):
    """
    Main worker with the configuration item set in the configuration file.
    :param current_step: step number.
    :param config_item: configuration data for this worker.
    """
    job_item_id = config_item[TAG_JOB_ID]
    job_item_action = config_item[TAG_JOB_ACTION]

    logging_info('[%s.1] complete worker <%s - %s>' % (current_step, job_item_id, job_item_action), colour='BLUE')


def run_main(config_file):
    """
    Main method
    :param config_file: file with the run configuration
    """
    start_time = time.time()

    logging_info("[1] - Parsing configuration file.")
    configuration_data = __parse_configuration_file(config_file)
    job_list = configuration_data[TAG_JOBS]

    threads = []
    counter = 0
    for job_item in job_list:
        x = threading.Thread(name=f'Thread-{str(counter).rjust(3, "0")}',
                             target=run_main_worker,
                             args=("2", job_item))
        threads.append(x)
        x.start()
        counter = counter + 1

    for index, thread in enumerate(threads):
        thread.join()

    elapsed_time = time.time() - start_time
    elapsed_time_format = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    logging_info("[3] - Process finished! Time elapsed: %s" % elapsed_time_format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION, usage='%(prog)s -c <configuration_file>')
    parser.add_argument('-c', '--config', required=True, metavar="file", help='informs about a configuration file')

    script_args = parser.parse_args()
    input_config_file = script_args.config

    if os.path.isfile(input_config_file):
        run_main(input_config_file)
    else:
        parser.print_help()
