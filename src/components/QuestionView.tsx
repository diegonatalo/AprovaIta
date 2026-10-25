"use client";

import { Markdown } from "./Markdown";
import type { Questao } from "@/lib/tipos";

const LETRAS = ["A", "B", "C", "D", "E"] as const;

/** Mostra uma questão. Com `revelar`, destaca gabarito e exibe o comentário. */
export function QuestionView({
  questao,
  numero,
  escolha,
  onEscolher,
  revelar,
  mostrarSituacao = true,
}: {
  questao: Questao;
  numero: number;
  escolha: number | null;
  onEscolher?: (i: number) => void;
  revelar: boolean;
  mostrarSituacao?: boolean;
}) {
  const nome = `q-${questao.id}`;
  return (
    <fieldset className="rounded-xl border border-borda bg-card p-4">
      <legend className="px-1 text-sm font-semibold text-muted">
        Questão {numero}
        {questao.origem === "banca" && questao.fonte
          ? ` · ${questao.fonte.orgao} ${questao.fonte.ano}, ${questao.fonte.cargo}, nº ${questao.fonte.numero}`
          : " · autoral"}
      </legend>
      <Markdown className="mb-3">{questao.enunciado}</Markdown>
      <div className="space-y-2">
        {questao.alternativas.map((alt, i) => {
          const certa = revelar && i === questao.gabarito;
          const errada = revelar && escolha === i && i !== questao.gabarito;
          return (
            <label
              key={i}
              className={`flex cursor-pointer items-start gap-3 rounded-lg border p-3 text-sm ${
                certa
                  ? "border-acerto bg-acerto/10"
                  : errada
                    ? "border-erro bg-erro/10"
                    : escolha === i
                      ? "border-acento bg-acento/10"
                      : "border-borda"
              }`}
            >
              <input
                type="radio"
                name={nome}
                className="mt-1"
                checked={escolha === i}
                disabled={revelar || !onEscolher}
                onChange={() => onEscolher?.(i)}
              />
              <span>
                <strong>{LETRAS[i]})</strong> {alt}
              </span>
            </label>
          );
        })}
      </div>
      {revelar && (
        <div className="mt-4 rounded-lg border border-borda p-3 text-sm">
          <p className="font-semibold">
            Gabarito: {LETRAS[questao.gabarito]}
            {mostrarSituacao &&
              (escolha === null ? " (não respondida)" : escolha === questao.gabarito ? " — você acertou" : " — você errou")}
          </p>
          {questao.origem === "banca" && questao.fonte && (
            <p className="mt-1 text-xs text-muted">Fonte do gabarito: {questao.fonte.gabaritoFonte} (preliminar; alterações pós-recurso não conferidas)</p>
          )}
          <Markdown className="mt-1 text-muted">{questao.comentario}</Markdown>
        </div>
      )}
    </fieldset>
  );
}
