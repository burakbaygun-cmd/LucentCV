"use client";

import ReactMarkdown from "react-markdown";

interface MarkdownViewerProps {
  content: string;
}

export function MarkdownViewer({ content }: MarkdownViewerProps) {
  return (
    <div className="prose prose-sm dark:prose-invert max-w-none prose-headings:text-primary prose-a:text-secondary">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
}
