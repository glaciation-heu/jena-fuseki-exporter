import logging


logger = logging.getLogger("jena_fuseki_exporter")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)+10s   %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)