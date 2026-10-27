#!/usr/bin/env python3
"""Gera os SVGs do README a partir de theme.json e content.json.

Uso: python docs/assets/build.py   (requer Pillow)
"""
import base64
import io
import json
import textwrap
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SHOTS = HERE.parent / "screenshots"
T = json.loads((HERE / "theme.json").read_text(encoding="utf-8"))
C = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
ANIM = T["animations"]
GLOW = T["glow"]
SANS, DISPLAY, MONO = T["fontSans"], T["fontDisplay"], T["fontMono"]


def esc(s):
    return escape(s, quote=True)


def write(name, svg):
    (HERE / name).write_text(svg, encoding="utf-8")


def svg_open(w, h, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>\n"
    )


def grad(id_, x1="0", y1="0", x2="1", y2="0"):
    return (
        f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
        f'<stop offset="0" stop-color="{T["accent"]}"/><stop offset="1" stop-color="{T["accent2"]}"/></linearGradient>'
    )


def radial(id_, color, op):
    return (
        f'<radialGradient id="{id_}"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
        f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'
    )


def mono_w(text, size, spacing=0.0):
    return len(text) * (0.6 * size + spacing)


# ---------- imagens ----------
def webp_uri(img, max_kb=200, width=1280):
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    for q in (80, 74, 68, 62, 56, 50):
        buf = io.BytesIO()
        img.convert("RGB").save(buf, "WEBP", quality=q, method=6)
        if len(buf.getvalue()) <= max_kb * 1024:
            break
    kb = len(buf.getvalue()) / 1024
    print(f"  imagem {img.width}x{img.height} q={q} {kb:.0f} KB")
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(), img.size


