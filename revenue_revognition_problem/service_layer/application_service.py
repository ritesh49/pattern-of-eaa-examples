from abc import ABC, abstractmethod

class EmailGateway(ABC):

    @abstractmethod
    def send_email_message(self, to_address: str, subject: str, body: str):
        pass


class IntegrationGateway(ABC):
    
    @abstractmethod
    def publish_revenue_recognitions_calculation(self, contract: Contract):
        pass


class ApplicationService:
    def _get_email_gateway(self) -> EmailGateway:
        # return instance of EmailGateway
        pass
    
    def _get_integration_gateway(self) -> IntegrationGateway:
        # return instance of IntegrationGateway
        pass


class RecognitionService(ApplicationService):
    def calculate_revenue_recognitions(self, contract_number: int):
        contract: Contract = Contract.read_for_update(contract_number)
        contract.calculate_recognitions()
        self._get_email_gateway().send_email_message(contract.get_administrator_address(),
                                                    "RE: Contract #" + contract_number,
                                                    contract + "has had revenue recognition calculated.")
        self._get_integration_gateway().publish_revenue_recognitions_calculation(contract)
    
    def recognized_revenue(self, contract_number:int, as_of: Date):
        return Contract.read(contract_number).recognized_revenue(as_of)
    
