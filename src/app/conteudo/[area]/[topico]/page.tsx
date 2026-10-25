import Link from "next/link";
import { notFound } from "next/navigation";
import { NOMES_AREA } from "../../../../../config/prova";
import { acharTopico, listarTopicos } from "@/lib/content";
import { Markdown } from "@/components/Markdown";
import { QuizCard } from "@/components/QuizCard";
import { StatusButtons } from "@/components/StatusButtons";
import type { Area } from "@/lib/tipos";

export function generateStaticParams() {
  return listarTopicos().map((t) => ({ area: t.area, topico: t.slug }));
}

export default async function PaginaTopico({
  params,
}: {
  params: Promise<{ area: string; topico: string }>;
}) {
  const { area, topico } = await params;
  const t = acharTopico(area, topico);
  if (!t) notFound();
  const chave = `${t.area}/${t.slug}`;

  return (
    <article className="space-y-8">
      <header className="space-y-3">
        <Link href={`/conteudo/${t.area}/`} className="text-sm text-acento">
          ← {NOMES_AREA[t.area as Area]}
        </Link>
        <h1 className="text-2xl font-bold">{t.titulo}</h1>
        {t.statusFonte === "PENDENTE_FONTE" && (
          <p className="rounded-lg border border-erro p-3 text-sm text-erro">
            PENDENTE_FONTE: este tópico depende do texto oficial e ainda não foi conferido.
          </p>
        )}
        <StatusButtons chave={chave} />
      </header>

      <Markdown className="prose-estudo">{t.conteudo}</Markdown>

      <QuizCard chave={chave} quiz="A" questoes={t.autorais} />
      <QuizCard chave={chave} quiz="B" questoes={t.banca} />
    </article>
  );
}
