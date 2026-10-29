# Contrato — Portal do Cliente e Laudo (Triagio)

## 1. Objetivo

Implementar a HU-06 (acompanhamento externo) e a HU-07 (laudo simplificado), respeitando RN-04 e RN-05 do `REQUISITOS.md`.

Este documento descreve uma decisão de implementação da equipe, não uma exigência adicional da disciplina.

## 2. Dependências

- Fábrica Flask: `app.create_app(test_config=None)`.
- Banco compartilhado: `app.extensions.db`.
- Vistoria: `app.vistorias.models.Vistoria`, tabela `vistorias`.
- Veículo: `Vistoria.veiculo`, com `placa`, `modelo` e `ano`.
- Evidências: `Vistoria.avarias`, `Vistoria.pertences` e `Vistoria.observacoes`.
- Estados: `EmPreenchimento` -> `Finalizada` -> `LaudoDisponivel`.

## 3. Tabelas

### TokenAcesso

- `id` inteiro, PK.
- `vistoria_id` inteiro, FK obrigatória e única para `vistorias.id`.
- `token` texto longo, obrigatório e único.
- `criado_em` texto ISO 8601 UTC.

Nesta primeira versão, uma vistoria tem no máximo um token persistido. O token é gerado com `secrets.token_urlsafe(32)`, não com a placa, ID ou números sequenciais.

### Laudo

- `id` inteiro, PK.
- `vistoria_id` inteiro, FK obrigatória e única para `vistorias.id`.
- `emitido_em` texto ISO 8601 UTC.
- `caminho_arquivo` caminho relativo do PDF em `instance/laudos/`.

## 4. Rotas

| Método | Caminho | Finalidade | Resposta ou erro |
|---|---|---|---|
| GET | `/portal/vistorias/<id>/acesso` | Tela interna com link e ações | 200; ID inexistente: 404 |
| POST | `/portal/vistorias/<id>/token` | Gerar token se ausente; repetição é idempotente | 303; ID inexistente: 404 |
| GET | `/acompanhar/<token>` | Exibir situação via token, sem login administrativo | 200; token inválido: 404 |
| POST | `/portal/vistorias/<id>/laudo` | Gerar o PDF de uma vistoria finalizada | 303; rascunho: 422 |
| GET | `/acompanhar/<token>/laudo.pdf` | Entregar PDF após validação do token | 200; inexistente/indevido: 404 |

A tela `/portal/...` é interna somente por convenção de caminho: o projeto ainda não tem login. Portanto, a aplicação fica restrita ao ambiente de demonstração local.

## 5. Fluxos

1. Atendente cria e preenche a vistoria (módulo Danilo).
2. O atendente gera um token e entrega o link ao cliente.
3. O cliente abre `/acompanhar/<token>` e vê apenas a situação da vistoria; token inválido não exibe dados.
4. Danilo finaliza a vistoria, que passa a `Finalizada`.
5. O atendente gera laudo em PDF; a transição passa a `LaudoDisponivel`.
6. Ao atualizar o mesmo link, o cliente vê a opção de visualizar o PDF.
7. Pedidos repetidos de token/laudo não produzem registros duplicados.

## 6. Dados contidos no PDF

- identificação técnica da vistoria e do veículo;
- data/hora de início e finalização, explicitamente em UTC;
- combustível, observações, avarias e pertences.

O PDF é salvo em `instance/laudos/`; sua URL de entrega valida o token. Não há busca externa por placa.

## 7. Qualidade e restrições

- Proteger páginas com token e PDF contra cache e indexação por mecanismos de busca.
- Não mostrar nome nem telefone do cliente na tela externa.
- Usar token aleatório de alta entropia, sem derivar da placa.
- Não armazenar PDF nem banco SQLite no Git.
- Gerar laudo apenas após finalização e manter integridade de `Vistoria.status`.
- Verificar token no servidor em cada acesso à página ou ao PDF.
- O módulo não implementa autenticação administrativa, CSRF, revogação de token, expiração, controle de tentativas nem ambiente público. Esses itens precisam de decisão da equipe antes de uso real.

## 8. Critérios de aceitação e verificações

- **CA-06.1:** token único; uma vistoria possui no máximo um token.
- **CA-06.2:** a consulta externa usa o token e não exige login na área administrativa.
- **CA-06.3:** token inválido ou inexistente retorna 404 sem detalhes.
- **CA-06.4:** apresenta estado e, quando disponível, caminho para o PDF.
- **CA-07.1:** rascunho não gera laudo.
- **CA-07.2:** PDF contém dados de vistoria, veículo, avarias e observações.
- **CA-07.3:** PDF é entregue como application/pdf e pode ser impresso/salvo.
- **CA-07.4:** laudo pertence a uma única vistoria.

## 9. Limitações para uma próxima iteração

- Falta autenticação e autorização na área interna; URL interna não equivale a controle de acesso.
- Falta proteção CSRF de formulários POST.
- O token é um segredo na URL, pode aparecer em logs e no histórico do navegador; implementar gestão de expiração/revogação e reduzir exposição antes de operar com dados reais.
- A entrega de arquivos fotográficos ainda depende do módulo de Danilo; não reutilizar uma rota de fotos pública por ID para expor evidências ao cliente.
- A infraestrutura de hospedagem e política de backup não fazem parte desta proposta local.

## 10. Histórico

- 28/10/2026 — versão inicial do contrato para HU-06 e HU-07.
