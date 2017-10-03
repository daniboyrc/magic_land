#!/usr/bin/env python
# coding: utf-8
# TST test
# (c) 2012-2016 Dalton Serey, UFCG

from __future__ import print_function
from __future__ import unicode_literals
from collections import Counter
import os
import re
import sys
import json
import shlex
import codecs
import signal
import string
import unicodedata

from subprocess import Popen, PIPE

TIMEOUT_DEFAULT = 2
PYTHON = 'python2.7'
if sys.version_info < (2,7):
    sys.stderr.write('tst.py: requires python 2.7 or later\n')
    sys.exit(1)

REDIRECTED = os.fstat(0) != os.fstat(1)

STATUS_CODE = {
    # TST test codes
    'DefaultError': 'e',
    'Timeout': 't',
    'Success': '.',
    'QuasiSuccess': '*',
    'AllTokensSequence': '@',
    'AllTokensMultiset': '&',
    'MissingTokens': '%',
    'Fail': 'F',
    'ScriptTestError': '!',
    'Inconclusive': '?',
    'UNKNOWN': '-',

    # Python ERROR codes
    'AttributeError': 'a',
    'SyntaxError': 's',
    'EOFError': 'o',
    'ZeroDivisionError': 'z',
    'IndentationError': 'i',
    'IndexError': 'x',
    'ValueError': 'v',
    'TypeError': 'y',
    'NameError': 'n',
}


def to_unicode(obj, encoding='utf-8'):
    assert isinstance(obj, basestring), type(obj)
    if isinstance(obj, unicode):
        return obj

    for encoding in ['utf-8', 'latin1']:
        try:
            obj = unicode(obj, encoding)
            return obj
        except UnicodeDecodeError:
            pass

    assert False, "tst: non-recognized encoding"


def read_tstjson(file, exit=False, quit_on_fail=False):
    #with codecs.open(file, mode='r', encoding='utf-8') as f:
    #    tstjson = json.loads(to_unicode(f.read()))
    with open(file) as fd:
        tstjson = json.load(fd)


    return tstjson


def unpack_results(run_method):

    def wrapper(self, *args, **kwargs):
        run_method(self, *args, **kwargs)

        if self.testcase.type == 'io':
            self.result['summary'] = STATUS_CODE[self.result['status']]

    return wrapper


def parse_test_report(data):
    if data and data[0] == '{':
        # assume it's json
        try:
            report = json.loads(data)
            if 'summary' not in report:
                return None, None
            return report['summary'], report.get('feedback')
        except:
            pass

    parts = data.split('\n', 2)
    # TODO: Spaces should be accepted as summary lines.
    #       Improve the specification of a valid summary line.
    if ' ' in parts[0]:
        return None, None

    summary = parts[0]
    if len(parts) > 2:
        feedback = parts[2]
    else:
        feedback = None

    return summary, feedback


