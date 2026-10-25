import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/** Renderiza Markdown (explicações e enunciados). Tabelas ganham rolagem horizontal no celular. */
export function Markdown({ children, className = "" }: { children: string; className?: string }) {
  return (
    <div className={className}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          table: ({ children }) => (
            <div className="tabela">
              <table>{children}</table>
            </div>
          ),
          input: ({ type, checked }) =>
            type === "checkbox" ? (
              <input type="checkbox" checked={checked} disabled readOnly className="mr-2" />
            ) : null,
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
