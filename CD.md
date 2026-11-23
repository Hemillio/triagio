# Entrega contínua para a demonstração local

## Situação atual

- A CI já existe em .github/workflows/testes.yml: executa python -m pytest -q em Pull Requests para main e em pushes para main.
- A entrega contínua será feita pelo GitHub Actions, usando runner hospedado pelo GitHub para gerar um pacote do código.
- Para a demonstração acadêmica, Hemillio baixará o pacote e iniciará o Triagio no computador principal. Essa inicialização local é manual; portanto, esta etapa automatiza a entrega do pacote, não o deploy automático no PC.
- Não é necessário escolher Render para este formato de demonstração.

## Responsabilidades

### João Mateus

1. Criar o workflow de entrega, condicionado à conclusão bem-sucedida da CI na main.
2. Gerar um pacote versionado pelo hash do commit e disponibilizá-lo como artefato do GitHub Actions.
3. Excluir do pacote .env, banco local, conteúdo de instance/, fotos, PDFs e ambientes virtuais.
4. Documentar como baixar e iniciar o pacote localmente, e abrir PR para revisão do grupo.

### Hemillio

1. Confirmar com o professor que artefato entregue automaticamente e execução manual local atendem ao requisito de CD.
2. Informar o sistema operacional do computador principal e preparar nele a versão de Python e as dependências do projeto.
3. Após o merge e a geração do artefato, baixar o pacote, iniciá-lo localmente e ensaiar a demonstração usando dados fictícios.

## Fluxo de entrega

1. Uma mudança é aberta em Pull Request; a CI executa os testes em runner hospedado pelo GitHub.
2. O grupo revisa e aprova o Pull Request, que então é integrado à main.
3. Após a CI do push à main terminar com sucesso, o workflow de CD empacota exatamente aquele commit e publica o artefato.
4. Hemillio baixa o artefato e inicia a demonstração no computador local.

As instruções de preparação e inicialização estão em [GUIA_CD_LOCAL.md](GUIA_CD_LOCAL.md).

## Segurança e limites

- O pacote não deve conter chaves, arquivos locais, dados reais ou arquivos ignorados pelo Git.
- A demonstração fica restrita ao computador local e usa dados fictícios. Não se deve publicar o servidor de desenvolvimento na internet.
- O Triagio ainda não exige login na área interna e não tem proteção CSRF nos formulários.
- O repositório é público. O GitHub recomenda evitar runners próprios em repositórios públicos, pois código não confiável enviado em Pull Requests pode comprometer a máquina do runner. Por isso, o workflow usa runner hospedado pelo GitHub e não instala runner no PC de Hemillio.

## Cadência e revisão

A meta do grupo é abrir dois Pull Requests pequenos e revisáveis por dia até **26/11/2026 às 15h**. Cada PR deve tratar uma mudança coesa, passar pela CI e receber revisão de outra pessoa, conforme CONTRIBUTING.md. A cadência não justifica dividir artificialmente uma mudança; se uma dependência ou revisão impedir o próximo passo, registrar o bloqueio no grupo.

## Referências

- [Uso seguro do GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use).
- [Entender o GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions).
