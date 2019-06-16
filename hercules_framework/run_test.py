"""This module is intended to run the tests
"""
import argparse
import os
import sys
import unittest
from dataclasses import dataclass

from colour_runner import runner
from coverage import Coverage
from pybadges import badge

TEST_DIREC = './test/'
REPORT_DIREC = './report'
STATIC_FOLDER = 'static'
OMMITABLE = ['.env/*', 'test/*', '*/__init__.py', '*/usr/local/lib*']



def get_coverage_badge_color(coverage: float):
    if coverage <= 25:
        return 'red'
    elif coverage <= 50:
        return 'orange'
    elif coverage <= 75:
        return 'yellow'
    else:
        return 'green'


def compute_result(result):
    if result.wasSuccessful():
        code = 0
    else:
        code = 1

    return code


@dataclass
class Args:
    filter: str
    badge: bool
    report: bool
    output: str
    input: str
    coverage: bool
    verbose: bool

    def __post_init__(self):
        if self.badge or self.report:
            self.coverage = True
        if self.filter is not None:
            self.badge = False
            self.coverage = False
            self.report = False


def parse_args(argv) -> Args:
    """
    Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--filter', '-f', help='Filter by function name or class.')
    parser.add_argument(
        '--badge', '-b', help='Generate badge.', action='store_true')
    parser.add_argument(
        '--report', '-r', help='Generate Report.', action='store_true')
    parser.add_argument(
        '--output', '-o', help='Report output.', default=REPORT_DIREC)
    parser.add_argument(
        '--input', '-i', help='Test path.', default=TEST_DIREC)
    parser.add_argument(
        '--coverage', '-c', help='Coverage.',  action='store_true')
    parser.add_argument(
        '--verbose', '-v', help='Verbosity.',  action='store_true')
    if not argv:
        parser.print_help()
    return Args(**parser.parse_args(argv).__dict__)


def filter_tests(test_name: str, suite: unittest.TestSuite):
    suite_out = unittest.TestSuite()
    for test_suite_list in suite:
        for test_suite in test_suite_list._tests:
            if isinstance(test_suite, unittest.suite.TestSuite):
                for test_case in test_suite:
                    if test_name in str(test_case):
                        suite_out.addTest(test_case)
            else:
                suite_out.addTest(test_suite)
    return suite_out if suite_out._tests else suite


def dyscovery(disc_path: str) -> unittest.TestSuite:
    sys.path.insert(0, os.path.abspath(''))
    return unittest.TestLoader().discover(disc_path)


def create_static_folder() -> None:
    try:
        os.mkdir(STATIC_FOLDER)
    except FileExistsError:
        pass


def generate_coverage_badge(cov: float) -> None:
    create_static_folder()
    path = STATIC_FOLDER + '/coverage.svg'
    s = badge(left_text='coverage', right_text='{}%'.format(
        int(cov)), right_color=get_coverage_badge_color(cov))
    with open(path, 'w+') as file:
        file.write(s)


def generate_passing_badge(passing: bool=False) -> None:
    create_static_folder()
    path = STATIC_FOLDER + '/tests.svg'
    s = badge(left_text='tests', right_text='passing' if passing else 'fail',
              right_color='green' if passing else 'red')
    with open(path, 'w+') as file:
        file.write(s)


def main(argv=sys.argv[1:]):
    args = parse_args(argv)
    if args.verbose:
        os.environ['DEBUG'] = 'True'
    suite_out = dyscovery(args.input)
    if args.filter is not None:
        suite_out = filter_tests(args.filter, suite_out)
    if args.coverage:
        coverage = Coverage()
        coverage.start()
    result = runner.ColourTextTestRunner(verbosity=2).run(suite_out)
    cov = 0
    if args.coverage:
        coverage.stop()
        coverage.save()
        cov = coverage.report(omit=OMMITABLE)

    if args.report:
        coverage.html_report(omit=OMMITABLE, directory=args.output)
        # coverage.xml_report(outfile=args.output +
        #                     '/sonaqube_report.xml', omit=OMMITABLE)
    if args.badge:
        generate_coverage_badge(cov)
        generate_passing_badge(result)
    exit(code=compute_result(result))


if __name__ == '__main__':
    main()
