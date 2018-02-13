from azure.storage.queue import QueueService

queue_service = QueueService(account_name='roian', account_key='1234qwer')
print('---1')
messages = queue_service.get_messages('taskqueue')
print('---2')

for message in messages:
    print(message.content)
    queue_service.delete_message('taskqueue', message.id, message.pop_receipt)