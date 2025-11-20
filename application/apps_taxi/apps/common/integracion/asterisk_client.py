import json
import logging

import requests

logger = logging.getLogger(__name__)


class AsteriskCliente:
    __urlbase = ""
    __username = ""
    __password = ""

    def __init__(self, _urlbase, _username, _password):
        self.__urlbase = _urlbase[:-1] if _urlbase.endswith("/") else _urlbase
        self.__username = _username
        self.__password = _password

    def get_url(self, endpoint):
        return f"{self.__urlbase}/{endpoint}"

    def get_request(self, method, raw_url, data_dict, **kwargs):
        mesnsaje = "Falló la conexión al servidor. {error}"
        try:
            if method.lower() == "post":
                raw_data = json.dumps(data_dict)
                response = requests.post(
                    raw_url,
                    raw_data,
                    auth=(self.__username, self.__password),
                    timeout=600,
                    verify=False,
                )
            elif method.lower() == "get":
                response = requests.get(
                    raw_url,
                    params=data_dict,
                    auth=(self.__username, self.__password),
                    timeout=600,
                    verify=False,
                )
            else:
                raise Exception("No se conecto al intermediario")
            return response
        except requests.exceptions.RequestException as err:
            logger.error(mesnsaje.format(error=str(err)), exc_info=True)
            raise Exception(str(err))
        except requests.exceptions.HTTPError as errh:
            logger.error(mesnsaje.format(error=str(errh)), exc_info=True)
            raise Exception(str(errh))
        except requests.exceptions.ConnectionError as errc:
            logger.error(mesnsaje.format(error=str(errc)), exc_info=True)
            raise Exception(str(errc))
        except requests.exceptions.Timeout as errt:
            logger.error(mesnsaje.format(error=str(errt)), exc_info=True)
            raise Exception(str(errt))
        except Exception as ex:
            logger.error(mesnsaje.format(error=str(ex)), exc_info=True)
            raise Exception(str(ex))

    def get_endpoint(self, endpoint, **kwargs):
        return self.get_request("get", self.get_url(endpoint), kwargs)

    def post_endpoint(self, endpoint, **kwargs):
        return self.get_request("post", self.get_url(endpoint), kwargs)
