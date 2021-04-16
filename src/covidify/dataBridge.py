import matplotlib.image as mpimg
import pandas as pd
from PIL import Image
from __future__ import annotations
from abc import ABC, abstractmethod 

#Abstract data injestion
class AbstractDataInjestion:

    def __init__(self, implementation: Implementation) -> None:
        self.implementation = implementation

    def injestion(self) -> str:
        return (f"Reading .png:\n" f"{self.implementation.injestion_implementation()}")

#1st Extended abstract data injestion, reads .tsv file
class csvDataInjestion(AbstractDataInjestion):
    def injestion(self) -> str:
        return (f"Reading .csv:\n"f"{self.implementation.injestion_implementation()}")

#2nd Extended abstract data injestion, reads .csv file
class jpgDataInjestion(AbstractDataInjestion):
    def injestion(self) -> str:
        return (f"Reading .jpg:\n"f"{self.implementation.injestion_implementation()}")

class Implementation(ABC):
    @abstractmethod
    def injestion_implementation(self) -> str:
        pass

class pngConcreteImplementation(Implementation):
    def injestion_implementation(self) -> str:
        img = mpimg.imread('/image_path.png')
        print("Done Reading png!\n")
        return img

class csvConcreteImplementation(Implementation):
    def injestion_implementation(self) -> str:
        dt = pd.read_csv(r'/data.csv')
        print("Done Reading csv!\n")
        return dt

class jpgConcreteImplementation(Implementation):
    def injestion_implementation(self) -> str:
        img = Image.open("/image_path.jpg")
        print("Done reading jpg!\n")
        return img

def client_code(abstraction: AbstractDataInjestion) -> None:
    print(abstraction.injestion(), end="")

if __name__ == "__main__":
    implementation = pngConcreteImplementation()
    abstraction = AbstractDataInjestion(implementation)
    client_code(abstraction)

    implementation = csvConcreteImplementation()
    abstraction = csvDataInjestion(implementation)
    client_code(abstraction)

    implementation = jpgConcreteImplementation()
    abstraction = jpgDataInjestion(implementation)
    client_code(abstraction)