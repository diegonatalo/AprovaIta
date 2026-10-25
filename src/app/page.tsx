import Link from "next/link";
import { NOMES_AREA, PROVA } from "../../config/prova";
import { SITE } from "../../config/site";
import { AREAS, listarTopicos } from "@/lib/content";
import { Countdown, ProgressoGeral } from "@/components/HomeWidgets";

export default function Home() {
  const topicos = listarTopicos();
  return (
    <div className="space-y-8">
      <section>
        <p className="text-sm font-semibold text-acento">{SITE.nome}</p>
        <h1 className="text-2xl font-bold">Agente Administrativo — Câmara de Itanhaém</h1>
        <p className="text-sm text-muted">
          Concurso nº 01/2026 · {PROVA.banca} · prova em 06/12/2026
        </p>
      </section>

      <section className="grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl border border-borda bg-card p-4">
          <h2 className="mb-1 text-sm font-semibold text-muted">Faltam para a prova</h2>
          <Countdown alvoISO={PROVA.dataProva} />
        </div>
        <div className="rounded-xl border border-borda bg-card p-4">
          <h2 className="mb-2 text-sm font-semibold text-muted">Progresso geral</h2>
          <ProgressoGeral chaves={topicos.map((t) => `${t.area}/${t.slug}`)} />
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-lg font-bold">Áreas</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          {AREAS.map((a) => (
            <Link
              key={a}
              href={`/conteudo/${a}/`}
              className="rounded-xl border border-borda bg-card p-4 hover:border-acento"
            >
              <p className="font-semibold">{NOMES_AREA[a]}</p>
              <p className="text-sm text-muted">
                {PROVA.distribuicao[a]} questões · {topicos.filter((t) => t.area === a).length} tópico(s) escritos
              </p>
            </Link>
          ))}
        </div>
      </section>

      <section className="flex flex-wrap gap-3">
        <Link href="/simulado/" className="rounded-lg bg-acento px-4 py-2 text-sm font-semibold text-background">
          Simulados
        </Link>
        <Link href="/revisao/" className="rounded-lg border border-borda px-4 py-2 text-sm">
          Caderno de erros
        </Link>
      </section>
    </div>
  );
}
