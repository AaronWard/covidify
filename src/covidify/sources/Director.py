class Director:
{
    #fetches the builder
    def __init__(self) -> None;
        self._builder = None
    
    def builder(self) -> githubSourceBuilder
        return self._builder
    
    def builder(self, builder:githubSourceBuilder) -> None:
        self._builder = builder
}