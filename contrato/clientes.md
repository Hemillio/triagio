# Contrato de cadastro e histórico — Triagio

**Responsável:** Kauane Coimbra Sousa.

**Origem:** HU-01, HU-05, RN-01, RN-02, CA-01.1 a CA-01.4 e CA-05.1 a CA-05.3 do `REQUISITOS.md`.

Este é um contrato técnico **proposto** para implementação e revisão pela equipe; não é uma exigência literal comprovada dos capítulos 7 e 8.

## Modelo compartilhado

- `app/clientes/models.py` exporta `Cliente` (`__tablename__ = "clientes"`) e `Veiculo` (`__tablename__ = "veiculos"`).
- `Cliente`: `id`, `nome`, `telefone` (opcional), `ativo`.
- `Veiculo`: `id`, `cliente_id`, `placa`, `modelo`, `ano`, `ativo`.
- `Veiculo.cliente` associa cada veículo a exatamente um cliente; `Cliente.veiculos` reúne seus veículos.
- `Veiculo.placa` é única no banco. O formulário grava placas sem espaços/hífens e em maiúsculas, para evitar duplicatas por variação de digitação.
- Cadastro desativado **não é apagado** quando guarda histórico; a desativação está modelada, mas sua interface fica fora deste incremento.
- `Veiculo.ativo` fica disponível para os módulos de Hemillio e Danilo, que devem recusar veículo inativo em novos agendamentos/vistorias.

## Rotas propostas

| Método | Rota | Função | Sucesso | Falha |
|---|---|---|---|---|
| GET | `/clientes/novo` | Formulário de cliente + primeiro veículo | 200 | — |
| POST | `/clientes/novo` | Cadastrar ambos em uma transação | 303 para `/veiculos` | 422 com mensagem e dados mantidos |
| GET | `/veiculos/novo` | Formulário de veículo para cliente existente | 200 | — |
| POST | `/veiculos/novo` | Associar mais um veículo a cliente ativo | 303 para `/veiculos` | 422 por dados ou placa em conflito |
| GET | `/veiculos` | Lista/busca interna (consulta `placa`, opcional) | 200 | Busca inválida mostra mensagem |
| GET | `/veiculos/<id>/historico` | Vistorias anteriores do veículo | 200 | 404 se veículo não existe |

## Validações do incremento

- Nome do cliente obrigatório (até 120 caracteres); telefone opcional (até 30 caracteres).
- Placa obrigatória, letras/números, até 10 caracteres depois de remover hífens e espaços. **O material não definiu formato de placa; o grupo deve avaliar esta validação adicional.**
- Modelo obrigatório (até 120 caracteres); ano inteiro positivo de no máximo quatro dígitos. Os limites são escolhas técnicas iniciais, sujeitos à revisão.
- A mesma placa não gera um segundo veículo, mesmo se vier com letras minúsculas ou hífen. O banco mantém restrição única para proteger inserções simultâneas.

## Integrações

1. **Hemillio:** fornece `app.extensions.db`, Flask-Migrate e a fábrica `create_app(test_config=None)`; `app.agendamentos.models.Agendamento` possui FK `veiculos.id`.
2. **Danilo:** fornece `app.vistorias.models.Vistoria` com FK `veiculos.id`, e rota `vistorias.detalhe` com parâmetro `vistoria_id`. A página de histórico é integrada **após** essa rota.
3. **João:** pode acessar `vistoria.veiculo.placa`, `vistoria.veiculo.modelo`, `vistoria.veiculo.ano` e `vistoria.veiculo.cliente.nome`. O link específico do laudo depende do contrato do portal; por enquanto o histórico abre o registro da vistoria.
4. Não criar outra tabela `veiculos`, instância `db` ou modelo `Cliente` nos demais módulos.

## Restrições para a demonstração

Este incremento não implementa autenticação interna nem proteção CSRF. **Execute somente localmente, com dados e placas fictícios; não exponha a aplicação na internet.** Privacidade, autenticação e permissão por usuário precisam ser resolvidas antes do uso real.
