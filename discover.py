#!/usr/bin/env python

import select
import sys
import pybonjour

global hosttarget
global fullname
global connections
resolved = []

def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname_in,
                     hosttarget_in, port, txtRecord):
    global hosttarget
    hosttarget = hosttarget_in
    global fullname
    fullname = fullname_in
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        #print 'Resolved service:'
        #print '  fullname   =', fullname
        #print '  hosttarget =', hosttarget
        #print '  port       =', port
        resolved.append(True)

def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
                    regtype, replyDomain):
    if errorCode != pybonjour.kDNSServiceErr_NoError:
        return

    if not (flags & pybonjour.kDNSServiceFlagsAdd):
        print hosttarget, 'removed'
        return

    #print 'Service added; resolving'

    resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                interfaceIndex,
                                                serviceName,
                                                regtype,
                                                replyDomain,
                                                resolve_callback)

    try:
        while not resolved:
            ready = select.select([resolve_sdRef], [], [], timeout)
            if resolve_sdRef not in ready[0]:
                print 'Resolve timed out'
                break
            pybonjour.DNSServiceProcessResult(resolve_sdRef)
        else:
            resolved.pop()
    finally:
        resolve_sdRef.close()

def discover(regtype, timeout_in):
    global timeout
    timeout = timeout_in
    browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
                                              callBack = browse_callback)   

    try:
        try:
            while True:
                ready = select.select([browse_sdRef], [], [], timeout)
                if browse_sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(browse_sdRef)
                    return (hosttarget, fullname)
        except KeyboardInterrupt:
            browse_sdRef.close()
            sys.exit(0)
            pass
    finally:
        browse_sdRef.close()

#regtype = raw_input('regtype:')
#timeout = 1
#discover(regtype, timeout)