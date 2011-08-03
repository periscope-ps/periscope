"""
Pull different data types from perfSONAR cloud
"""
from cProfile import Profile
from pstats import Stats
from optparse import make_option
import time

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.validators import URLValidator
from django.conf import settings

from psapi.protocol import EndPointPair as psEndPointPair
from psapi.protocol import Interface
from psapi.protocol import events

from periscope.topology.models import NetworkObject

from periscope.topology.lib.helpers import find_service_watch
from periscope.topology.lib.helpers import find_endpoint

from periscope.measurements.lib import query_psservice
from periscope.measurements.lib import pull_all_data
from periscope.measurements.lib import get_meta_keys
from periscope.measurements.lib import get_measurements_data
from periscope.measurements.lib import pull_root_hints
from periscope.measurements.lib import save_lookup_service_result
from periscope.measurements.lib import create_service_client
from periscope.measurements.lib import create_lookup_query
from periscope.measurements.lib import interface_to_port


def pull_roots(service_url, print_services=True):
    """
    Pulls gLS from roots hints
    """
    if not service_url:
        service_url = settings.GLS_ROOT_HINTS
    try:
        pull_root_hints(service_url, print_services)
    except Exception as exp:
        raise CommandError(exp)


def pull_lookup_service(service_url, print_services=True):
    """
    Pulls all registered services from perfSONAR lookup service.
    """
    if service_url is None:
        raise CommandError("Please provide a valid gLS/hLS service "
            "URL: e.g. --url http://example.com:9999/service")

    # Send pull all data to the lookup service
    try:
        client = create_service_client(service_url)
        query = create_lookup_query()
        result = query_psservice(client, query)
        save_lookup_service_result(result, print_services)
    except Exception as exp:
        raise CommandError(exp)


def pull_measurements_data(service_url, network_object,
                        measurements_events, start_time, end_time):
    """
    Generic method to pull perfSONAR measurements
    """

    if service_url:
        service = create_service_client(service_url)
    else:
        if not isinstance(network_object, NetworkObject):
            raise CommandError("Please define a service.")
        
        services = find_service_watch(network_object, measurements_events)
        if not services:
            raise CommandError("Please define a service.")
        service = create_service_client(services[0])
    
    for event in measurements_events:
        objects_keys = get_meta_keys(service, network_object, event)
        keys = []
        for obj in objects_keys:
            keys.append(objects_keys[obj])
        
        result = get_measurements_data(service, keys, event,
                        start_time, end_time)
        
        # TODO (AH): save results
        print event
        print result.data
        print "\n"

def extract_endpoint(src, dst):
    """
    Reads endpoint pair object from user input data.
    If the endpoint has existing matching endpointpair in UNIS
    it will be returned instead.

    @returns: None, L{periscope.topology.models.EndPointPair}, or
            L{psapi.protocol.EndPointPair}
    """
    if not src and not dst:
        return None

    endpoint = find_endpoint(src, dst)
    if endpoint:
        return endpoint

    endpoint = psEndPointPair(src=src, dst=dst)
    endpoint.src_type = None
    endpoint.dst_type = None
    return endpoint


def extract_interface(ifaddress, ifname, ipaddress, hostname):
    """
    Reads interface object from user input data.
    If the interface has existing matching port it will be returned
    instead.

    @returns: None, L{periscope.topology.models.Port}, or
            L{psapi.protocol.Interface}
    """

    if not ifaddress and not ifname and not ipaddress and not hostname:
        return None

    interface = Interface(ifAddress=ifaddress, ifName=ifname,
                    ipAddress=ipaddress, hostName=hostname)
    port = interface_to_port(interface, False)

    if port:
        return port
    else:
        return interface


