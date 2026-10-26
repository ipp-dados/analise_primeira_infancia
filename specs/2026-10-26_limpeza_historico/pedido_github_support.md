# Pedido ao GitHub Support — remover cache dos commits antigos (pendente)

Tarefa B6b de `tasks.md`. Depois da reescrita do histórico (2026-10-26), os commits antigos com dado sensível
continuam acessíveis no github.com por hash completo (conferido em 2026-10-26: HTTP 200). Só o GitHub Support remove
essas visões em cache e coleta os objetos órfãos.

## Como pedir

1. Abrir https://support.github.com/contact (logado como `leoaucar`).
2. Escolher a conta/organização **`ipp-dados`** (se não aparecer, a conta pessoal, citando o repositório na mensagem).
3. Tema: o que mais se aproximar de **"Remove sensitive data"** / remoção de commits ou visões em cache.
4. Assunto: `Remove cached views of rewritten commits — ipp-dados/analise_primeira_infancia`
5. Mensagem (em inglês costuma ter resposta mais rápida; colar como está):

```
Hello,

We removed sensitive data from the public repository ipp-dados/analise_primeira_infancia
by rewriting its history with git filter-repo and force-pushing all branches and tags
on 2026-10-26. The data was (a) per-neighbourhood counts below 20 from a social-assistance
registry (CadÚnico), which our data-protection rule forbids publishing, and (b) external
review documents that include a person's name.

The old commits are still reachable by SHA on github.com. Please remove the cached views
and garbage-collect the dereferenced objects for:

- cdfacd21fef92bcdb54987d07df1750c7c685423  (contained the counts below 20)
- 101e6bf7b6e2f574a80852d1216590b6982f5791  (contained the review documents)

Details:
- First changed commit reported by git filter-repo (old -> new):
  6bdb624d01742ac9411ca0da8ba0d41fca3f0bb8 -> cb555a70c8a42229fca87a7fe8ba256563f79611
- Affected pull requests: none (the repository has no pull requests)
- Forks: none
- Git LFS: not used
- All branches (staging_main, demo, main) and tags (rodada/*) were force-pushed.

Thank you.
```

## Depois

- O GitHub responde em alguns dias; pode pedir confirmação de que todas as branches e tags foram reescritas (foram).
- Conferir que os dois links abaixo passaram a dar **404**:
  - https://github.com/ipp-dados/analise_primeira_infancia/commit/cdfacd21fef92bcdb54987d07df1750c7c685423
  - https://github.com/ipp-dados/analise_primeira_infancia/commit/101e6bf7b6e2f574a80852d1216590b6982f5791
- Até lá: ninguém dá push de clone antigo, e o backup (`../backup_analise_primeira_infancia_2026-10-26/`) fica
  guardado. Com os 404, apagar o backup (B8) e marcar B6b em `tasks.md`.
