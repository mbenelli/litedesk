# cmds.py - Interface to system commands.
#
# Commands are built as callable instance of `Cmd` class.
# This approach is a bit more dynamic than a class hierarchy, and it seems
# appropriate for the current requirements.

import re, subprocess, shlex, os

def check_passwordless_sudo(cmd):
    '''
    Check if `cmd` can be run with sudo without password.
    `cmd` is a list of command and parameters, as returned from `shlex.split()`
    Return value is a pair of a command and a boolean value: if the check pass
    the command is the original one with `sudo` prepended, and the boolean is
    `True`, otherwise, the command is the argument unchangend and the boolean
    is `False`.
    '''
    with open(os.devnull, 'w') as nil:
        if subprocess.call(['sudo', '-A'] + cmd, stderr=nil, stdout=nil) == 0:
            cmd = ['sudo'] + cmd
            sudo = True
        else:
            cmd = cmd
            sudo = False
        return cmd, sudo


class Cmd(object):
    '''
    Inteface for a system command.
    It is initialized by a dictionary with `cmd`, `re`, and, optionally,
    `sudo` fields.
    An instance of this class is a callable object that, when called,
    runs the command defined in `cmd` string, search for all occurences of
    regular expression `re` in the output and return them.
    If the boolean field `sudo` is supplied and it is `True`, then the
    command will be runned with sudo without password, if possible. 
    The return value of the call is a dictionary with a field 'data'
    containing the result of finding `re` in the output of `cmd` invocation,
    and, eventually, a list of errors(warnings) in the  `errors`(`warnings`)
    fields.
    '''
    def __init__(self, definition):
        cmd = shlex.split(definition['cmd'])
        self.re = definition['re']
        if ('sudo' in definition) and definition['sudo']:
            self.need_sudo = True
            self.cmd, self.sudo = check_passwordless_sudo(cmd)
        else:
            self.need_sudo = False
            self.sudo = False
            self.cmd = cmd

    def __call__(self):
        res = {}
	with open(os.devnull, 'w') as nil:
            try:
                res['data'] = re.findall(self.re,
                    subprocess.check_output(self.cmd, stderr=nil))
                if (self.need_sudo and not self.sudo):
                    res['warnings'] = ['The command "' + self.cmd[0]
                        + '" is not running as root user.'
                        + ' In order to have more reliable informations,'
                        + ' please provide "sudo" passwordless access'
                        + ' to "' + self.cmd[0] + '"']
                return res
            except subprocess.CalledProcessError:
                return { 'errors': ['Cannot run command: %s' % self.cmd] }


# Commands definitions.
#
# The following code should probably reside in a separate module in order to
# easily add/modify commands, but that would be useful only if the `Cmd` is
# sufficiently generic. At the moment it is likely that adding/modifying
# commands will require some tweaks in the `Cmd` class, maybe for a more
# powerful result parsing or for asynchronous communication and so on.
        
definitions = {
    'battery': {
        'cmd':  "acpi -i",
        're': re.compile('.*:\s(Charging|Discharging|Full|Unknow),*\s*(\d+%)'
            + '*,*\s*(\d\d:\d\d)*.*\n.*')
    },
    'wifi': {
        'cmd': "/sbin/iwlist scan",
        're': re.compile('ESSID:"(.*)"'),
        'sudo': True
    }
}

battery = Cmd(definitions['battery'])
wifi = Cmd(definitions['wifi'])

