class PortalAdapterInterface:
    """
        Interface for portal adapters. Each adapter should implement the adapt method to transform the data as needed.
    """
    def adapt(self, df):
        raise NotImplementedError("Subclasses must implement this method")

