# Contrato do módulo de agendamentos — Triagio

Este arquivo detalha a implementação da HU-02 e os critérios CA-02.1 a CA-02.4. É uma proposta técnica, não um enunciado novo da disciplina.

## Dependências

- `app/extensions.py` exporta a instância compartilhada `db`.
- `app/clientes/models.py` exporta `Veiculo` (`__tablename__ = 'veiculos'`, com `id`, `placa`, `modelo`, `ano`, `ativo`).
- `app/agendamentos/models.py` exporta `Agendamento` (`__tablename__ = 'agendamentos'`, com `id`, `veiculo_id`, `data_hora`, `status`).
- `app/templates/base.html` define `{% block content %}`.
- Danilo pode ler `Agendamento.id` e `Agendamento.veiculo_id` para criar uma vistoria ligada ao agendamento.

## Capacidade e conflito — decisão a validar

Interpretação inicial: há um horário de início de recepção disponível para apenas um veículo, sem controle de duração. Dois registros para o mesmo instante UTC são incompatíveis. **A equipe deve confirmar essa hipótese; se houver várias baias/atendentes ou janelas de duração, atualizar requisito, contrato, modelo e testes antes da implementação.**

## Rotas propostas

| Método | Caminho | Entrada | Resposta de sucesso | Erro |
|---|---|---|---|---|
| GET | `/agendamentos` | nenhuma | 200, lista ordenada por data | — |
| GET | `/agendamentos/novo` | nenhuma | 200, formulário | — |
| POST | `/agendamentos/novo` | `veiculo_id`, `data_hora` | 303 para lista | 422, veículo/horário inválido ou em conflito |

## Dados

- `veiculo_id`: inteiro positivo de veículo existente e ativo.
- `data_hora`: campo HTML `datetime-local` em horário de Palmas.
- Persistência: data/hora convertida para UTC, ISO 8601 com `+00:00`.
- `status`: `Agendado` nesta primeira versão (outros estados dependem de requisito futuro).
- Nenhum dado de cliente é duplicado no agendamento; placa/modelo vêm do relacionamento com `Veiculo`.

## Critérios de aceite deste incremento

- CA-02.1: formulário permite escolher veículo existente e horário.
- CA-02.2: agendamento salvo tem vínculo de banco com aquele veículo.
- CA-02.3: a segunda criação para o mesmo instante não é confirmada.
- CA-02.4: a recusa informa ao usuário que o horário está indisponível.

## Limite de operação

Rotas internas sem autenticação nesta implementação inicial: **uso exclusivamente local, com veículos fictícios**. Proteger o acesso e formulários contra CSRF antes de publicar a aplicação na internet.