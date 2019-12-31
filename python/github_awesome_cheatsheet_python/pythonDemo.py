# ecoding:utf-8
import datetime
#单元测试
import unittest


print("hello")

#六种基本类型
i = 0

print (i)
t = None
if t is None:
    print  "none"
else :
    print "not none"

def showTimeDemo():
    #从字符串中创建 datetime
    # dt1 = datetime.datetime.strptime('20091031', '%Y%m%d')
    #获取当前的时间
    dt1 = datetime.datetime.now()
    print dt1.strftime('%m/%d/%Y %H:%M')
    #获取 date 对象
    print dt1.date()
    #获取 time 对象
    print dt1.time()

def lambdademo():
    '''lambda的demo'''
    a = lambda x : x*2
    print a(5)

class TestSubclass(unittest.TestCase):
  def test_func(self):
    self.assertEqual(0, 0)
    # 可以通过msg关键字参数提供测试失败时的提示消息
    self.assertEqual(0, 0, msg='modified message')
    self.assertGreater(1, 0)
    self.assertIn(0, [0])
    self.assertTrue(True)
    self.assertTrue(False)#在执行了unittest.main()后会crash，必须以test_开头
    # 测试是否会抛出异常
    # with self.assertRaises(KeyError):
    #   _ = dict()[1]

  def setUp(self):
      # To do: connect to the database
      pass

  def tearDown(self):
      # To do: release the connection
      pass

  def test_database(self):
      # To do: test the database
      pass
  # 被@unittest.skip装饰器装饰的测试类或测试函数会被跳过
  @unittest.skip(reason='just skip')
  def test_skip(self):
    raise Exception('I shall never be tested')

def test_testdemo():
    unittest.main()
    # TestSubclass().test_func()

test_testdemo()

