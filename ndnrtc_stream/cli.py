"""
ndnrtc-stream

Usage:
  ndnrtc-stream publish [<prefix> -i <identity> -s <video_size> -b <bitrate> -c <config_file> --instance_name <instance> --stream_name <stream_name> --thread_name <thread_name> -v <verbose>]
  ndnrtc-stream fetch <stream_prefix> [-t <trust_schema> -s <video_size> -c <config_file> -a <cert_file> --instance_name <instance> --stream_name <stream_name> --thread_name <thread_name> -v <verbose>]
  ndnrtc-stream -h | --help
  ndnrtc-stream --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  -a, --cert_file                   Certificate which will be used as a trust anchor for data verification.
  -b,--bitrate=<bitrate>            Video stream target encoding bitrate in Kbps.
  -c,--config_file=<config_file>    ndnrtc-client config file.
  -i,--identity=<ndn_identity>      NDN identity used to sign data (default identitiy is used if ommited).
  -s,--video_size=<video_size>      Video stream resolution in the form <width>x<height>.
  -t,--trust_schema=<trust_schema>  Trust schema verification policy.
  --instance_name=<instance>        Customized instance name (see NDN-RTC namespace >= v3)
  --stream_name=<stream_name>       Customized stream name (see NDN-RTC namespace >= v3)
  --thread_name=<thread_name>       Customized thread name (see NDN-RTC namespace >= v3)
  -v,--verbose                      Verbose output.

Examples:
  ndnrtc-stream publish
  ndnrtc-stream publish /ndn/edu/ucla/cs/alex
  ndnrtc-stream publish /ndn/edu/ucla/cs/alex -i /ndn/edu/csu/alex
  ndnrtc-stream fetch /ndn/edu/ucla/cs/alex
  ndnrtc-stream publish /hello-ndn --stream-name custom
  ndnrtc-stream fetch /hello-ndn --stream-name custom

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/remap/ndnrtc-stream
"""

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION
import logging

rootLogger = logging.getLogger()
rootLogger.handlers = []

def main():
    """Main CLI entrypoint."""
    import ndnrtc_stream.commands
    options = docopt(__doc__, version=VERSION)

    for (k, v) in options.items(): 
        if hasattr(ndnrtc_stream.commands, k) and v:
            module = getattr(ndnrtc_stream.commands, k)
            commands = getmembers(module, isclass)
            command = [(name,cls) for (name,cls) in commands if name.lower() == k][0][1]
            ndnrtc_stream.commands = commands
            command = command(options)
            command.run()
