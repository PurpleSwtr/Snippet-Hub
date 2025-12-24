import type { TagBase } from "./tag"

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
  tags: { id: number; name: string }[]
}

export interface SnippetCreate {
  title: string
  snippet_type: SnippetType
  content: string
  technology_id: number
  tags: { name: string }[]
}