class TestRun:

    def __init__(self, subject, testcase):
        self.subject = subject
        self.testcase = testcase
        self.result = {}
        self.result['type'] = self.testcase.type
        self.result['name'] = self.testcase.name

    def run(self, timeout=TIMEOUT_DEFAULT):
        if self.testcase.type == 'io':
            self.run_iotest()

        elif self.testcase.type == 'script':
            self.run_script()

        else:
            assert False, 'unknown test type'


    @unpack_results
    def run_script(self, timeout=TIMEOUT_DEFAULT):
        cmd_str = '%s %s' % (self.testcase.script, self.subject.filename)
        command = shlex.split(cmd_str.encode('utf-8'))
        self.result['command'] = cmd_str

        process = Popen(command, stdout=PIPE, stderr=PIPE) 
        signal.alarm(timeout)
        try:
            stdout, stderr = map(to_unicode, process.communicate())
            signal.alarm(0) # reset the alarm
            process.wait()
        except CutTimeOut: # program didn't stop within expected time
            process.terminate()
            self.result['status'] = 'Timeout'
            self.result['summary'] = 't'
            return

        # collect test data
        self.result['exit_status'] = process.returncode
        self.result['stderr'] = stderr # comment out to remove from report
        self.result['stdout'] = stdout # comment out to remove from report

        # check for correct termination of the test script
        if self.result['exit_status'] != 0:
            self.result['status'] = 'ScriptTestError'
            self.result['summary'] = '!'
            return

        # collect report from either stderr or stdout
        summary, feedback = parse_test_report(stderr)
        if not summary:
            summary, feedback = parse_test_report(stdout)

        if not summary:
            self.result['status'] = 'Inconclusive'
            self.result['summary'] = '?'
            return

        self.result['summary'] = summary
        if summary == len(summary) * '.':
            self.result['status'] = 'Success'
        else:
            self.result['status'] = 'Fail'

        return


    @unpack_results
    def run_iotest(self, timeout=TIMEOUT_DEFAULT):

        # default is running through python
        cmd_str = '%s %s' % (PYTHON, self.subject.filename)

        command = shlex.split(cmd_str.encode('utf-8'))

        # encode test input data
        if self.testcase.input:
            input_data = self.testcase.input.encode('utf-8')
        else:
            input_data = ''
        self.result['input'] = self.testcase.input
        self.result['output'] = self.testcase.output

        # loop until running the test
        while True:
            process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE) 
            signal.alarm(timeout) 
            try:

                # run subject as external process 
                process_data = process.communicate(input=input_data)
                stdout, stderr = map(to_unicode, process_data)

                # collect output data
                self.result['stdout'] = stdout # comment out to remove from report
                self.result['stderr'] = stderr # comment out to remove from report

                # reset alarm for future use
                signal.alarm(0)
                process.wait()

                # leave loop
                break

            except CutTimeOut:
                # timeout... give up
                process.terminate()
                self.result['status'] = 'Timeout'
                return

            except OSError:
                # external error... must run again!
                process.terminate()

        # 1. Did an ERROR ocurred during execution?
        if process.returncode != 0:

            # set default status
            self.result['status'] = 'DefaultError'

            # try use error code from stderr, if available
            for error_code in STATUS_CODE:
                if error_code in stderr:
                    self.result['status'] = error_code
                    break

            return

        # 2. Was it a PERFECTLY SUCCESSFUL run?
        preprocessed_stdout = preprocess(stdout,\
                            self.testcase.ignore)
        if self.testcase.preprocessed_output  == preprocessed_stdout:
            self.result['status'] = 'Success'
            return


        # 3. Was it a NORMALIZED SUCCESSFUL run?
        normalized_stdout = preprocess(stdout, DEFAULT_OPS)
        if self.testcase.normalized_output == normalized_stdout:
            self.result['status'] = 'QuasiSuccess'
            return

        # 4. Doesn't the testcase specify TOKENS?
        if not self.testcase.tokens:
            self.result['status'] = 'Fail'
            return

        # set flags to use with methods re.*
        flags = re.DOTALL|re.UNICODE
        if 'case' in self.testcase.ignore:
            flags = flags|re.IGNORECASE

        # 5. Does the output have ALL EXPECTED TOKENS IN SEQUENCE?
        regex = '(.*)%s(.*)' % ('(.*)'.join(self.testcase.tokens))
        if re.match(regex, preprocessed_stdout, flags=flags):
            self.result['status'] = 'AllTokensSequence'
            return

        # 6. Does the output have the TOKENS MULTISET?
        regex = '|'.join(self.testcase.tokens)
        found = re.findall(regex, preprocessed_stdout, flags=flags)
        found_ms = Counter(found)                        
        tokens_ms = Counter(self.testcase.tokens)
        if found_ms >= tokens_ms:
            self.result['status'] = 'AllTokensMultiset'
            return

        # 7. Does the output have a proper SUBSET OF THE TOKENS?
        if found_ms <= tokens_ms and len(found_ms) > 0:
            self.result['status'] = 'MissingTokens'
            return

        # 8. otherwise...
        self.result['status'] = 'Fail'
        return
          

class TestSubject:

    def __init__(self, filename):
        self.filename = filename
        self._io_results = ''
        self.analyzer_results = ''
        self.testruns = []
        self._results = None
        self._summaries = None


    def results(self):
        if not self._results:
            self._results = []
            for tr in self.testruns:
                self._results.append(tr.result)

        return self._results


    def add_testrun(self, testrun):
        self.testruns.append(testrun)
        self._summaries = None


    def feedbacks(self):
        return [tr['feedback'] for tr in self.results() if tr.get('feedback')]


    def summaries(self, join_io=False):
        if not self._summaries:
            iosummaries = []
            self._summaries = []
            for tr in self.results():
                if join_io and tr['type'] == 'io':
                    iosummaries.append(tr['summary'])
                else:
                    self._summaries.append(tr['summary'])

            if iosummaries:
                self._summaries.insert(0, ''.join(iosummaries))

        return self._summaries


    def verdict(self):
        return 'success' if all(c == '.' for c in ''.join(self.summaries())) else 'fail'


    def summary(self):
        status_codes = [tr['summary'] for tr in self.results()]
        return ''.join(status_codes)



