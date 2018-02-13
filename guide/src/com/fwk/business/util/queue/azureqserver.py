import time
from azure.storage.queue import QueueService

print('---1')

queue_service = QueueService(account_name='roian', account_key='1234qwer')
print('---2')

queue_service.create_queue('taskqueue')
print('---3')

cnt=0

while True:
    time.sleep(3)
    print('.')
    cnt += 1
    if cnt == 100:
        break

queue_service.delete_queue('taskqueue')
# queue_service.put_message('taskqueue', u'Hello World')
