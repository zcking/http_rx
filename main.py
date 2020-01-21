"""
main.py

Entry point for running the http_rx as
a script, or program.
"""

import time

from rx import doctor

def main(urls):
    print(f'monitoring {urls}...')
    doc = doctor.Doctor(urls)

    while True:
        healthy, total = doc.run()
        print(f'{healthy}/{total} passed')
        time.sleep(5) # sleep for 5 seconds


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
            description='HTTP Rx - Your HTTP Doctor',
    )
    parser.add_argument('url', type=str, help='URL(s) to monitor', nargs='+')
    
    args = parser.parse_args()
    main(args.url)

