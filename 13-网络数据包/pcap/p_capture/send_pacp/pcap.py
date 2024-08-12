from src.util.send_pacp import pcapTypes as ptypes
import ctypes
import fnmatch
import time
import sys
from collections import Callable

from src.log.Log import log


class WinPcapDevices(object):
    class PcapFindDevicesException(Exception):
        pass

    def __init__(self):
        self._all_devices = None

    def __enter__(self):
        assert self._all_devices is None
        all_devices = ctypes.POINTER(ptypes.pcap_if_t)()
        err_buffer = ctypes.create_string_buffer(ptypes.PCAP_ERRBUF_SIZE)
        if ptypes.pcap_findalldevs(ctypes.byref(all_devices), err_buffer) == -1:
            raise self.PcapFindDevicesException("Error in WinPcapDevices: %s\n" % err_buffer.value)
        self._all_devices = all_devices
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._all_devices is not None:
            ptypes.pcap_freealldevs(self._all_devices)

    def pcap_interface_iterator(self):
        if self._all_devices is None:
            raise self.PcapFindDevicesException("WinPcapDevices guard not called, use 'with statement'")
        pcap_interface = self._all_devices
        while bool(pcap_interface):
            yield pcap_interface.contents
            pcap_interface = pcap_interface.contents.next

    def __iter__(self):
        return self.pcap_interface_iterator()

    @classmethod
    def list_devices(cls):
        device_list = list()
        with cls() as devices:
            for device in devices:
                log.info('name:{}, description:{}'.format(device.name, device.description))
                if device.description:
                    device_list.append({'name': device.name.decode('utf-8', 'backslashreplace'), 'description': device.description.decode('utf-8', 'backslashreplace')})
                else:
                    device_list.append({'name': device.name.decode('utf-8', 'backslashreplace'), 'description': device.name.decode('utf-8', 'backslashreplace')})
        return device_list

    @classmethod
    def get_matching_device(cls, glob=None):
        for dict_devices in cls.list_devices():
            if fnmatch.fnmatch(dict_devices['name'], glob):
                return dict_devices['name'], dict_devices['description']
        return None, None


class WinPcap(object):
    """
    A Class to access WinPcap interface functionality.
    Wrapping device opening / closing using the 'with' statement
    """
    # /* prototype of the packet handler */
    # void packet_handler(u_char *param, const struct pcap_pkthdr *header, const u_char *pkt_data);
    HANDLER_SIGNATURE = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_ubyte),
                                         ctypes.POINTER(ptypes.pcap_pkthdr),
                                         ctypes.POINTER(ctypes.c_ubyte))

    class WinPcapException(Exception):
        pass

    class CallbackIsNotCallable(WinPcapException):
        pass

    class DeviceIsNotOpen(WinPcapException):
        """
        Exception raised when trying to use the underlying device without opening it first.
        Can eb resolved by calling the sought method within a 'with' statement.
        """
        pass

    def __init__(self, device_name, snap_length=65536, promiscuous=1, timeout=1000):
        """
        :param device_name: the name of the device to open on context enter
        :param snap_length: specifies the snapshot length to be set on the handle.
        :param promiscuous:  specifies if the interface is to be put into promiscuous mode(0 or 1).
        :param timeout: specifies the read timeout in milliseconds.
        """
        self._handle = None
        self._name = device_name.encode('utf-8')
        self._snap_length = snap_length
        self._promiscuous = promiscuous
        self._timeout = timeout
        self._err_buffer = ctypes.create_string_buffer(ptypes.PCAP_ERRBUF_SIZE)
        self._callback = None
        self._callback_wrapper = self.HANDLER_SIGNATURE(self.packet_handler)

    def __enter__(self):
        assert self._handle is None
        self._handle = ptypes.pcap_open_live(self._name, self._snap_length, self._promiscuous, self._timeout,
                                             self._err_buffer)
        if not self._handle:
            self._handle = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._handle is not None:
            ptypes.pcap_close(self._handle)

    def init(self):
        assert self._handle is None
        self._handle = ptypes.pcap_open_live(self._name, self._snap_length, self._promiscuous, self._timeout,
                                             self._err_buffer)
        if not self._handle:
            self._handle = None
        log.info("success open adapter")
        return self

    def exit(self):
        if self._handle is not None:
            ptypes.pcap_close(self._handle)
            log.info("success close adapter")

    def packet_handler(self, param, header, pkt_pointer):
        if not isinstance(self._callback, Callable):
            raise self.CallbackIsNotCallable()
        pkt_data = ctypes.string_at(pkt_pointer, header.contents.len)
        return self._callback(self, param, header, pkt_data)

    def stop(self):
        if self._handle is None:
            raise self.DeviceIsNotOpen(self._err_buffer.value.decode('utf-8', 'backslashreplace'))
        ptypes.pcap_breakloop(self._handle)

    def run(self, callback=None, limit=0):
        """
        Start pcap's loop over the interface, calling the given callback for each packet
        :param callback: a function receiving (win_pcap, param, header, pkt_data) for each packet intercepted
        :param limit: how many packets to capture (A value of -1 or 0 is equivalent to infinity)  0 代表EOF时停止 -1 代表无限循环
        """
        if self._handle is None:
            raise self.DeviceIsNotOpen(self._err_buffer.value.decode('utf-8', 'backslashreplace'))
        # Set new callback
        self._callback = callback
        # Run loop with callback wrapper
        ptypes.pcap_loop(self._handle, limit, self._callback_wrapper, None)

    def send(self, packet_buffer):
        """
        send a buffer as a packet to the network interface
        :param packet_buffer: buffer to send (length shouldn't exceed MAX_INT)
        """
        if self._handle is None:
            raise self.DeviceIsNotOpen(self._err_buffer.value.decode('utf-8', 'backslashreplace'))
        buffer_length = len(packet_buffer)
        buf_send = ctypes.cast(ctypes.create_string_buffer(packet_buffer, buffer_length),
                               ctypes.POINTER(ctypes.c_ubyte))
        ptypes.pcap_sendpacket(self._handle, buf_send, buffer_length)

    def is_open(self):
        if self._handle is None:
            raise self.DeviceIsNotOpen(self._err_buffer.value.decode('utf-8', 'backslashreplace'))
        else:
            return True

    def run_ex(self):
        if self._handle is None:
            raise self.DeviceIsNotOpen(self._err_buffer.value.decode('utf-8', 'backslashreplace'))
        pkt_data = ctypes.POINTER(ctypes.POINTER(ptypes.pcap_pkthdr))
        header = ctypes.POINTER(ctypes.POINTER(ptypes.u_char))
        ptypes.pcap_next_ex(self._handle, pkt_data, header)
        print(pkt_data)


