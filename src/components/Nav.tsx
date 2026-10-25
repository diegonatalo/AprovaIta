"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSyncExternalStore } from "react";

const LINKS = [
  { href: "/", rotulo: "Início" },
  { href: "/conteudo/especificos/", rotulo: "Específicos" },
  { href: "/conteudo/portugues/", rotulo: "Português" },
  { href: "/conteudo/matematica/", rotulo: "Matemática" },
  { href: "/conteudo/legislacao/", rotulo: "Legislação" },
  { href: "/simulado/", rotulo: "Simulado" },
  { href: "/revisao/", rotulo: "Revisão" },
  { href: "/progresso/", rotulo: "Progresso" },
];

function assinarTema(f: () => void) {
  const o = new MutationObserver(f);
  o.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
  return () => o.disconnect();
}

export function Nav() {
  const caminho = usePathname();
  const escuro = useSyncExternalStore(
    assinarTema,
    () => document.documentElement.classList.contains("dark"),
    () => false,
  );
  function alternar() {
    const novo = !document.documentElement.classList.contains("dark");
    document.documentElement.classList.toggle("dark", novo);
    try {
      localStorage.setItem("tema", novo ? "dark" : "light");
    } catch {}
  }
  return (
    <header className="sticky top-0 z-10 border-b border-borda bg-background/95 backdrop-blur">
      <nav aria-label="Principal" className="mx-auto flex max-w-4xl items-center gap-1 overflow-x-auto px-3 py-2 text-sm">
        {LINKS.map((l) => (
          <Link
            key={l.href}
            href={l.href}
            aria-current={(l.href === "/" ? caminho === "/" : caminho.startsWith(l.href)) ? "page" : undefined}
            className="whitespace-nowrap rounded-md px-3 py-2 hover:bg-card aria-[current=page]:bg-card aria-[current=page]:font-semibold aria-[current=page]:text-acento"
          >
            {l.rotulo}
          </Link>
        ))}
        <button
          onClick={alternar}
          aria-label={escuro ? "Mudar para tema claro" : "Mudar para tema escuro"}
          className="ml-auto whitespace-nowrap rounded-md border border-borda px-3 py-2"
        >
          {escuro ? "Claro" : "Escuro"}
        </button>
      </nav>
    </header>
  );
}
