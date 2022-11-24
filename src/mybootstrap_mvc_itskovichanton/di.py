from opyoid import Module
from src.mybootstrap_core_itskovichanton.di import CoreModule


class MVCModule(Module):
    def configure(self) -> None:
        self.install(CoreModule)
