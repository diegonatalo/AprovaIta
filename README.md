# Aprova Ita

Site de estudos para o Concurso Público nº 01/2026 da Câmara Municipal de Itanhaém
(Agente Administrativo, VUNESP, prova em 06/12/2026).

Next.js (App Router, exportação estática) + TypeScript + Tailwind. O progresso fica no
`localStorage` do navegador.

## Comandos

```bash
npm run dev            # servidor local em http://localhost:3000
npm run validate       # confere o conteúdo (fontes, gabaritos, alternativas)
npm run test:motor     # testa a lógica de correção e simulados
npm run lint
npm run build          # gera o site estático em out/
```

## Conteúdo

Cada tópico fica em `content/<area>/<topico>/`:

- `explicacao.mdx`: resumo do conteúdo, com a fonte e os pontos a verificar.
- `questoes-autorais.json`: questões autorais (Quiz A).
- `questoes-banca.json`: questões reais da banca, com fonte e gabarito oficial (Quiz B).

Parâmetros da prova em `config/prova.ts`; nome e endereço do site em `config/site.ts`.
A pasta `fontes/` (provas e normas usadas na conferência) fica só na máquina local.
