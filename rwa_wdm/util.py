import logging
from argparse import Namespace

logger = logging.getLogger(__name__)


class Args(Namespace):
    pass


def validate_args(args: Namespace) -> None:

    if args.rwa is None:
        if args.r is None and args.w is None:
            raise ValueError('The use of either --rwa flag or both -r and -w '
                             'combined is required.')
        elif not (args.r and args.w):
            raise ValueError('Flags -r and -w should be set in combination.')
    elif args.rwa is not None:
        if args.r is not None or args.w is not None:
            raise ValueError('Set either --rwa flag alone or both -r and -w '
                             'flags combined.')
    if args.num_sim < 1:
        raise ValueError('Expect a positive integer as number of simulations.')
