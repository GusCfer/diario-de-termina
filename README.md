# Diário de Termina

Checklist de 100% para **The Legend of Zelda: Majora's Mask** (versão N64): as 24 máscaras na ordem recomendada, os 52 pedaços de coração, itens, carteiras, frascos e canções, cada um com passo a passo.

Site: https://diario-de-termina.web.app

## Recursos

- Página de detalhe para cada máscara e item, com screenshot, requisitos e passo a passo.
- Login com Google (Firebase Auth) e progresso salvo por usuário no Firestore, sincronizado entre aparelhos.
- Sem login, o progresso fica salvo no próprio navegador.
- PWA: instalável na tela inicial e funciona offline.

## Estrutura

```
src/template.html   página (HTML, CSS e lógica da checklist)
src/data.js         máscaras e itens com passo a passo
src/hearts.js       os 52 pedaços de coração
src/imgs2.json      imagens embutidas (base64)
src/auth.html       login com Google e sincronização com o Firestore
build.py            monta public/index.html
public/             site publicado (index.html, sw.js, manifest, ícones)
firestore.rules     cada usuário só acessa o próprio documento users/{uid}
```

## Desenvolvimento

```bash
python3 build.py                                  # gera public/index.html
python3 -m http.server 5000 -d public             # testa em http://localhost:5000
npx firebase-tools deploy --only hosting,firestore:rules
```

## Créditos

Imagens das máscaras, frascos e canções e informações de apoio: [Hyrule Legends](https://zelda.com.br/mm). Ícones de itens do inventário: [Zelda Wiki](https://zeldawiki.wiki). Lista de pedaços de coração baseada no guia do [Thonky](https://www.thonky.com/zelda-majoras-mask/pieces-of-heart). Ícone do relógio de Clock Town: arte de Otaku Crafts.

Projeto de fã, sem fins lucrativos. The Legend of Zelda e Majora's Mask são marcas da Nintendo.