class WinPcapUtils(object):
    """
    Utilities and usage examples
    """

    @staticmethod
    def packet_printer_callback(win_pcap, param, header, pkt_data):
        try:
            local_tv_sec = header.contents.ts.tv_sec
            ltime = time.localtime(local_tv_sec)
            timestr = time.strftime("%H:%M:%S", ltime)
            print("%s,%.6d len:%d" % (timestr, header.contents.ts.tv_usec, header.contents.len))
        except KeyboardInterrupt:
            win_pcap.stop()
            sys.exit(0)

    @staticmethod
    def capture_on(pattern, callback):
        """
        :param pattern: a wildcard pattern to match the description of a network interface to capture packets on
        :param callback: a function to call with each intercepted packet
        """
        device_name, desc = WinPcapDevices.get_matching_device(pattern)
        if device_name is not None:
            with WinPcap(device_name) as capture:
                capture.run(callback=callback)

    @staticmethod
    def capture_on_device_name(device_name, callback):
        """
        :param device_name: the name (guid) of a device as provided by WinPcapDevices.list_devices()
        :param callback: a function to call with each intercepted packet
        """
        with WinPcap(device_name) as capture:
            capture.run(callback=callback)

    @classmethod
    def capture_on_and_print(cls, pattern):
        """
        Usage example capture_on_and_print("*Intel*Ethernet")
        will capture and print packets from an Intel Ethernet device
        """
        cls.capture_on(pattern, cls.packet_printer_callback)

    @classmethod
    def send_packet(cls, name, packet_buffer, callback=None, limit=10):
        """
        Send a buffer as a packet to a network interface and optionally capture a response
        :param name: a wildcard pattern to match the description of a network interface to capture packets on
        :param packet_buffer: a buffer to send (length shouldn't exceed MAX_INT)
        :param callback: If not None, a function to call with each intercepted packet
        :param limit: how many packets to capture (A value of -1 or 0 is equivalent to infinity)
        """
        device_name, desc = WinPcapDevices.get_matching_device(name)
        if device_name is not None:
            with WinPcap(device_name) as capture:
                capture.send(packet_buffer)
                if callback is not None:
                    capture.run(callback=callback, limit=limit)
        else:
            raise Exception('can no find adapter name：{}'.format(name))

