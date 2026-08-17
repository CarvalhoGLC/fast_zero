Ferramentas de desenvolvimento são bastante pessoais. Selecionei 3 que representam bem o que esperamos de um ambiente de desenvolvimento:

Ruff: Um linter e formatador bem poderoso e rápido
Pytest: Para escrevermos os testes
Taskipy: Para não termos que lembrar todos os comandos da aplicação

====================================================================================================

Durante a análise estática do código, queremos buscar por coisas específicas. No Ruff, precisamos dizer exatamente o que ele deve analisar.

I (Isort): ordenação de imports em ordem alfabética
F (Pyflakes): procura por alguns erros em relação a boas práticas de código
E (pycodestyle): erros de estilo de código
W (pycodestyle): avisos sobre estilo de código
PL (Pylint): "erros" em relação a boas práticas de código
PT (flake8-pytest): boas práticas do Pytest