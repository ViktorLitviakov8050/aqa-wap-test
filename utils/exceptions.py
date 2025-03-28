class TwitchTestError(Exception):
    """Base exception for all Twitch test errors"""
    pass

class ElementNotFoundError(TwitchTestError):
    """Raised when an element cannot be found"""
    pass

class ElementNotClickableError(TwitchTestError):
    """Raised when an element cannot be clicked"""
    pass

class NavigationError(TwitchTestError):
    """Raised when navigation fails"""
    pass

class SearchError(TwitchTestError):
    """Raised when search operation fails"""
    pass

class StreamerSelectionError(TwitchTestError):
    """Raised when streamer selection fails"""
    pass 