def phones_composite():
    """topico.png + simulado.png lado a lado, em um único quadro."""
    W, H, ph = 1280, 820, 760
    canvas = Image.new("RGB", (W, H), T["card"])
    shots = []
    for n in ("topico", "simulado"):
        im = Image.open(SHOTS / f"{n}.png").convert("RGB")
        im = im.resize((round(im.width * ph / im.height), ph), Image.LANCZOS)
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, *im.size), 36, fill=255)
        shots.append((im, mask))
    gap = 110
    total = sum(s[0].width for s in shots) + gap
    x = (W - total) // 2
    for im, mask in shots:
        canvas.paste(im, (x, (H - ph) // 2), mask)
        x += im.width + gap
    return canvas


# ---------- peças ----------
def dots(x, y):
    cols = ["#ff8a7a", "#f5d36a", T["accent"]]
    return "".join(f'<circle cx="{x + i * 16}" cy="{y}" r="4.5" fill="{c}"/>' for i, c in enumerate(cols))


def banner():
    name_words = C["name"].split(" ")
    pill = f'github.com/diegonatalo/{C["repo"]}'.upper()
    pill_w = mono_w(pill, 13, 1.8) + 52
    tag_lines = textwrap.wrap(C["tagline"], 34)[:2]
    chips, x = [], 72
    for s in C["stack"]:
        w = 0.6 * 13 * len(s) + 38
        if x + w > 735:
            break
        chips.append((s, x, w))
        x += w + 10
    src = Image.open(SHOTS / "principal-dark.png").convert("RGB")
    crop = src.crop((384, 0, 1756, 1080)).resize((732, round(1080 * 732 / 1372)), Image.LANCZOS)
    uri, _ = webp_uri(crop, width=732)

    o = svg_open(1200, 470, f'{C["name"]}: {C["tagline"]}')
    o += "<defs>" + grad("g") + radial("ga", T["accent"], 0.26) + radial("gb", T["accent2"], 0.26)
    o += '<clipPath id="card"><rect width="1200" height="470" rx="26"/></clipPath>'
    o += '<clipPath id="frame"><rect x="770" y="58" width="366" height="318" rx="20"/></clipPath>'
    o += '<pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">'
    o += f'<path d="M44 0H0V44" fill="none" stroke="{T["fg"]}" stroke-opacity="0.045"/></pattern>'
    o += "<style>"
    if ANIM:
        o += ".pulse{animation:p 2.4s ease-in-out infinite}@keyframes p{50%{opacity:.35}}"
        o += ".d1{animation:a 14s ease-in-out infinite alternate}.d2{animation:b 16s ease-in-out infinite alternate}"
        o += "@keyframes a{to{transform:translate(60px,30px)}}@keyframes b{to{transform:translate(-60px,-24px)}}"
    o += "</style></defs>\n"
    o += f'<g clip-path="url(#card)"><rect width="1200" height="470" fill="{T["bg"]}"/>'
    if T["grid"]:
        o += '<rect width="1200" height="470" fill="url(#grid)"/>'
    if GLOW:
        o += '<g class="d1"><circle cx="170" cy="40" r="330" fill="url(#ga)"/></g>'
        o += '<g class="d2"><circle cx="1040" cy="420" r="380" fill="url(#gb)"/></g>'
    o += "</g>\n"
    o += f'<rect x="72" y="62" width="{pill_w:.0f}" height="36" rx="18" fill="{T["accent"]}" fill-opacity="0.10" stroke="{T["accent"]}" stroke-opacity="0.38"/>'
    o += f'<circle class="pulse" cx="92" cy="80" r="4" fill="{T["accent"]}"/>'
    o += f'<text x="108" y="85" font-family="{MONO}" font-size="13" letter-spacing="1.8" fill="{T["accent"]}">{esc(pill)}</text>\n'
    first, last = " ".join(name_words[:-1]), name_words[-1]
    if first:
        o += (
            f'<text x="72" y="196" font-family="{DISPLAY}" font-size="98" font-weight="800" letter-spacing="-3" fill="{T["fg"]}">'
            f'{esc(first)} <tspan fill="url(#g)">{esc(last)}</tspan></text>\n'
        )
    else:
        o += f'<text x="72" y="196" font-family="{DISPLAY}" font-size="98" font-weight="800" letter-spacing="-3" fill="{T["fg"]}">{esc(last)}</text>\n'
    for i, ln in enumerate(tag_lines):
        o += f'<text x="72" y="{296 + 28 * i}" font-family="{SANS}" font-size="20" fill="{T["muted"]}">{esc(ln)}</text>\n'
    for i, (s, cx, w) in enumerate(chips):
        col = T["accent"] if i % 2 == 0 else T["accent2"]
        o += f'<rect x="{cx:.0f}" y="362" width="{w:.0f}" height="32" rx="16" fill="{T["bg"]}" stroke="{T["borderStrong"]}"/>'
        o += f'<circle cx="{cx + 16:.0f}" cy="378" r="3.5" fill="{col}"/>'
        o += f'<text x="{cx + 28:.0f}" y="383" font-family="{MONO}" font-size="13" fill="{T["fg"]}">{esc(s)}</text>\n'
    o += f'<rect x="770" y="58" width="366" height="318" rx="20" fill="{T["card"]}"/>'
    o += dots(792, 73)
    o += f'<text x="953" y="77" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{T["subtle"]}">aprovaita.vercel.app</text>'
    o += f'<g clip-path="url(#frame)"><image href="{uri}" x="770" y="88" width="366" height="288" preserveAspectRatio="xMidYMin slice"/></g>'
    o += f'<rect x="770.5" y="58.5" width="365" height="317" rx="20" fill="none" stroke="{T["borderStrong"]}"/>'
    o += f'<line x1="770" y1="88" x2="1136" y2="88" stroke="{T["borderStrong"]}"/>'
    o += f'<rect x="0.5" y="0.5" width="1199" height="469" rx="26" fill="none" stroke="{T["borderStrong"]}"/>'
    o += "</svg>\n"
    write("banner.svg", o)


def button(name, label, primary):
    text = f"{label} ↗"
    w = round(len(text) * 9.6 + 56)
    o = svg_open(w, 52, text)
    o += f"<defs>{grad('g')}</defs>"
    if primary:
        o += f'<rect width="{w}" height="52" rx="26" fill="url(#g)"/>'
        fill = T["onAccent"]
    else:
        o += f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="50.5" rx="25.5" fill="{T["card"]}" stroke="{T["borderStrong"]}" stroke-width="1.5"/>'
        fill = T["fg"]
    o += f'<text x="{w / 2}" y="32" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{fill}">{esc(text)}</text></svg>\n'
    write(name, o)
    return w


def header(name, num, label, title):
    pill = f"{num:02d} · {label}"
    pw = len(pill) * 9.4 + 34
    o = svg_open(1000, 124, f"{pill}: {title}")
    o += "<defs>" + grad("g") + radial("a", T["accent2"], 0.16) + radial("b", T["accent"], 0.14)
    o += '<clipPath id="c"><rect width="1000" height="124" rx="22"/></clipPath></defs>'
    o += f'<g clip-path="url(#c)"><rect width="1000" height="124" fill="{T["card"]}"/>'
    if GLOW:
        o += '<circle cx="960" cy="0" r="200" fill="url(#a)"/><circle cx="40" cy="124" r="190" fill="url(#b)"/>'
    o += "</g>"
    o += f'<rect x="0.5" y="0.5" width="999" height="123" rx="22" fill="none" stroke="{T["borderStrong"]}"/>'
    o += f'<rect x="40" y="26" width="{pw:.0f}" height="28" rx="14" fill="{T["accent"]}" fill-opacity="0.10" stroke="{T["accent"]}" stroke-opacity="0.38"/>'
    o += f'<text x="{40 + pw / 2:.0f}" y="45" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="1.6" fill="{T["accent"]}">{esc(pill)}</text>'
    o += f'<text x="40" y="94" font-family="{DISPLAY}" font-size="36" font-weight="800" letter-spacing="-0.8" fill="{T["fg"]}">{esc(title)}</text>'
    o += '<rect x="40" y="106" width="64" height="3" rx="1.5" fill="url(#g)"/></svg>\n'
    write(name, o)


def feature(name, idx, title, desc):
    lines = textwrap.wrap(desc, 54)[:5]
    o = svg_open(490, 290, f"Funcionalidade {idx:02d}: {title}. {desc}")
    o += "<defs>" + grad("g") + radial("a", T["accent"], 0.20)
    o += '<clipPath id="c"><rect width="490" height="290" rx="22"/></clipPath></defs>'
    o += f'<g clip-path="url(#c)"><rect width="490" height="290" fill="{T["card"]}"/>'
    if GLOW:
        o += '<circle cx="480" cy="0" r="170" fill="url(#a)"/>'
    o += '<rect width="490" height="4" fill="url(#g)"/></g>'
    o += f'<rect x="0.5" y="0.5" width="489" height="289" rx="22" fill="none" stroke="{T["borderStrong"]}"/>'
    o += f'<text x="34" y="44" font-family="{MONO}" font-size="12" letter-spacing="1.6" fill="{T["subtle"]}">FUNCIONALIDADE {idx:02d}</text>'
    o += f'<text x="34" y="82" font-family="{DISPLAY}" font-size="28" font-weight="700" fill="{T["fg"]}">{esc(title)}</text>'
    for i, ln in enumerate(lines):
        o += f'<text x="34" y="{116 + 22 * i}" font-family="{SANS}" font-size="14.5" fill="{T["muted"]}">{esc(ln)}</text>'
    o += "</svg>\n"
    write(name, o)


def stack(name):
    y, cur, placed = 26, 0, []
    avail = 1000 - 52
    for i, s in enumerate(C["stack"]):
        w = 0.6 * 13 * len(s) + 38
        if cur + w > avail and cur:
            y += 40
            cur = 0
        placed.append((s, 26 + cur, y, w, i))
        cur += w + 10
    h = y + 32 + 26
    o = svg_open(1000, h, "Stack: " + ", ".join(C["stack"]))
    o += f'<rect x="0.5" y="0.5" width="999" height="{h - 1}" rx="20" fill="{T["card"]}" stroke="{T["borderStrong"]}"/>'
    for s, cx, cy, w, i in placed:
        col = T["accent"] if i % 2 == 0 else T["accent2"]
        o += f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="32" rx="16" fill="{T["bg"]}" stroke="{T["borderStrong"]}"/>'
        o += f'<circle cx="{cx + 16:.0f}" cy="{cy + 16}" r="3.5" fill="{col}"/>'
        o += f'<text x="{cx + 28:.0f}" y="{cy + 21}" font-family="{MONO}" font-size="13" fill="{T["fg"]}">{esc(s)}</text>'
    o += "</svg>\n"
    write(name, o)


def shot(name, img, route, alt):
    uri, (iw, ih) = webp_uri(img)
    ih_s = round(1000 * ih / iw)
    h = 28 + ih_s + 20
    o = svg_open(1000, h, alt)
    o += "<defs>" + radial("a", T["accent"], 0.22)
    o += f'<clipPath id="c"><rect x="0" y="0" width="1000" height="{28 + ih_s}" rx="16"/></clipPath></defs>'
    if GLOW:
        o += f'<ellipse cx="500" cy="{h - 8}" rx="420" ry="40" fill="url(#a)"/>'
    o += f'<g clip-path="url(#c)"><rect width="1000" height="{28 + ih_s}" fill="{T["card"]}"/>'
    o += f'<image href="{uri}" x="0" y="28" width="1000" height="{ih_s}"/></g>'
    o += dots(20, 14)
    o += f'<text x="500" y="18" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{T["subtle"]}">{esc(route)}</text>'
    o += f'<rect x="0.5" y="0.5" width="999" height="{28 + ih_s - 1}" rx="16" fill="none" stroke="{T["borderStrong"]}"/>'
    o += f'<line x1="0" y1="28" x2="1000" y2="28" stroke="{T["borderStrong"]}"/></svg>\n'
    write(name, o)


def footer():
    o = svg_open(1000, 90, f'© {C["year"]} {C["author"]}')
    o += "<defs>" + grad("g") + "</defs>"
    o += '<rect x="0" y="13" width="1000" height="2" fill="url(#g)" fill-opacity="0.7"/>'
    o += f'<text x="500" y="52" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{T["subtle"]}">© {C["year"]} {C["author"].upper()}</text>'
    o += "</svg>\n"
    write("footer.svg", o)


def main():
    banner()
    button("btn-demo.svg", "Demonstração", True)
    button("btn-code.svg", "Código", False)
    for key, label in (("portfolio", "Portfólio"), ("linkedin", "LinkedIn"), ("github", "GitHub")):
        button(f"btn-{key}.svg", label, False)
    heads = [
        ("sobre", "SOBRE", "Sobre o projeto"),
        ("demo", "DEMO", "Telas"),
        ("funcionalidades", "FUNCIONALIDADES", "O que dá para fazer"),
        ("stack", "STACK", "Stack"),
        ("rodar", "COMO RODAR", "Rodando localmente"),
        ("estrutura", "ESTRUTURA", "Estrutura"),
        ("mais", "MAIS", "Mais informações"),
        ("autor", "AUTOR", "Autor"),
    ]
    for i, (k, lab, tit) in enumerate(heads, 1):
        header(f"h-{k}.svg", i, lab, tit)
    for i, (t, d) in enumerate(C["features"], 1):
        feature(f"f-{i:02d}.svg", i, t, d)
    stack("stack.svg")
    shot("shot-principal-dark.svg", Image.open(SHOTS / "principal-dark.png"), "/", "Tela inicial do Aprova Ita: contagem regressiva para a prova, progresso geral e áreas de estudo")
    shot("shot-principal-light.svg", Image.open(SHOTS / "principal-light.png"), "/", "Tela inicial do Aprova Ita no tema claro")
    shot("shot-estudar.svg", Image.open(SHOTS / "estudar.png"), "/conteudo", "Lista de tópicos de Língua Portuguesa com o status de cada um")
    shot("shot-progresso.svg", Image.open(SHOTS / "progresso.png"), "/progresso", "Painel de progresso com próximo passo sugerido e desempenho por área")
    shot("shot-celular.svg", phones_composite(), "/conteudo · /simulado", "Página de um tópico e simulado no celular")
    footer()
    print("ok")


if __name__ == "__main__":
    main()