class Command(BaseCommand):
    """
    One command to pull all kind of perfSONAR data.
    """
    args = "[roots|lookup|if-utilization|if-errors|if-discard|iperf|owamp|"
    args += "traceroute|all]"

    option_list = BaseCommand.option_list + (
        make_option('-u', '--url',
            action='store',
            dest='url',
            default=None,
            help='Service URL to pull data from'),
        make_option(None, '--ifName',
            action='store',
            dest='ifName',
            default=None,
            help='Interface name'),
        make_option(None, '--ifAddress',
            action='store',
            dest='ifAddress',
            default=None,
            help='Interface address'),
        make_option(None, '--ipAddress',
            action='store',
            dest='ipAddress',
            default=None,
            help='Interface IP address'),
        make_option(None, '--hostname',
            action='store',
            dest='hostname',
            default=None,
            help='Hostname'),
        make_option(None, '--src',
            action='store',
            dest='src',
            default=None,
            help='Source address'),
        make_option(None, '--dst',
            action='store',
            dest='dst',
            default=None,
            help='Destination address'),
        make_option(None, '--meta-key',
            action='store',
            dest='meta_key',
            default=None,
            help='Query metadata key'),
        make_option(None, '--get-meta-key',
            action='store_true',
            dest='get_meta_key',
            default=None,
            help='Query metadata key'),
        make_option(None, '--profile',
            action='store',
            dest='profile',
            default=False,
            help='Saves profiling results to a file'),
        make_option('-s', '--silent',
            action='store_true',
            dest='silent',
            default=None,
            help="Don't print output to stdout"),
        make_option('-d', '--direction',
            action='store',
            dest='direction',
            default=None,
            help="Interface measurements direction 'sent' or 'recv'"),
        make_option(None, '--start_time',
            action='store',
            dest='start_time',
            default=None,
            help="Start time for measurements data."),
        make_option(None, '--end_time',
            action='store',
            dest='end_time',
            default=None,
            help="Start time for measurements data."),
    )

    def handle(self, *args, **options):
        profile_file = options.pop('profile', None)
        if profile_file:
            profiler = Profile()
            profiler.runcall(self._handle, *args, **options)
            stats = Stats(profiler)
            stats.dump_stats(profile_file)
        else:
            self._handle(*args, **options)

    def _handle(self, *args, **options):
        """
        Unprofiled command handler.
        """
        direction = options.pop('direction', None)
        service_url = options.pop('url', None)
        start_time = options.pop('start_time', int(time.time()) - 10000)
        end_time = options.pop('end_time', int(time.time()))
        print_services = not options.pop('silent', False)
        src = options.pop('src', None)
        dst = options.pop('dst', None)
        ifaddress = options.pop('ifAddress', None)
        ifname = options.pop('ifName', None)
        ipaddress = options.pop('ipAddress', None)
        hostname = options.pop('hostname', None)

        endpoint = extract_endpoint(src, dst)
        interface = extract_interface(ifaddress, ifname, ipaddress, hostname)

        if len(args) == 0:
            raise CommandError("Use one of the following "
                            "arguments: %s" % self.args)

        if args[0] == 'roots':
            pull_roots(service_url, print_services)

        elif args[0] == 'lookup':
            pull_lookup_service(service_url, print_services)

        elif args[0] == 'if-utilization':
            if direction == 'sent':
                snmp_events = [events.NET_UTILIZATION_SENT]
            elif direction == 'recv':
                snmp_events = [events.NET_UTILIZATION_RECV]
            else:
                snmp_events = [events.NET_UTILIZATION_SENT,
                                events.NET_UTILIZATION_RECV]

            pull_measurements_data(service_url, interface,
                                snmp_events, start_time, end_time)
        elif args[0] == 'if-error':
            if direction == 'sent':
                snmp_events = [events.NET_ERROR_SENT]
            elif direction == 'recv':
                snmp_events = [events.NET_ERROR_RECV]
            else:
                snmp_events = [events.NET_ERROR_SENT, events.NET_ERROR_RECV]

            pull_measurements_data(service_url, interface,
                                snmp_events, start_time, end_time)

        elif args[0] == 'if-discard':
            if direction == 'sent':
                snmp_events = [events.NET_DISCARD_SENT]
            elif direction == 'recv':
                snmp_events = [events.NET_DISCARD_RECV]
            else:
                snmp_events = [events.NET_DISCARD_SENT,
                                events.NET_DISCARD_RECV]

            pull_measurements_data(service_url, interface,
                                snmp_events, start_time, end_time)

        elif args[0] == 'iperf':
            pull_measurements_data(service_url, endpoint,
                                [events.IPERF2], start_time, end_time)

        elif args[0] == 'owamp':
            pull_measurements_data(service_url, endpoint,
                                [events.OWAMP], start_time, end_time)

        elif args[0] == 'traceroute':
            pull_measurements_data(service_url, endpoint,
                                [events.TRACEROUTE], start_time, end_time)

        elif args[0] == 'all':
            print "pulling all data"
            pull_all_data()
        else:
            raise CommandError("Undefined pulling command: '%s'" % args[0])
