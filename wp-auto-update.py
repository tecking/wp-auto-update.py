# wp-auto-update.py
#
# wp-auto-update.py is a Python script to update WordPress websites.
# Once you setup a configuration file (YAML format),
# it cruises multiple websites and updates WordPress automatically.
#
# Copyright 2022 -, tecking
# Version 1.0.0
#
# Licensed under the MIT License.


import sys
import smtplib
import textwrap
import paramiko
import yaml
import argparse
import subprocess
from doctest import master
from typing import Text
from email.mime.text import MIMEText
from datetime import datetime


# Constants
MAIL_SMTP = '{str}'
MAIL_PORT = {int}
MAIL_USER = '{str}'
MAIL_PASS = '{str}'
MAIL_SUBJ = '{str}'
MAIL_TO = '{str}'
MAIL_FROM = '{str}'


def read_config():
	"""Read configuration file.

	Returns:
		list: Host information of the servers.
	"""

	try:
		parser = argparse.ArgumentParser()
		parser.add_argument('file', nargs='?', default='config.yml', help='configuration file (YAML format)')
		args = parser.parse_args()
		with open(args.file, 'r') as file:
			config = yaml.safe_load(file)
	except Exception as e:
		message = 'Exception occured while loading YAML... wp-auto-update.py was aborted.\n\n'
		message += e.__doc__
		send_mail(message)
		sys.exit(1)

	return config


def update_wp(args):
	"""Run WP commands.

	Args:
		args (list): Host information of the servers.

	Returns:
		string: Execution results with WP commands.
	"""

	wp = '\
	wp db export `wp eval "echo WP_CONTENT_DIR . DIRECTORY_SEPARATOR . DB_NAME;"`.sql && \
	wp core update --locale=ja && \
	wp plugin update --all && \
	wp theme update --all && \
	wp language core update && \
	wp language plugin update --all && \
	wp language theme update --all && \
	wp cli update --yes'

	wp = textwrap.dedent(wp)
	wget = 'wget --spider -nv --timeout 60 -t 3'

	try:
		users = args['users']
	except Exception as e:
		message = 'Exception occured while parsing YAML... wp-auto-update.py was aborted.\n\n'
		message += e.__doc__
		send_mail(message)
		sys.exit(1)
		
	output = []

	for user in users:

		output.append(f"### {user['name']} ###\n")

		if 'options' in user:
			for option in user['options']:
				if 'search' in option and 'replace' in option:
					tmp = wp
					wp = tmp.replace(option['search'], option['replace'])

		try:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(user['host'], username=user['user'], key_filename=user['key'], passphrase=user['phrase'], password=user['pass'], port=user['port'])

			stdin, stdout, stderr = client.exec_command(f"cd {user['dir']}; {wp}")
			stdin.close()
		except Exception as e:
			message = 'Some exception occured... wp-auto-update.py was aborted.\n\n'
			message += e.__doc__
			send_mail(message)
			sys.exit(1)

		for line in stdout:
			output.append(line)

		for line in stderr:
			output.append(line)

		client.close()

		command = wget.split()
		command.append(user['url'])
		proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		output.append(proc.stderr.decode('utf-8'))
		output.append('\n')

	return ''.join(output)


def send_mail(args):
	"""Send execution results by email.

	Args:
		args (string): Execution results with WP commands.
	"""

	message = MIMEText(args, 'plain')
	date = datetime.now()

	message['Subject'] = date.strftime(MAIL_SUBJ)
	message['To'] = MAIL_TO
	message['From'] = MAIL_FROM

	mail = smtplib.SMTP(MAIL_SMTP, MAIL_PORT)
	mail.ehlo()
	if mail.has_extn('STARTTLS'):
		mail.starttls()
	mail.login(MAIL_USER, MAIL_PASS)

	mail.send_message(message)
	mail.quit()
	print('Execution results has been mailed.')
	return


def main():
	config = read_config()
	output = update_wp(config)
	send_mail(output)


if __name__ == '__main__':
	main()