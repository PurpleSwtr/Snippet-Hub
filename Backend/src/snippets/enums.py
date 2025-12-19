from enum import Enum

class SnippetType(str, Enum):
    CODE = "code"
    MARKDOWN = "markdown"
    # IMAGE = "image"
    ARCHIVE = "archive"
    LINK = "link"
    PROMPT = "prompt"

class OptionType(str, Enum):
    FORMAT = "format"
    MODIFIER = "modifier" 
    ROLE = "role"
    TEMPLATE = "template"

class CategoryType(str, Enum):
    GENERAL = "general"
    PROGRAMMING = "programming"
    DESIGN = "design"
    DOCUMENTATION = "documentation"
    SECURITY = "security"
    DATA_SCIENCE = "data_science"
    DEVOPS = "devops"
    BUSINESS = "business"