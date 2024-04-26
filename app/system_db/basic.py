from abc import ABC,abstractmethod

class BasicCRUD(ABC):
    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def get_preview_data(self,offset:int,columns:list,tablename:str):
        pass

    @abstractmethod
    def get_types(self,tablename:str):
        pass