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

## Enciclopédia

A aba **Termina** reúne NPCs, inimigos, mini-chefes, chefes, objetos, locais e dungeons.

```
src/enc.js            NPCs, objetos, locais e dungeons (texto próprio)
tools/enc_src.json    texto de inimigos e chefes extraído dos guias do Hyrule Legends
tools/enc_auto.py     gera src/enc_auto.js a partir de tools/enc_src.json
tools/enc_check.js    valida ids e referências e lista as imagens (node tools/enc_check.js .)
tools/enc_fetch.py    baixa e converte as imagens para public/enc/<id>.webp
```
