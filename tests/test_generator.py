import unittest, json, mock, random
from env import scripts
from mock import Mock
from scripts.generator import DataGenerator
from scripts.generator import AbstractDatum

class TestDataGenerator(unittest.TestCase):
	
	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_string_datum_good(self, mock1):
		gen = DataGenerator('char_gen_good.json', seed='1234567890')
		test_num = 500
		data = []
		for i in range(test_num):
			data.append(gen.generate())
		
		occ = {}
		total = 0
		for items in data:
			for key in items:
				total += 1
				if key in occ:
					occ[key] += 1
				else:
					occ[key] = 1
		
		assert len(occ.keys()) == 4
		for key in occ:
			assert occ[key] == test_num
						
#		for key in occ.keys():
#			print("KEY: " + key + " | OCC: " + str(occ[key]) + " | PROB: " + str( occ[key]/float(test_num) ))
		
		assert total == 4*test_num

	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_gen_key_check_field(self, mock1):
		try:
			gen = DataGenerator('char_gen_bad-01.json', seed='1234567890')
			self.fail('Should have failed with KeyError on fieldName')
		except KeyError as e:
			assert("Could not find 'fieldName' in field of schema:" in str(e))
			
	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_gen_key_check_type(self, mock1):
		try:
			gen = DataGenerator('char_gen_bad-02.json', seed='1234567890')
			self.fail('Should have failed with KeyError on type')
		except KeyError as e:
			assert('Could not find \'type\' in field of schema:' in str(e))
			
	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_gen_key_check_root(self, mock1):
		try:
			gen = DataGenerator('char_gen_bad-03.json', seed='1234567890')
			self.fail('Should have failed with TypeError')
		except TypeError as e:
			assert('Root of JSON Schema is not a list' in str(e))

		
	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_gen_check_field_type(self, mock1):
		try:
			gen = DataGenerator('char_gen_bad-04.json', seed='1234567890')
			self.fail('Should have failed with TypeError')
		except RuntimeError as e:
			assert('Field type was not found. Please change the field type or implement a new datum' in str(e))
			
	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_gen_check_values(self, mock1):
		try:
			gen = DataGenerator('char_gen_bad-05.json', seed='1234567890')
			self.fail('Should have failed with KeyError')
		except KeyError as e:
			assert('Missing key: values in field3' in str(e))

	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_gen_abstract_datum(self, mock1):
		try:
			field = {}
			field['fieldName'] = "ABC123"
			field['type'] = "ABC123"
			dat = AbstractDatum(field)
			dat.check()
			self.fail('Should raise not implemented error')
		except NotImplementedError as e:
			assert('AbstractDatum: This method should have been implemented by a sublcass' in str(e))
			
		try:
			field = {}
			field['fieldName'] = "ABC123"
			field['type'] = "ABC123"
			dat = AbstractDatum(field)
			dat.generate(random)
			self.fail('Should raise not implemented error')
		except NotImplementedError as e:
			assert('AbstractDatum: This method should have been implemented by a sublcass' in str(e))

	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_num_datum_good(self, mock1):
		gen = DataGenerator('num_gen_good.json')
		test_num = 500
		data = []
		mu1 = 0
		mu2 = 0
		for z in range(test_num):
			dat = gen.generate()
			assert type(dat['field1']) == int
			assert type(dat['field5']) == float
			mu1 += float(dat['field1'])/test_num
			mu2 += dat['field5']/test_num
			data.append(dat)
			assert(len(dat) == 11)
		assert(abs(mu1 - 50) < 10) # ensure they are at least in the right general range
		assert(abs(mu2 - 100) < 10)  # ensure they are at least in the right general range

		assert len(data) == test_num
		
		
	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_dup_fields(self, mock1):
		try:
			gen = DataGenerator('dup_fields.json')
			test_num = 10
			data = []
			mu1 = 0
			mu2 = 0
		except ValueError as e:
			assert 'Cannot have duplicate field names' in str(e)
		
	@mock.patch('scripts.config.get_conf_dir', return_value='res/')
	def test_bad_distribution(self, mock1):
		try:
			gen = DataGenerator('bad_dist.json')
		except ValueError as e:
			assert 'Distribution can only be one of: uniform, exponential, gaussian, or gamma' in str(e)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		