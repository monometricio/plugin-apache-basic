# plugin-apache-basic
Monometric.IO Apache HTTPD status plugin (https://monometric.io)

## Description

This plugin will query apache httpd via mod_status. More metrics will be
available if ExtendedStatus is enabled.

## Installation

```mm-plugins install monometricio/plugin-apache-basic```

```mm-plugins enable monometricio/plugin-apache-basic```

You should see the plugin when running ```mm-plugins list```.

Remember to edit the configuration file ```/etc/mm-agent/plugins/monometricio-plugin-apache-basic.conf```.

## Configuration

For the plugin to work, apache needs to have mod_status enabled:

Example configuration:

```
ExtendedStatus On
<Location /server-status>
    SetHandler server-status
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
</Location>
```

Example plugin configuration:

```
[Env]
MMIO_HTTPD_URL=http://127.0.0.1/server-status?auto
```

*NOTE*: The url must have the _?auto_ suffix. This suffix will make the output
from mod_status machine readable, and is required by the plugin.

## Provided metrics

```
_counter.apache.requests_per_sec: 34
_counter.apache.kb_per_sec: 67
apache.busy_workers: 1
apache.idle_workers: 7
apache.workers.sending_reply: 1
apache.workers.waiting_for_connection: 7
apache.workers.open_slot: 248
```
