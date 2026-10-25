<div align="center">

<img src="public/icon.svg" alt="Logo do Aprova Ita: um check branco sobre fundo verde-petróleo, com um sol coral e uma onda" width="84" height="84" />

# Aprova Ita

**Estude para a Câmara de Itanhaém direto do celular.**<br />
Explicações objetivas, questões comentadas, simulados cronometrados e um caderno que lembra o que você errou.

<br />

![Next.js](https://img.shields.io/badge/Next.js_16-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React_19-20232a?style=flat-square&logo=react&logoColor=61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-3178c6?style=flat-square&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS_4-06b6d4?style=flat-square&logo=tailwindcss&logoColor=white)
![Dados no navegador](https://img.shields.io/badge/dados-só_no_seu_navegador-0a6b7c?style=flat-square)

</div>

<br />

Site de estudos para o **Concurso nº 01/2026 da Câmara Municipal de Itanhaém**
(cargo Agente Administrativo, banca VUNESP, prova em 06/12/2026).
São 40 questões: 8 de Português, 5 de Matemática, 3 de Legislação Municipal e 24 de Conhecimentos Específicos.

## ✨ O que dá para fazer

| Recurso | Descrição |
|---|---|
| **Estudar por área** | 47 tópicos em Português, Matemática, Legislação e Específicos, cada um com explicação e questões. |
| **Quiz por tópico** | Quiz A com questões autorais e Quiz B com questões reais da VUNESP, com gabarito comentado. |
| **Simulados** | Prova de 40 questões com cronômetro de 3h, pausa, marcação para revisar e folha de respostas. |
| **Nota como no edital** | Acertos × 100 ÷ 40, com aviso de habilitação (nota mínima 50). |
| **Caderno de erros** | Tudo o que você errou fica guardado. Acertou ao refazer? A questão sai do caderno. |
| **Progresso** | Tópicos vistos e dominados, desempenho por área, pontos fracos e próximo passo sugerido. |
| **Contagem regressiva** | Quantos dias faltam para a prova, na tela inicial. |
| **Tema claro e escuro** | Segue o tema do aparelho e dá para trocar na hora. |

## 🔒 Seus dados

Não há conta nem servidor. Seu progresso, os simulados e o caderno de erros ficam no
`localStorage` do navegador. Depois da primeira visita, o site também abre sem internet.

Para trocar de aparelho ou não perder nada ao limpar o navegador, use **Progresso → Backup**:
exporte um arquivo JSON e importe no outro lugar.

## 🧠 Como funciona

| Conceito | Regra |
|---|---|
| **Nota** | `acertos × 100 ÷ 40`. Habilitado com nota igual ou maior que 50 (20 acertos). |
| **Simulado completo** | 40 questões na proporção da prova. Prefere questões que você ainda não fez. |
| **Simulado reduzido** | Se o banco não cobre algum grupo, o simulado sai menor e a nota **não** é comparável ao corte. |
| **Cronômetro** | Calculado pelo relógio, então não perde tempo se a aba ficar em segundo plano. |
| **Prova em andamento** | Fica salva. Você pode recarregar a página e retomar de onde parou. |

## 📚 Sobre o conteúdo

> [!NOTE]
> O conteúdo foi produzido com apoio de IA e **não substitui o edital nem as normas oficiais**.
> Confira os pontos marcados com `VERIFICAR` antes de decorar.

- **Questões da banca** só entram quando vêm de provas reais da VUNESP e têm fonte. Os gabaritos usados
  são os preliminares; mudanças após recursos não foram conferidas.
- **Questões autorais** são identificadas como tal na tela.
- **Legislação municipal:** ainda não há questões reais da banca para esse grupo.
- **Divisão dos 24 Específicos** entre Administração Geral (10), Arquivologia (6) e Administração Pública (8)
  é uma suposição, porque o edital não informa. Ela fica em `config/prova.ts` e pode ser mudada.
- Alguns tópicos estão marcados como "fora do programa do edital" e ficam sinalizados no site.

## 🚀 Rodando localmente

Requer [Node.js](https://nodejs.org) e npm.

```bash
git clone https://github.com/diegonatalo/AprovaIta.git
cd AprovaIta
npm install
npm run dev        # http://localhost:3000
```

| Comando | O que faz |
|---|---|
| `npm run dev` | Servidor de desenvolvimento |
| `npm run build` | Gera o site estático em `out/` |
| `npm run lint` | Roda o ESLint |
| `npm run validate` | Confere o conteúdo: fontes, gabaritos e alternativas (`validate:strict` trata avisos como erros) |
| `npm run test:motor` | Testa a correção e a montagem dos simulados |

## 🗂️ Estrutura

```text
src/
├── app/          rotas: início, conteúdo, simulado, revisão e progresso
├── components/   interface: navegação, questões, prova, painéis
└── lib/          carga do conteúdo, correção, simulados e armazenamento local
content/          um tópico por pasta: explicação e questões
config/           parâmetros da prova (prova.ts) e identidade do site (site.ts)
scripts/          validação do conteúdo e testes do motor
public/           ícone, manifest e service worker
```

<details>
<summary><b>Como adicionar um tópico</b></summary>

1. Crie a pasta `content/<area>/<topico>/` (em Específicos, dentro da subárea).
2. Escreva `explicacao.mdx` com `titulo`, `ordem` e `resumo` no cabeçalho.
3. Adicione `questoes-autorais.json` (Quiz A) e, se houver prova real com fonte, `questoes-banca.json` (Quiz B).
4. Rode `npm run validate` e corrija o que ele apontar.

</details>

## 🌐 Deploy

O site é 100% estático (`output: "export"`), então roda em qualquer hospedagem, como a Vercel.
Ao publicar, ajuste o endereço em `config/site.ts`: ele alimenta o `sitemap.xml`, o `robots.txt` e os metadados.

## 🧭 Próximos passos

- [ ] Questões reais da banca para Legislação Municipal (falta prova de Câmara que cubra o tema).
- [ ] Conferir se houve mudança de gabarito após recursos nas provas usadas.
- [ ] Confirmar o horário exato da prova no edital.
- [ ] Definir o endereço público e atualizar `config/site.ts`.
- [ ] Capturas de tela e imagem de compartilhamento (Open Graph).
- [ ] Testes automatizados da interface (hoje só há validação do conteúdo e teste do motor).

<br />

<div align="center">
  <sub>Feito com 💚 para quem estuda no ônibus, na fila e na hora do almoço.</sub>
</div>
