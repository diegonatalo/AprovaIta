import type { Metadata, Viewport } from "next";
import { Geist } from "next/font/google";
import "./globals.css";
import { Nav } from "@/components/Nav";
import { RegistrarSW } from "@/components/RegistrarSW";
import { SITE } from "../../config/site";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title: { default: `${SITE.nome} — Agente Administrativo, Câmara de Itanhaém`, template: `%s · ${SITE.nome}` },
  description: SITE.descricao,
  applicationName: SITE.nome,
  manifest: "/manifest.webmanifest",
  icons: { icon: "/icon.svg" },
};

export const viewport: Viewport = { themeColor: "#1d4ed8" };

// Aplica o tema salvo antes da pintura para evitar flash.
const SCRIPT_TEMA = `try{var t=localStorage.getItem('tema');if(t==='dark'||(!t&&matchMedia('(prefers-color-scheme: dark)').matches))document.documentElement.classList.add('dark')}catch(e){}`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={geistSans.variable} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: SCRIPT_TEMA }} />
      </head>
      <body className="min-h-screen">
        <a href="#conteudo" className="sr-only focus:not-sr-only focus:absolute focus:z-20 focus:bg-card focus:p-3">
          Pular para o conteúdo
        </a>
        <RegistrarSW />
        <Nav />
        <main id="conteudo" className="mx-auto max-w-4xl px-4 py-6">{children}</main>
      </body>
    </html>
  );
}
