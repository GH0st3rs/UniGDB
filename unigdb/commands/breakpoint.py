import argparse
import cmd2

from unigdb.color import Color, message
import unigdb.commands
from unigdb.commands import GenericCommand

_breakpoints_ = {}


@unigdb.commands.register_command
class BreakCommand(GenericCommand):
    """Set breakpoint at specified location."""

    _cmdline_ = 'break'
    _aliases_ = ["b", ]

    def __init__(self, cls):
        super(BreakCommand, self).__init__(cls)

    break_parser = argparse.ArgumentParser(description=Color.yellowify(__doc__), add_help=False)
    break_parser.add_argument('location', metavar='LOCATION', type=int, nargs=argparse.OPTIONAL, help='Address for breakpoint')

    @cmd2.with_argparser(break_parser)
    def do_break(self, args: argparse.Namespace):
        if args.location:
            setBreakpoint(args.location, temporary=False)
        else:
            message.hint('Current breakpoints:')
            print('Address\tTemporary')
            for item in unigdb.commands.breakpoint._breakpoints_:
                print('%#x\t%s' % (item, hasBreakpoint(item)))


def setBreakpoint(addr: int, temporary: bool):
    unigdb.commands.breakpoint._breakpoints_[addr] = temporary


def hasBreakpoint(addr: int):
    return unigdb.commands.breakpoint._breakpoints_.get(addr)


def delBreakpoint(addr: int):
    unigdb.commands.breakpoint._breakpoints_.pop(addr)