class TestCase():

    def __init__(self, test):

        # get data from tst.json
        self.name = test.get('name')
        self.type = test.get('type', 'io')
        self.input = test.get('input', '')
        self.output = test.get('output', '')
        self.tokens = test.get('tokens', [])
        self.ignore = test.get('ignore', [])
        self.script = test.get('script')
        self.files = test.get('files')

        # convert tokens to a list of strings, if necessary
        if isinstance(self.tokens, basestring):
            self.tokens = self.tokens.split()

        # convert ignore to a list of strings, if necessary
        if isinstance(self.ignore, basestring):
            self.ignore = self.ignore.split()

        # identify tokens within the expected output
        if not self.tokens and '{{' in self.output:
            p = r'{{(.*?)}}' # r'{{.*?}}|\[\[.*?\]\]'
            self.tokens = re.findall(p, self.output)
            # remove tokens' markup from expected output
            self.output = re.sub(p, lambda m: m.group(0)[2:-2], self.output)

        # preprocess individual tokens
        for i in xrange(len(self.tokens)):
            self.tokens[i] = preprocess(self.tokens[i], self.ignore)

        # set up preprocessed output
        self.preprocessed_output = preprocess(self.output, self.ignore)

        # set up normalized output
        self.normalized_output = preprocess(self.output, DEFAULT_OPS)

        # setup expression to match tokens (so we do it once for all subjects)
        self.tokens_expression = '|'.join(self.tokens) if self.tokens else ''



def preprocess(text, operator_names):

    # expand if all is requested
    if operator_names == ['all']:
        operator_names = OPERATOR.keys()

    # sorted to assure 'whites' is last
    operators = [OPERATOR[name] for name in \
                            sorted(operator_names)]

    # apply operators to text
    for op in operators:
        text = op(text)

    return text


def squeeze_whites(text):
    data = [lin.strip().split() for lin in text.splitlines()]
    data = [' '.join(line) for line in data]
    return '\n'.join(data)


def remove_linebreaks(text):
    # TODO: use carefully! it substitutes linebreaks for ' '
    return ' '.join(text.splitlines())


def drop_whites(text):
    # TODO: Use carefully! deltes all whites
    table = dict((ord(char), None) for char in string.whitespace)
    return text.translate(table)


def punctuation_to_white(text):
    # TODO: Use carefully! it substitutes punctuation for ' '
    # TODO: The specification is wrong!
    #       Punctuation should be changed to spaces? This will
    #       duplicate some whites... Should punctuation be deleted?
    #       This would merge tokens into a single one... Should we
    #       have a mixed behavior? All punctuation surrounded by white
    #       would be deleted and punctuation not surrounded
    # For now, it should be used with whites to work properly.
    table = dict((ord(char), u' ') for char in string.punctuation)
    return text.translate(table)


def squeeze_all_whites(text):
    return ' '.join(text.strip().splitlines())


def strip_blanks(text):
    return ' '.join(text.split())


def strip_accents(text):
    # text must be a unicode object, not str
    try:
        nkfd_form = unicodedata.normalize('NFKD', unicode(text,'utf-8'))
        only_ascii = nkfd_form.encode('ASCII', 'ignore')
    except:
        nkfd_form = unicodedata.normalize('NFKD', text)
        only_ascii = nkfd_form.encode('ASCII', 'ignore')

    return unicode(only_ascii)


OPERATOR = {
    'case': string.lower,
    'accents': strip_accents,
    'extra_whites': squeeze_whites,
    'linebreaks': remove_linebreaks, # not default
    'punctuation': punctuation_to_white, # not default
    'whites': drop_whites, # not default
}
DEFAULT_OPS = ['case', 'accents', 'extra_whites']

class CutTimeOut(Exception): pass

def alarm_handler(signum, frame):
    raise CutTimeOut

signal.signal(signal.SIGALRM, alarm_handler)


def to_unicode(obj, encoding='utf-8'):
    assert isinstance(obj, basestring), type(obj)
    if isinstance(obj, unicode):
        return obj

    for encoding in ['utf-8', 'latin1']:
        try:
            obj = unicode(obj, encoding)
            return obj
        except UnicodeDecodeError:
            pass

    assert False, 'tst: non-recognized encoding (use utf-8 or latin1)'


def read_tests(tstjson):

    # read tests from tstjson
    tests = tstjson['tests']

    # copy default ignore options to testcases without ignore
    # TODO: the test should look up the default ignore clause
    ignore = tstjson.get('ignore')
    if ignore:
        for test in tests:
            if 'ignore' not in test:
                test['ignore'] = ignore

    # put each test case in a TestCase instance
    return [TestCase(t) for t in tests]


def main(filename, tests_file):

    # parse command line data
    timeout = 5
    # read subject
    subject = TestSubject(filename)
    # read local tests
    tests = read_tstjson(tests_file)
    # read testcases
    testcases = read_tests(tests)

    for testcase in testcases:
        testrun = TestRun(subject, testcase)
        testrun.run(timeout=timeout)
        subject.add_testrun(testrun)

    summary = ''.join(subject.summaries(join_io=True))
    line = '%s' % (summary)
    return line.encode('utf-8')

if __name__ == '__main__':
    main('teste.py', 'tst.json')