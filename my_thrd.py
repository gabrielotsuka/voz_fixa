import threading 
import time

def testSleep (n, name):
	print('This is the {}. Will sleep for {} seconds'.format(name,n))
	time.sleep(n)
	print('Slept well.')

t = threading.Thread(target = testSleep, name = 'thread1', args = (5,'thread1'))

t.start()

print('hihihihi')