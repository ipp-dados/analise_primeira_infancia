# Validação — `specs/2026-09-28_website_mobile`

Escrita **antes** da implementação. Tamanhos: **390×844** (iPhone 12-15), **360×740** (Android pequeno),
**768×1024** (tablet retrato), **1024×768** (tablet paisagem), mais **1400×900** (desktop, regressão). Motores:
Chromium (canal Chrome), Firefox e WebKit via Playwright, com `is_mobile`/`has_touch` nos tamanhos de celular. Por
`file://` e por `http.server` imitando o Pages. Nada conta como validado só porque o gerador rodou sem erro.

Linha de base (2026-09-28, `staging_main` 928127a, 390 px): 114/114 alvos < 44 px; texto dos gráficos no 10º
percentil ~6 px; legenda cobre 50 % do mapa; tooltip sai da tela; 579 px até o conteúdo.

## Base
- [ ] V0.1 Gerador sem `AVISO`, dentro do orçamento (index ≤ 1 MB, site ≤ 2 MB); 2 execuções com o mesmo md5
- [ ] V0.2 Sem erro de JavaScript nas 7 abas, em todos os tamanhos e motores
- [ ] V0.3 **Desktop inalterado**: capturas a 1400 px das 7 abas iguais às de antes, pixel a pixel (a data do banner é
      mascarada)
- [ ] V0.4 Regras de site estático mantidas (só html/css/js/svg/png/jpg, caminhos relativos minúsculos, hash, sem `fetch`)

## 1. Base
- [ ] V1.1 Sem rolagem horizontal da página em nenhum tamanho e nenhuma aba
- [ ] V1.2 Alvos de toque < 44 px no celular: 0 (abas, pills, select, Taxa|Óbitos, CSV, outliers, `summary`, links)
- [ ] V1.3 Faixa de aviso + banner ≤ 320 px a 390 px
- [ ] V1.4 Fonte base 17 px no celular; contraste AA mantido (tabela V4 da `website_refactor`)

## 2. Navegação
- [ ] V2.1 A aba ativa fica inteira visível na barra após clicar, após abrir um link com hash e após voltar/avançar
- [ ] V2.2 Esmaecimento só do lado em que há mais abas (início: só à direita; fim: só à esquerda)
- [ ] V2.3 "Nesta seção ▾" mostra a subseção ativa enquanto rola; abre, leva à subseção ao tocar num link e fecha;
      fecha ao tocar fora, com Esc e ao trocar de aba; `aria-expanded` correto
- [ ] V2.4 Linha de progresso: 0 % no topo do painel e 100 % no fim, igual ao cálculo do desktop
- [ ] V2.5 Altura fixa total (abas + faixa + progresso) ≤ 100 px

## 3. Gráficos
- [ ] V3.1 Texto dos SVG de gráfico renderizado ≥ 11 px (10º percentil) a 390 e 360 px
- [ ] V3.2 Nenhum rótulo sobreposto (eixo x, rótulo final, barras): verificação por caixas delimitadoras + capturas
- [ ] V3.3 Girar a tela (390×844 → 844×390) redesenha sem erro e sem perder a pill, o modo ou a tabela aberta
- [ ] V3.4 Pill/aba/Taxa|Óbitos/Painéis|Linhas trocados para um painel antes oculto: o gráfico aparece com a largura
      certa (nenhum SVG com largura 0 ou viewBox de 680 no celular)
- [ ] V3.5 Pequenos múltiplos em 1 coluna a 390 px e 2 colunas a 600 px
- [ ] V3.6 Tooltip de linha por toque: aparece, fica dentro do cartão, fecha ao tocar fora

## 4. Pills
- [ ] V4.1 Cartões com ≥ 6 opções mostram o select no celular e as pills no tablet e no desktop; com ≤ 5, pills sempre
- [ ] V4.2 Escolher no select troca painel e texto (a mesma auditoria da `website_bugfix`: 45 cartões, 0 falhas)
- [ ] V4.3 Taxa|Óbitos preserva a opção escolhida no select; select e pills ficam sincronizados ao mudar de tamanho

## 5. Mapas
- [ ] V5.1 Legenda abaixo do mapa no celular (sobreposição 0 %); sobre o mapa no tablet e no desktop
- [ ] V5.2 Tooltip por toque em bairro, AP, RP, RA e CAP: dentro do cartão e da tela; tocar fora fecha
- [ ] V5.3 Botões CSV/outliers não se sobrepõem ao título (caixas delimitadoras) em nenhum cartão
- [ ] V5.4 Escala e rosa dos ventos com texto ≥ 10 px renderizado

## 6. Demais componentes
- [ ] V6.1 Tabelas largas rolam dentro do cartão com a primeira coluna fixa
- [ ] V6.2 Visão geral, callouts, Conclusões, rodapé e 404 sem estouro e com alvos ≥ 44 px

## 7. Aparelho real (usuário)
- [ ] V7.1 iPhone (Safari) e Android (Chrome): abrir o link publicado, trocar de aba pela barra, abrir "Nesta
      seção", usar um select de opções, alternar Taxa|Óbitos, tocar num mapa, baixar um CSV, girar a tela
- [ ] V7.2 Rolagem fluida (sem travadas perceptíveis) na aba Prioridade, a mais longa
