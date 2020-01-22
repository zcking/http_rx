"""
main.py

Entry point for running the http_rx as
a script, or program.
"""

import time
import logging

from rx import doctor

def main(urls):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')
    logging.info(f'monitoring {urls}...')
    doc = doctor.Doctor(urls)

    while True:
        health_report = doc.run()
        logging.info(str(health_report))
        health_report.log_failures()
        time.sleep(5) # sleep for 5 seconds


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
            description='HTTP Rx - Your HTTP Doctor',
    )
    parser.add_argument('url', type=str, help='URL(s) to monitor', nargs='+')
    
    args = parser.parse_args()
    main(args.url)

