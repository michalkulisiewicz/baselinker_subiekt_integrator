import logging

logging.basicConfig(filename='log.log', level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger('subiekt')