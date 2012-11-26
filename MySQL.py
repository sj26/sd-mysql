#!/usr/bin/env python

import subprocess

class MySQL:
    config_args = {
        "host": "--host",
        "port": "--port",
        "database": "--database",
        "username": "--user",
        "password": "--password"
    }

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

        self.command = ["mysql"]
        if 'MySQL' in self.raw_config:
            config = self.raw_config['MySQL']
            for (key, arg) in self.config_args.iteritems():
                if key in config:
                    self.command.append("%s=%s" % (arg, config[key]))
        self.command.append("--execute=STATUS")

    def run(self):
        try:
            output = subprocess.check_output(self.command)
            return {'running': True}
        except subprocess.CalledProcessError:
            self.checks_logger.exception("MySQL doesn't seem to be running, perhaps check your configuration?")
            return {'running': False}

if __name__ == '__main__':
    import logging
    print MySQL({}, logging, {}).run()
