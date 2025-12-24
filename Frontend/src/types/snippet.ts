export enum SnippetType {
  CODE = "code",
  MARKDOWN = "markdown",
  ARCHIVE = "archive",
  LINK = "link",
  PROMPT = "prompt"
}

export interface Snippet {
  id: number
  title: string
  content: string
  snippet_type: SnippetType
  technology_id: number
}

export interface SnippetCreate {
  title: string
  snippet_type: SnippetType
  content: string
  technology_id: number
}
