import Link from "next/link";
import { notFound } from "next/navigation";
import { NOMES_AREA, NOMES_SUBAREA, PROVA } from "../../../../config/prova";
import { AREAS, topicosDaArea } from "@/lib/content";
import { StatusDoTopico } from "@/components/StatusButtons";
import type { Area } from "@/lib/tipos";

export function generateStaticParams() {
  return AREAS.map((area) => ({ area }));
}

export default async function PaginaArea({ params }: { params: Promise<{ area: string }> }) {
  const { area } = await params;
  if (!AREAS.includes(area as Area)) notFound();
  const a = area as Area;
  const topicos = topicosDaArea(a);

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold">{NOMES_AREA[a]}</h1>
        <p className="text-sm text-muted">{PROVA.distribuicao[a]} questões na prova</p>
      </header>
      {topicos.length === 0 ? (
        <p className="rounded-xl border border-dashed border-borda p-4 text-sm text-muted">
          Nenhum tópico escrito nesta área ainda.
        </p>
      ) : (
        <ul className="space-y-3">
          {topicos.map((t) => (
            <li key={t.slug}>
              <Link
                href={`/conteudo/${t.area}/${t.slug}/`}
                className="flex items-start justify-between gap-3 rounded-xl border border-borda bg-card p-4 hover:border-acento"
              >
                <span>
                  {t.subarea && <span className="block text-xs text-muted">{NOMES_SUBAREA[t.subarea]}</span>}
                  <span className="font-semibold">{t.titulo}</span>
                  <span className="block text-sm text-muted">{t.resumo}</span>
                  {t.statusFonte === "PENDENTE_FONTE" && (
                    <span className="text-xs font-semibold text-erro">PENDENTE_FONTE</span>
                  )}
                </span>
                <StatusDoTopico chave={`${t.area}/${t.slug}`} />
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
