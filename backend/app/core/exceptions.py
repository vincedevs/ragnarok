class DocumentNotFoundError(Exception):
    """Raised when a document cannot be found"""


class InvalidDocumentError(Exception):
    """Raised when a document cannot be processed"""


class DocumentIngestionError(Exception):
    """Raised when a document cannot be indexed"""
