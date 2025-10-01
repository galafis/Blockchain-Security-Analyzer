# Diretrizes de Contribuição

Bem-vindo ao Blockchain Security Analyzer! Agradecemos seu interesse em contribuir para este projeto. Para garantir um processo de colaboração suave e eficaz, por favor, siga estas diretrizes.

## Como Contribuir

Existem várias maneiras de contribuir para este projeto:

*   **Reportar Bugs**: Se você encontrar um bug, por favor, abra uma issue detalhada.
*   **Sugerir Novas Funcionalidades**: Ideias para novas funcionalidades são sempre bem-vindas. Abra uma issue para discutir suas sugestões.
*   **Submeter Pull Requests**: Se você deseja contribuir com código, siga as diretrizes abaixo para submeter um Pull Request (PR).

## Reportando Bugs

Ao reportar um bug, por favor, inclua o máximo de detalhes possível:

1.  **Descrição Clara**: Descreva o bug de forma clara e concisa.
2.  **Passos para Reproduzir**: Forneça os passos exatos para reproduzir o bug.
3.  **Comportamento Esperado**: Descreva o que você esperava que acontecesse.
4.  **Comportamento Atual**: Descreva o que realmente aconteceu.
5.  **Capturas de Tela/Logs**: Se aplicável, inclua capturas de tela ou logs de erro.
6.  **Ambiente**: Informe seu sistema operacional, versão do Python, etc.

## Sugerindo Novas Funcionalidades

Ao sugerir uma nova funcionalidade, por favor, inclua:

1.  **Descrição da Funcionalidade**: Explique a funcionalidade e qual problema ela resolve.
2.  **Casos de Uso**: Descreva como a funcionalidade seria usada.
3.  **Benefícios**: Explique os benefícios que a funcionalidade traria ao projeto.

## Submetendo Pull Requests

Para submeter um Pull Request, siga estes passos:

1.  **Fork o Repositório**: Faça um fork do repositório para sua conta GitHub.
2.  **Clone o Fork**: Clone seu fork para sua máquina local.
    ```bash
    git clone https://github.com/SEU_USUARIO/Blockchain-Security-Analyzer.git
    cd Blockchain-Security-Analyzer
    ```
3.  **Crie uma Nova Branch**: Crie uma branch para sua funcionalidade ou correção de bug.
    ```bash
    git checkout -b feature/sua-funcionalidade
    # ou
    git checkout -b bugfix/correcao-de-bug
    ```
4.  **Faça Suas Alterações**: Implemente suas alterações, garantindo que o código siga os padrões de estilo do projeto.
5.  **Escreva Testes**: Adicione testes unitários para suas alterações, se aplicável, e certifique-se de que todos os testes existentes passem.
    ```bash
    python3 -m unittest tests/test_app.py
    ```
6.  **Commit Suas Alterações**: Escreva mensagens de commit claras e descritivas.
    ```bash
    git commit -m "feat: Adiciona nova funcionalidade X"
    # ou
    git commit -m "fix: Corrige bug Y"
    ```
7.  **Envie para o GitHub**: Envie suas alterações para o seu fork no GitHub.
    ```bash
    git push origin feature/sua-funcionalidade
    ```
8.  **Abra um Pull Request**: Vá para o repositório original no GitHub e abra um Pull Request da sua branch para a branch `main`.

## Padrões de Código

*   **Python**: Siga as diretrizes do [PEP 8](https://www.python.org/dev/peps/pep-0008/).
*   **Solidity**: Siga as diretrizes de estilo do [Solidity](https://docs.soliditylang.org/en/latest/style-guide.html).

## Revisão de Código

Todos os Pull Requests serão revisados pela equipe do projeto. Esteja preparado para fazer alterações com base no feedback recebido. A revisão de código é um processo colaborativo e visa melhorar a qualidade do código e do projeto como um todo.

## Código de Conduta

Ao participar deste projeto, você concorda em seguir nosso [Código de Conduta](CODE_OF_CONDUCT.md).
