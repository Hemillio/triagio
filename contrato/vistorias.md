
# Contrato do módulo de vistorias — Triagio

Este contrato organiza a implementação das HU-03 e HU-04 sem mudar o que está no `REQUISITOS.md`. É uma proposta técnica do grupo, não uma transcrição de exigências específicas dos capítulos 7 e 8.

## Dependências acordadas entre os módulos

- Hemillio mantém `app/extensions.py`, que expõe `db` (`Flask-SQLAlchemy`), e uma fábrica `create_app(test_config=None)` em `app/__init__.py`.
- A fábrica registra o Blueprint `app.vistorias.bp` e importa os modelos antes de criar/aplicar migrações.
- Kauane mantém `app/clientes/models.py` com `Cliente` e `Veiculo`; `Veiculo.__tablename__ = "veiculos"`, chave primária `id`, campo `ativo` e, ao menos, `placa`, `modelo`, `ano` e `cliente_id`.
- Hemillio mantém `app/agendamentos/models.py` com `Agendamento.__tablename__ = "agendamentos"` e chave primária `id`.
- João importa `Vistoria` e pode consultar `status`, `veiculo_id`, `iniciada_em`, `finalizada_em`, `avarias`, `pertences` e `fotos`. João não modifica diretamente as regras de finalização.
- `app/templates/base.html` fornece `{% block content %}` para as telas internas.
- Hemillio acrescenta `Pillow` às dependências do projeto antes da HU-04, para validar os arquivos de imagem.

**Acordo necessário:** se algum arquivo, classe ou campo do projeto-base não seguir esse contrato, a equipe precisa ajustar os planos antes de colar os códigos. Não criar uma segunda classe `Veiculo` ou uma segunda instância `db`.

## Rotas internas propostas

| Método | Rota | Entrada | Sucesso | Recusa |
|---|---|---|---|---|
| GET | `/vistorias/nova/<veiculo_id>` | ID do veículo | 200, confirmação | 404, veículo inexistente/inativo |
| POST | `/vistorias/iniciar/<veiculo_id>` | `agendamento_id` opcional | 303, detalhe | 404/422, vínculo inválido |
| GET | `/vistorias/<id>` | ID da vistoria | 200, checklist | 404, vistoria inexistente |
| POST | `/vistorias/<id>` | `nivel_combustivel`, `observacoes`, `avarias`, `pertences` | 303, dados salvos | 422, validação falhou ou vistoria encerrada |
| POST | `/vistorias/<id>/finalizar` | sem campos adicionais | 303, finalizada | 422, já finalizada |
| POST | `/vistorias/<id>/fotos` | `foto` (`multipart/form-data`) | 303, foto anexada | 422, tamanho, formato, quantidade ou estado |
| GET | `/vistorias/<id>/fotos/<foto_id>` | IDs | 200, imagem | 404, foto não pertence à vistoria |

## Campos e apresentação

- Avarias: uma linha por avaria, no formato `Região | descrição`.
- Pertences: uma descrição por linha; não inventar pertences quando não houver.
- Combustível: `nao_informado`, `vazio`, `1/4`, `1/2`, `3/4`, `cheio` (opções de interface propostas; não constavam do documento de requisitos).
- Estados persistidos, com a mesma grafia do `PROJETO.md`: `EmPreenchimento`, `Finalizada`, `LaudoDisponivel`.
- Instantes persistidos como texto ISO 8601 em UTC, incluindo o deslocamento `+00:00`; a apresentação deve converter para fuso local quando necessário.
- Foto: máximo de quatro por vistoria e tamanho de arquivo **até** 3 × 1024 × 1024 bytes (convenção implementada e registrada; se o grupo escolher MB decimal, alterar o contrato e os testes em conjunto).
- Fotos salvas em `instance/uploads/vistorias/<id>/`, nunca no Git; o banco armazena apenas o caminho relativo e o tamanho em bytes.

## Limites do incremento

- Sem autenticação da área administrativa neste incremento: **somente ambiente local, dados e fotos fictícios; nunca publicar essa versão com dados reais**. A autenticação e autorização devem ser definidas pelo grupo antes de expor o sistema na internet.
- Este módulo não gera token nem laudo: isso é responsabilidade do módulo de João.
- Este módulo não cria nem altera Cliente, Veículo ou Agendamento: responsabilidade de Kauane/Hemillio.
