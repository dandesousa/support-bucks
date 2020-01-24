import csv
import os
import logging
import random


logger = logging.getLogger(__name__)


MIN_TICKETS = 1
BASE_TICKETS = 1000
TICKET_WEIGHTS = {
    'primary-morning': BASE_TICKETS*0.05,
    'backup-morning': BASE_TICKETS*0.025,
    'primary-night': BASE_TICKETS*0.015,
    'backup-night': BASE_TICKETS*0.010
}
FALLBACK_TICKETS = 0


def get_args():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(description="Assigns a task to a support person based on weights")
    parser.add_argument("-v", "--verbose", action="count", help="the logging verbosity (more gives more detail)")
    parser.add_argument("--book", type=FileType('rt'), default=os.path.join(os.path.dirname(__file__), 'book.csv'), help="Path to the book of support bucks (default: %(default)s)")
    args = parser.parse_args()

    if args.verbose == 1:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s")
    logger.setLevel(level)

    return args

def main():
    args = get_args()

    ticket_counts = dict()
    total_tickets = 0
    for row in csv.DictReader(args.book):
        tickets = max(int(BASE_TICKETS - sum(TICKET_WEIGHTS.get(key, FALLBACK_TICKETS)*int(value) for key, value in row.items() if key != 'name')), MIN_TICKETS)
        name = row['name']
        total_tickets += tickets
        ticket_counts[name] = tickets

    names = list(ticket_counts.keys())
    weights = [ticket_counts[name] for name in names]

    results = dict()
    total_iterations = 100000
    for i in range(total_iterations):
        winner = random.choices(names, weights, k=1)[0]
        results.setdefault(winner, 0)
        results[winner] += 1

    print(f'The winner is: {winner}!')

    print('Simulation Results: ')
    for name, wins in results.items():
        expected_prob = (ticket_counts[name] / total_tickets) * 100
        actual_prob = (wins / total_iterations) * 100
        print(f'{name:<16}: {wins:<6} (e: {expected_prob:0.03}%, a: {actual_prob:0.03}%)')


if __name__ == '__main__':
    main()
