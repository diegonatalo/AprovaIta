"use client";

import { useSyncExternalStore } from "react";
import { ProgressRing } from "./ProgressRing";
import { useProgresso } from "@/lib/storage";

function assinarRelogio(f: () => void) {
  const id = setInterval(f, 60_000);
  return () => clearInterval(id);
}

export function Countdown({ alvoISO }: { alvoISO: string }) {
  // arredonda ao minuto para o snapshot ser estável entre leituras
  const agora = useSyncExternalStore(
    assinarRelogio,
    () => Math.floor(Date.now() / 60_000) * 60_000,
    () => 0,
  );
  if (!agora) return <p className="text-3xl font-bold">—</p>;
  const ms = new Date(alvoISO).getTime() - agora;
  if (ms <= 0) return <p className="text-xl font-bold">A prova já aconteceu.</p>;
  const dias = Math.floor(ms / 86_400_000);
  const horas = Math.floor((ms % 86_400_000) / 3_600_000);
  return (
    <p className="text-3xl font-bold">
      {dias} dias <span className="text-xl font-normal text-muted">e {horas}h</span>
    </p>
  );
}

export function ProgressoGeral({ chaves }: { chaves: string[] }) {
  const p = useProgresso();
  const vistos = chaves.filter((c) => (p.topicos[c] ?? "nao-visto") !== "nao-visto").length;
  const dominados = chaves.filter((c) => p.topicos[c] === "dominado").length;
  const pct = chaves.length ? (vistos / chaves.length) * 100 : 0;
  return (
    <div className="flex items-center gap-4">
      <ProgressRing valor={pct} rotulo="Conteúdo visto" />
      <p className="text-sm text-muted">
        {vistos} de {chaves.length} tópicos vistos
        <br />
        {dominados} dominados
      </p>
    </div>
  );
}
