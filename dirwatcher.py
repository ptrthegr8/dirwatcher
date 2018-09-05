"""
Dirwatcher is program that watches directories
for files containing a magic word.
It then logs the filenames in which the word was found,
along with the location in the file,
in addition to the word itself.
"""
import signal
import time
import logging
import argparse
import os

exit_flag = False

# Sets up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s : %(name)s : %(levelname)s : %(threadName)s : %(message)s')

file_handler = logging.FileHandler('test.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def arg_parser():
    """
    Returns parser for use in main
    """
    parser = argparse.ArgumentParser(
        description="watch a directory for file")
    parser.add_argument("dir", help="dir that is being watched")
    return parser


def dir_watcher(args):
    """
    Given a directory, searches through files and looks for magic word
    and logs if found. It also prints a message to the console.
    """
    magic_word = 'tuesday'
    my_dir = args.dir
    my_dir = os.path.abspath(my_dir)
    dir_filenames = os.listdir(my_dir)
    dir_filepaths = map(lambda filename: os.path.join(
        my_dir, filename), dir_filenames)
    for file_name in dir_filepaths:
        abbr_filename = os.path.basename(file_name)
        with open(file_name) as my_file:
            for num, line in enumerate(my_file, 1):
                if magic_word in line:
                    context = line[line.find(magic_word):]
                    with open(os.getcwd() + '/test.log', 'r') as log_file:
                        log_text = log_file.read()
                        output = 'file -> {} line -> {} text -> {}'.format(
                            abbr_filename, num, context)
                        if output not in log_text:
                            logger.info(
                                'file -> {} line -> {} text -> {}'.format(
                                    abbr_filename, num, context))


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    signames = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                    if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warn('Received {}'.format(signames[sig_num]))
    global exit_flag
    exit_flag = True


def main():
    start = time.time()
    args = arg_parser().parse_args()

    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
    print '\n', "-" * 50, '\n'
    print 'Dirwatcher on the lookout!'
    print '\n', "-" * 50, '\n'
    while not exit_flag:
        # Do my long-running stuff
        try:
            dir_watcher(args)
            # put a sleep inside my while loop
            # so cpu usage not at 100%
            time.sleep(5.0)
        except IOError as e:
            logger.warning(e)
            time.sleep(5.0)
        except Exception as e:
            logger.warning(e)
            time.sleep(5.0)

    end = time.time()
    print '\n', "-" * 50, '\n'
    print "Dirwatcher's watch has ended...\n", "Uptime: {} seconds".format(
        end - start)
    print '\n', "-" * 50, '\n'


if __name__ == "__main__":
    main()
