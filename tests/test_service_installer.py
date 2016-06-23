import unittest, json, mock, scripts
from env import scripts
from mock import Mock
from scripts import service_installer

non_linux_distro = ['', '', '']
other_linux_distro = ['mint', '', '']
centos_6_distro = ['CentOS', '6.8', 'Final']
centos_7_distro = ['CentOS', '7.1', 'Final']
ubuntu_12_distro = ['Ubuntu', '12.04', 'precise']
ubuntu_14_distro = ['Ubuntu', '14.04', 'trusty']
bad_ubuntu = ['Ubuntu', '1', 'NaN']

class TestHDPSelectInstall(unittest.TestCase):
	
	@mock.patch('platform.linux_distribution', return_value=centos_6_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['/usr/bin/hdp-select', ''])
	def test_hdp_select_centos_6_pass(self, mock, mock2):
		assert True == service_installer.install_hdp_select()
		
	
	@mock.patch('platform.linux_distribution', return_value=centos_7_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['/usr/bin/hdp-select', ''])
	def test_hdp_select_centos_7_pass(self, mock, mock2):
		assert True == service_installer.install_hdp_select()
	
	@mock.patch('platform.linux_distribution', return_value=ubuntu_12_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['/usr/bin/hdp-select', ''])
	def test_hdp_select_ubuntu_12_pass(self, mock, mock2):
		assert True == service_installer.install_hdp_select()
		
	@mock.patch('platform.linux_distribution', return_value=ubuntu_14_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['/usr/bin/hdp-select', ''])
	def test_hdp_select_ubuntu_14_pass(self, mock, mock2):
		assert True == service_installer.install_hdp_select()
		
		
	@mock.patch('platform.linux_distribution', return_value=centos_6_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['', ''])
	def test_hdp_select_centos_6_fail(self, mock, mock2):
		assert False == service_installer.install_hdp_select()
	
	@mock.patch('platform.linux_distribution', return_value=centos_7_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['', ''])
	def test_hdp_select_centos_7_fail(self, mock, mock2):
		assert False == service_installer.install_hdp_select()
	
	@mock.patch('platform.linux_distribution', return_value=ubuntu_12_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['', ''])
	def test_hdp_select_ubuntu_12_fail(self, mock, mock2):
		assert False == service_installer.install_hdp_select()
		
	@mock.patch('platform.linux_distribution', return_value=ubuntu_14_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['', ''])
	def test_hdp_select_ubuntu_14_fail(self, mock, mock2):
		assert False == service_installer.install_hdp_select()
		
	@mock.patch('platform.linux_distribution', return_value=bad_ubuntu)
	@mock.patch('scripts.shell.Shell.run', return_value=['', ''])
	def test_hdp_select_bad_ubuntu(self, mock, mock2):
		try:
			service_installer.install_hdp_select()
			self.fail('Should fail with a non-linux operating system')
		except EnvironmentError as e:
			assert str(e.message) == 'Must be using one of: CentOS 6.x, CentOS 7.x, Ubuntu 12.x, Ubuntu 14.x'
		
	
	@mock.patch('platform.linux_distribution', return_value=non_linux_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['/usr/bin/hdp-select', ''])
	def test_hdp_select_non_linux(self, mock, mock2):
		try:
			service_installer.install_hdp_select()
			self.fail('Should fail with a non-linux operating system')
		except EnvironmentError as e:
			assert str(e.message) == 'You must be running a linux distribution to install hdp-select'
			
	@mock.patch('platform.linux_distribution', return_value=other_linux_distro)
	@mock.patch('scripts.shell.Shell.run', return_value=['/usr/bin/hdp-select', ''])
	def test_hdp_select_other_linux(self, mock, mock2):
		try:
			service_installer.install_hdp_select()
			self.fail('Should fail with a non-linux operating system')
		except EnvironmentError as e:
			assert str(e.message) == 'Must be using one of: CentOS 6.x, CentOS 7.x, Ubuntu 12.x, Ubuntu 14.x'

class TestComponentCheck(unittest.TestCase):

	@mock.patch('scripts.shell.Shell.run', return_value=['/usr/bin/hdp-select', ''])
	def test_hdp_select_good(self, mock):
		assert service_installer.is_hdp_select_installed() == True
			
	@mock.patch('scripts.shell.Shell.run', return_value=['', ''])
	def test_hdp_select_bad(self, mock):
			assert service_installer.is_hdp_select_installed() == False
			
	@mock.patch('scripts.shell.Shell.run', return_value=['/usr/bin/ambari-server', ''])
	def test_ambari_good(self, mock):
		assert service_installer.is_ambari_installed() == True
			
	@mock.patch('scripts.shell.Shell.run', return_value=['', ''])
	def test_ambari_bad(self, mock):
			assert service_installer.is_ambari_installed() == False
			
