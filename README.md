Hacking task for LiteDesk
=========================

This is a Django application that provides two pages: a battery status viewer,
and a list of available wifi networks.  It is just a small programming task.

Dependencies
------------

The application should work on every modern linux system, it relies on `acpi`
and `iwlist`.  It also need django (of course), sqlite and jquery.
The project contains the single activity *sysinfo*.

Usage
-----

Launch the django application, for exaple on port 8000:

	python manage.py runserver 8000

then point your browser to the following pages:

	localhost:8000/sysinfo/battery
	localhost:8000/sysinfo/wifi

you may also be interested to the json API:

	localhost:8000/sysinfo/api/battery
	localhost:8000/sysinfo/api/wifi

**Important**: `iwlist` require root privileges in order to actually scan the
network, using it as a non-root user will give less reliable results, see man
page for more details.  In order to use `iwlist` with sudo, a passwordless
access is required, so please add something similar to `/etc/sudoers`:

	%sudo   ALL=NOPASSWD: /sbin/iwlist

Of course the only user that need this access is the one who runs django, so
its name can be used instead of the *sudo* group.
The application will work even without sudo, but it will show a warning in
the *wifi* page.
Note that the availability of passwordless `sudo` execution permission for
`iwlist` is checked when the module `cmds` is loaded, so you need to reload
it if you change your sudoers file.

Implementation notes
--------------------

This application does not need a database, but a database is used in order to
have a more typical configuration.

For battery info, `acpi` is used because it is quite widespread, it work both
on the old `/proc` filesystem both on the new `/sys`, and it make it possible
to have all needed information in a single process call. The drawback is that
a bit of parsing is needed, but it is just a quite simple regex.

For wifi info, `iwlist` is used because the newest `iw` seems to be instable
in the format of its output (at least, this is what it say about itself).

`sudo` has been preferred over setting the suid on process because most
distributions forbid setting the suid on scripts.  Setting the suid on
`/sbin/iwlist` is too invasive, writing a C file or compiling a shell script
with `mksh` sounds like a quite ad-hoc solution, not a well fit for a project
of this size.

All the call to system tools are synchronous, since the tools used does not
require long execution times.

