# CI e CD local para a demonstração

## Escopo e decisão

- A CI existente em .github/workflows/testes.yml executa python -m pytest -q em Pull Requests para main e em pushes para main.
- O GitHub Actions prepara o pacote em runner hospedado pelo GitHub. Não será instalado runner próprio no notebook nem haverá servidor público.
- Após a CI passar em um push para main, um job dependente dos testes prepara o ZIP do mesmo commit, extrai em uma pasta limpa, instala dependências, cria SQLite temporário, executa migrações e valida GET / com o Flask limitado a 127.0.0.1 e debug desligado.
- O Artifact só será publicado se essa validação passar. A retenção planejada é de 7 dias.
- Hemillio baixa o pacote aprovado e inicia a demonstração manualmente no computador principal. O CD automatiza a entrega e a validação do pacote; não mantém o sistema implantado no PC.

## Responsabilidades

### João Mateus — pipeline

1. Manter o job de entrega dependente do job de testes, liberado somente em push para main.
2. Empacotar uma lista permitida de arquivos e identificar o pacote pelo hash do commit validado.
3. Validar estrutura e conteúdo do ZIP, migrações e rota inicial em ambiente limpo, sem dados reais.
4. Publicar o Artifact somente após a validação e manter a retenção curta.
5. Registrar comandos e evidências da execução, manter as ações revisadas/fixadas por SHA e abrir PR para revisão.

### Hemillio — demonstração

1. Conferir a execução no Windows, a versão de Python e as dependências utilizadas.
2. Definir com João os comandos de migração e inicialização que o pipeline validará.
3. Baixar a versão aprovada, extraí-la em pasta limpa e ensaiar no PC principal sem dados reais.
4. Verificar cadastros, agendamentos, fotos e laudos com dados fictícios.
5. Apresentar logs da CI/CD, Artifact e sistema local com debug desligado.

### Verificação funcional

- Kauane verifica clientes, associação de veículos e histórico no pacote extraído.
- Danilo verifica abertura, preenchimento e finalização de vistorias, incluindo fotos fictícias.

## Fluxo

1. PRs para main passam por revisão de outra pessoa e pelos testes da CI.
2. Após aprovação, a mudança é integrada em main.
3. No push integrado, o job de pacote depende dos testes aprovados e usa o mesmo commit.
4. O pacote é montado a partir de arquivos permitidos, extraído em ambiente limpo e validado antes do upload do Artifact.
5. Hemillio baixa o Artifact aprovado e inicia a demonstração local manualmente.

O roteiro para preparar e executar o pacote está em [GUIA_CD_LOCAL.md](GUIA_CD_LOCAL.md).

## Segurança e limites

- Excluir .env, credenciais, tokens, bancos locais, instance/, ambientes virtuais, caches, logs, fotos, PDFs e uploads locais. Incluir apenas código, migrações, dependências e instruções necessárias.
- Usar SQLite e dados fictícios na validação e na demonstração. A chave temporária do runner nunca entra no Artifact.
- Restringir GITHUB_TOKEN ao mínimo necessário (contents: read) e não enviar segredos aos jobs.
- Não expor o servidor de desenvolvimento à internet. O Triagio ainda não exige login na área interna nem protege os formulários contra CSRF.
- O repositório é público. Usar runner hospedado pelo GitHub; não instalar runner próprio no notebook.

## Cronograma e revisão

- **24/11:** configurar gate da CI, pacote sem dados e início da validação.
- **25/11:** testar extração em ambiente limpo, corrigir falhas, revisar PR e ensaiar no PC.
- **26/11 até 15h:** integrar PR revisado, conferir CI, CD, Artifact e demonstração local.

Mantém-se a meta combinada de até dois PRs por dia até **26/11/2026 às 15h**, desde que cada um tenha uma mudança coesa e pronta para revisão. Não criar commits extras nem dividir artificialmente uma mudança só para cumprir quantidade; cada commit deve ter propósito técnico. Cada PR deve explicar o teste e a evidência, conforme CONTRIBUTING.md.

## Referências

- [Uso seguro do GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use).
- [Entender o GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions).
