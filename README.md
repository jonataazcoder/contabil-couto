# Contábil Couto — site

Site one-page da **Contábil Couto – Contabilidade & Assessoria**, R. Cel. João Leme, 559 – Centro, Bragança Paulista/SP.

- `public/` — site publicado (estático, servido pela Vercel)
- `vercel.json` — cache, cabeçalhos de segurança e URLs limpas
- `src/` — fontes: HTML/CSS/JS, emblema vetorizado e o script de build

## Rebuild
```bash
cd src
npm i csso-cli terser playwright   # e: pip install pillow
python3 build.py https://SEU-DOMINIO   # gera src/dist
```
Depois copie `src/dist/*` para `public/` (e `vercel.json` para a raiz).
