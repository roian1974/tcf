import multiprocessing
import time
from multiprocessing import Pool


def runSimulation(params):
    """This is the main processing function. It will contain whatever
    code should be run on multiple processors.

    """
    param1, param2 = params
    # Example computation
    processedData = []
    for ctr in range(1000000):
        processedData.append(param1 * ctr - param2 ** 2)

    return processedData


if __name__ == '__main__':
    # Define the parameters to test
    param1 = range(100)
    param2 = range(2, 202, 2)

    params = zip(param1, param2)

    pool = multiprocessing.Pool()

    # Parallel map
    tic = time.time()
    results = pool.map(runSimulation, params)
    toc = time.time()

    # Serial map
    tic2 = time.time()
    results = map(runSimulation, params)
    toc2 = time.time()

    print('Parallel processing time: %r\nSerial processing time: %r'
          % (toc - tic, toc2 - tic2))