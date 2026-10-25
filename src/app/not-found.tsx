import Link from "next/link";
import type { Metadata } from "next";
import { NOMES_AREA } from "../../config/prova";
import { AREAS } from "@/lib/content";

export const metadata: Metadata = { title: "Página não encontrada" };

export default function NaoEncontrada() {
  return (
    <div className="mx-auto max-w-xl space-y-6 py-10 text-center">
      <p className="text-6xl font-bold text-acento" aria-hidden="true">404</p>
      <h1 className="text-2xl font-bold">Essa página não existe</h1>
      <p className="text-muted">
        O endereço pode ter mudado ou estar digitado errado. Volte ao início ou escolha uma área para continuar estudando.
      </p>
      <Link href="/" className="inline-block rounded-lg bg-acento px-5 py-3 font-semibold text-background">
        Ir para o início
      </Link>
      <nav aria-label="Áreas de estudo" className="flex flex-wrap justify-center gap-2 text-sm">
        {AREAS.map((a) => (
          <Link key={a} href={`/conteudo/${a}/`} className="rounded-md border border-borda px-3 py-2 hover:bg-card">
            {NOMES_AREA[a]}
          </Link>
        ))}
        <Link href="/simulado/" className="rounded-md border border-borda px-3 py-2 hover:bg-card">Simulado</Link>
        <Link href="/progresso/" className="rounded-md border border-borda px-3 py-2 hover:bg-card">Progresso</Link>
      </nav>
    </div>
  );
}
