import type { StatusTopico } from "@/lib/tipos";

const ROTULO: Record<StatusTopico, string> = {
  "nao-visto": "Não visto",
  visto: "Visto",
  dominado: "Dominado",
};
const COR: Record<StatusTopico, string> = {
  "nao-visto": "border-borda text-muted",
  visto: "border-aviso text-aviso",
  dominado: "border-acerto text-acerto",
};

export function TopicStatusBadge({ status }: { status: StatusTopico }) {
  return (
    <span className={`inline-block rounded-full border px-2 py-0.5 text-xs font-medium ${COR[status]}`}>
      {ROTULO[status]}
    </span>
  );
}