class TestZeppelinInstall(unittest.TestCase):

	@mock.patch('scripts.service_installer.is_ambari_installed', return_value=False)
	def test_zeppelin_ambari_bad(self, mock):
		try:
			service_installer.install_zeppelin()
			self.fail('Cannot continue installation without Ambari')
		except EnvironmentError as e:
			assert str(e.message) == 'You must install the demo on the same node as the Ambari server. Install Ambari here or move to another node with Ambari installed before continuing'
			
	@mock.patch('scripts.service_installer.is_ambari_installed', return_value=True)
	@mock.patch('scripts.service_installer.is_hdp_select_installed', return_value=False)
	@mock.patch('scripts.service_installer.install_hdp_select', return_value=False)
	def test_zeppelin_ambari_good(self, mock, mock2, mock3): #Also HDP select bad
		try:
			service_installer.install_zeppelin()
			self.fail('Cannot continue installation without hdp-select')
		except EnvironmentError as e:
			assert str(e.message) == 'hdp-select could not be installed. Please install it manually and then re-run the setup.'
			
	@mock.patch('scripts.service_installer.is_ambari_installed', return_value=True)
	@mock.patch('scripts.service_installer.is_hdp_select_installed', return_value=True)
	@mock.patch('scripts.service_installer.install_hdp_select', return_value=True)
	@mock.patch('scripts.service_installer.check_ambari_service_installed', return_value=True)
	@mock.patch('__builtin__.raw_input', return_value='y')
	def test_zeppelin_check_is_good(self, mock, mock2, mock3, mock4, mock5):
			assert service_installer.install_zeppelin() == True
			
			
	@mock.patch('scripts.service_installer.is_ambari_installed', return_value=True)
	@mock.patch('scripts.service_installer.is_hdp_select_installed', return_value=True)
	@mock.patch('scripts.service_installer.install_hdp_select', return_value=True)
	@mock.patch('scripts.service_installer.check_ambari_service_installed', return_value=False)
	@mock.patch('__builtin__.raw_input', side_effect=['\n', '\n', 'v', 'y'])
	def test_zeppelin_no_ambari_contact_continue(self, mock, mock2, mock3, mock4, mock5):
			assert service_installer.install_zeppelin() == True
			
	
	@mock.patch('scripts.service_installer.is_ambari_installed', return_value=True)
	@mock.patch('scripts.service_installer.is_hdp_select_installed', return_value=True)
	@mock.patch('scripts.service_installer.install_hdp_select', return_value=True)
	@mock.patch('scripts.service_installer.check_ambari_service_installed', return_value=False)
	@mock.patch('__builtin__.raw_input', side_effect=['\n', '\n', 'v', 'n'])
	def test_zeppelin_no_ambari_contact_no_continue(self, mock, mock2, mock3, mock4, mock5):
			assert service_installer.install_zeppelin() == False
			
class TestAmbariServiceCheck(unittest.TestCase):
	

	@mock.patch('scripts.curl_client.CurlClient.make_request', side_effect=[['', ''], ['200 OK', '']])
	@mock.patch('__builtin__.raw_input', side_effect=['\n', '\n', 'v', 'n'])
	def test_ambari_check_good(self, mock, mock2):
		conf = scripts.config.read_config('global-config.conf')['AMBARI']
		assert service_installer.check_ambari_service_installed('ZEPPELIN', conf) == True
		
	@mock.patch('scripts.curl_client.CurlClient.make_request', side_effect=[['200 OK', ''], ['200 OK', '']])
	@mock.patch('__builtin__.raw_input', side_effect=['\n', '\n', 'v', 'n'])
	def test_ambari_check_false(self, mock, mock2):
		conf = scripts.config.read_config('global-config.conf')['AMBARI']
		assert service_installer.check_ambari_service_installed('ZEPPELIN', conf) == True
		
		
	@mock.patch('scripts.curl_client.CurlClient.make_request', side_effect=[['', ''],['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', '']])
	@mock.patch('__builtin__.raw_input', side_effect=['', '', '', '', '', '', '', '', '', '', ''])
	def test_ambari_check_many_attempts(self, mock, mock2):
		conf = scripts.config.read_config('global-config.conf')['AMBARI']
		assert service_installer.check_ambari_service_installed('ZEPPELIN', conf) == False
	
#
#class TestZeppelinAddNotebook(unittest.TestCase):
#	
#	
			
			