class LLMException(Exception):
    """Base exception for all LLM errors."""


class AuthenticationError(LLMException):
    """Invalid API credentials."""


class RateLimitError(LLMException):
    """Rate limit exceeded."""


class ProviderUnavailableError(LLMException):
    """Provider unavailable."""


class InvalidRequestError(LLMException):
    """Invalid request."""