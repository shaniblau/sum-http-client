def create_files():
    with open('./file_a', 'wb') as file:
        file.write(b'a')
    with open('./file_b', 'wb') as file:
        file.write(b'b')


def redis_cleanup(redis_client_fixture, key):
    redis_client_fixture.delete(key)
