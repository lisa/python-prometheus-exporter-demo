#!/usr/bin/env python

from sets import Set

import logging
import os
import time
import platform
import psutil

from prometheus_client import start_http_server, Gauge

LOGGED_IN_USERS = Gauge('logged_in_users',"Number of logged in users", labelnames=['hostname', 'username'])

# A list (implemented as a Set) of all active Users
ACTIVE_USERS = Set([])

def collect():
    # Build up the histogram for logged in users
    seen_users = {}
    for user in psutil.users():
        if user.name not in seen_users:
            seen_users[user.name] = 1
        else:
            seen_users[user.name] += 1
        
        ACTIVE_USERS.add(user.name)

    # Add users to exported data list
    for user, count in seen_users.iteritems():
        LOGGED_IN_USERS.labels(
            hostname = platform.node(),
            username = user
        ).set(count)

    # Delete people from Prometheus who are no longer logged in
    # This avoids stale data in 'LOGGED_IN_USERS'
    for inactive_user in ACTIVE_USERS - Set(seen_users.keys()):
        logging.info("Removing username='%s' from Prometheus ",inactive_user)
        ACTIVE_USERS.remove(inactive_user)
        LOGGED_IN_USERS.remove(platform.node(),inactive_user)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

    logging.info("Starting exporter")
    start_http_server(8081)
    while True:
        collect()
        time.sleep(1)
