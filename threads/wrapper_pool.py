from concurrent.futures import ThreadPoolExecutor


class wrapper_pool (ThreadPoolExecutor):
    __instance = None

    # ------------------------------------------------------------------------------------------------------------------

    class wrapper_pool (object):
        def __new__(cls):
            print("in new")
            if not hasattr (cls, 'instance'):
                cls.instance = super (wrapper_pool, cls).__new__ (cls)
                print('new instance')
            return cls.instance

    def __init__(self, max_workers=None, thread_name_prefix='', initializer=None, initargs=()):
        print("in init")
        super ().__init__ (max_workers, thread_name_prefix, initializer, initargs)



