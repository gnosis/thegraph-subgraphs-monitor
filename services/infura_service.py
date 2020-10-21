import requests
import os


class InfuraService(Exception):
    pass


class InfuraNetworkNotSupported(InfuraService):
    pass


class InfuraEndpointUnavailableException(InfuraService):
    pass


class InfuraTokenNotDefinedException(InfuraService):
    pass


INFURA_TOKEN = os.environ.get('INFURA_TOKEN')


class InfuraProvider:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = InfuraService()
        return cls.instance

    @classmethod
    def del_singleton(cls):
        if hasattr(cls, "instance"):
            del cls.instance


class InfuraService:
    def __init__(self, infura_token: str = INFURA_TOKEN):
        """
        :param infura_token: str. Infura specifies a token to control service usage
        """

        if not infura_token:
            raise InfuraTokenNotDefinedException()

        self.infura_token = infura_token

        self.mainnet_url = f'https://mainnet.infura.io/v3/{self.infura_token}'
        self.rinkeby_url = f'https://rinkeby.infura.io/v3/{self.infura_token}'

        # Get latest blocks to only do it one time
        self.latest_mainnet_block_number = self.get_latest_mainnet_block_number()
        self.latest_rinkeby_block_number = self.get_latest_rinkeby_block_number()

    def get_latest_mainnet_block_number(self) -> int:
        """
        Get latest MAINNET block number from Infura service
        :return: int
        """

        response = requests.post(url=self.mainnet_url,
                                 json={"jsonrpc":"2.0","method":"eth_blockNumber","params": [],"id":1},
                                 timeout=2)

        response_json = response.json()

        # Hex to int
        infura_mainnet_latest_block = int(response_json['result'], 16)

        return infura_mainnet_latest_block

    def get_latest_rinkeby_block_number(self) -> int:
        """
        Get latest RINKEBY block number from Infura service
        :return: int
        """

        response = requests.post(url=self.rinkeby_url,
                                 json={"jsonrpc":"2.0","method":"eth_blockNumber","params": [],"id":1},
                                 timeout=2)

        if response:
            response_json = response.json()
            # Hex to int
            infura_mainnet_latest_block = int(response_json['result'], 16)

            return infura_mainnet_latest_block
        else:
            raise InfuraEndpointUnavailableException()

    def get_latest_block_number_of_network(self, network: str) -> int:
        """
        Get latest block number of network requested
        Only mainnet and rinkeby networks are supported
        :return: int
        """

        if network == 'mainnet':
            return self.latest_mainnet_block_number
        elif network == 'rinkeby':
            return self.latest_rinkeby_block_number
        else:
            raise InfuraNetworkNotSupported()
