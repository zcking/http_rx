"""
main.py

Entry point for running the http_rx as
a script, or program.
"""

import time
import logging

from rx import doctor

def main():
    import json
    import os

    # Parse JSON config file
    config_file_path = os.environ.get('RX_CONF', 'config.json')
    with open(config_file_path) as config_file:
        config = json.load(config_file)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')
    doc = doctor.Doctor(config)

    while True:
        health_report = doc.run()
        logging.info(str(health_report))
        health_report.log_failures()
        time.sleep(config.get('intervalSeconds', 5)) # sleep for 5 seconds by default


if __name__ == '__main__':
    main()

