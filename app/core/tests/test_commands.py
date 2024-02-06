
"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check') # mock the check method in commands/wait_for_db
class CommandTests(SimpleTestCase):
  """Test Commands"""
  def test_wait_for_db_ready(self, patched_check): # patched_check is the mocked version of the check method above
    """Test waiting for db if db is ready"""
    patched_check.return_value = True # we control what the mocked version of check returns
    call_command('wait_for_db') # execute the code inside commands/wait_for_db
    patched_check.assert_called_once_with(databases=['default'])

  @patch('time.sleep')
  def test_wait_for_db_delay(self, patched_sleep, patched_check):
    """Test waiting for db when getting OperationalError"""
    patched_check.side_effect = [Psycopg2OpError] * 2 + \
        [OperationalError] * 3 + [True]

    call_command('wait_for_db')
    self.assertEqual(patched_check.call_count, 6)
    patched_check.assert_called_with(databases=['default'])
