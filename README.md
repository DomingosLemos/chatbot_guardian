# chatbot_guardian

## Descrição

Este chatbot é uma tentativa de criar uma realidade à imagem do projeto que está a decorrer no curso ***BotCamp*** na [LetsBot](https://www.letsbot.com.br/). 

O desafio lançado no curso ***HelloBot*** (curso inicial de uma semana) era o de criar um chatbot, usando o Dialogflow, com criação de intents que respondessem a um conjunto de questões mais frequentes lançadas por milhares de pais em relação a uma ferramenta de gestão de entradas e saídas dos filhos das escolas. 

A ferramenta pertence à [School Guardian](https://www.schoolguardian.app/) e esta empresa em parceria com a LetsBot entregou um caso real para ser resolvido no ambito do curso. Desta forma, todos os matriculados vão ter a possibilidade de resolver um caso real utilizando todas as técnicas aprendidas ao longo de várias semanas.

## Objetivo

O desafio a que me propus não era trazer para aqui o resultado do bot criado em Dialogflow, mas replicar os conhecimentos utilizando programação em Python.

## Percurso de aprendizagem

Segue uma breve descrição dos passos dados na construção do chatbot realizado no curso inicial ***HelloBot***

1. A ***School Guadian*** entregou um conjunto de top questões recebidas pelos encarregados de educação onde tivemos numa primeira fase encaixar em intenções (intents). 

2. Depois tivemos que enriquecer cada intenção com perguntas similares e respostas alternativas, para que tivessemos uma fonte de dados para treinar um modelo de Processamento de Linguagem Natural (NLP). Como resultado, tivemos um ficheiro de excel com a seguinte estrutura: 

<img width="523" alt="Intents_result" src="https://user-images.githubusercontent.com/76813386/156903609-ae23e7f7-7c96-4c12-bfec-d93f2c5762ba.PNG">

3. Terminado a primeira fase de **Behavior/Interaction** partimos para a fase de **Architect/Build**, utilizando o Dialogflow como ferramenta, adicionando todas as intents, com as potenciais questões dos clientes e respectivas respostas. Nesta fase o nosso conjunto de dados foi treinado com Inteligencia Artificial para que fosse possível identificar a intenção da questão do cliente, mesmo com outras construções de sintaxe.

<img width="431" alt="Dialogflow" src="https://user-images.githubusercontent.com/76813386/156903831-deff43b7-203a-430f-91ab-d05970280a51.PNG">

4. A fase seguinte foi a criação de um site integrado com o nosso bot e que estivesse na internet para acesso de todos. Para a realização desta etapa utilizamos o [Google Sites](https://sites.google.com/) como ferramenta. Após publicação, bastou partilhar com os colegas para que podessem testar.

O resultado foi este: [School Guardian Bot](https://sites.google.com/view/schoolguardion-dalemos/p%C3%A1gina-inicial)

5. A última fase do ***HelloBot*** foi de **Training**, onde todos fomos convidados a quebrar o bot dos colegas e assim poder fazer o **Curate** dos nossos bots. Confesso que esta foi uma das partes bem divertidas do curso.

6. Dando continuidade aos conteúdos do BotCamp, foi introduzido um novo mecanismo, chamado de webhook, onde é permitido uma interação mais dinâmica, que não limita às resposta previamente programadas. Isto é feito recorrendo a chamadas de APIs externas ao bot. Até aqui tudo pacífico, não fosse a necessidade de poder haver chamadas que necessitam de parâmetros que têm que ser recolhidos das frases dos utilizadores. Segue um pequeno exemplo que ajuda a perceber melhor:

<img width="261" alt="webhook_bot" src="https://user-images.githubusercontent.com/76813386/160299321-446e8b44-63e8-4ab2-9c71-43f55453df7b.png">

  No exemplo anterior, podem ver 3 conversas (a seta indica a ordem das entradas). Em todas as conversas a chamada cai na intent "Obter_nome_responsavel" que necessita de identificar o nome do responsável da criança. Neste caso, não podemos prever uma resposta certa, uma vez que depende do nome da criança. Aqui entra a utilização do webhook, ou seja, uma chamada de uma API exterior que irá validar dentro de alguma base de dados da escola a resposta à questão. Para o bot é indiferente ao que é feito dentro da API, apenas lhe interessa o resultado. 
Este webhook está preparado para responder apenas a dois nomes de crianças "João" e "Júlia", a título de demonstração.
Na 1ª conversa, o bot identificou o nome do aluno e a api respondeu qual o responsável correspondente. 
Na 2ª conversa não foi colocado o nome da criança e o bot como identificou a falta desta informação perguntou "Qual o nome da criança?".
Na 3ª conversa, apesar do bot ter identificado o nome da criança, quando fez a chamada, a api não devolveu nada o que originou a resposta de não existir aquela criança. 
A grande diferença desta solução, comparativamente ao Dialogflow é que o processo está preparado para usar diferentes webhook para diferentes Intents e quando pede o nome da criança, o que for respondido é tratado como se do nome se tratasse, terminando essa iteração. 
Mas nem tudo são rosa, pois o bot apenas foi preparado para ir até máximo de um parâmetro. Esta configuração encontra-se no ficheiro "job_intents.json" explicado mais abaixo.

## Estrutura/setup do projecto Python

A aprendizagem anterior foi essencial para o desenho e construção do chatbot. A ideia não foi replicar o conjunto completo de todas as intents identificadas, mas montar uma estrutura que permita fazer algo semelhante.

Quero deixar bem claro que uma parte do código foi extraido da net e não é de minha autoria. Deixo mais abaixo as referências. 
O verdadeiro desafio foi colar as várias peças encontradas na net e montar uma solução identica à da formação, com desenvolvimentos para várias features. 

### Funcionalidades desenvolvidas

O bot está construido numa base de Inteligência Artificial, recorrendo a NLP e Deep Learning.
Segue a lista das features já desenvolvidas:
* Identificação das intents com base nos diálogos conversacionais desenhados
* Chamada a webhook para interações externas. Cada intent pode recorrer a um webhook diferente
* Desambiguação recorrendo a entidades

### Roadmap

Funcionalidades ainda por desenvolver ou melhorar:
* Fluxos conversacionais com IA
* Aceitar lista de parâmetros para as APIs
* Melhorar o design do frontend de ambas as versões

### Setup 

Segue os passos realizados para conseguir executar o projeto no seu computador.

Em primeiro lugar deve ter o motor de Python instalado na sua máquina (https://www.python.org/). <br>
Depois de instalado, recomendo como boa prática criar um environment para o projeto, por forma a ter um ambiente isolado de bibliotecas.
Para isso (supondo que está num ambiente windows), entre numa Command Prompt (digitar cmd após carregar no botão do windows)

Criar um env indicando a pasta que terá o projeto (a path pode ser à sua escolha):
> python -m venv C:\Meu\chatbot<br>
> cd C:\Meu\chatbot<br>

Ativar o environment:
> Scripts\activate.bat<br>

Dentro do environment, no meu caso chamei de chatbot, temos que instalar as seguintes livrarias necessárias para rodar o projecto:
> pip install nltk<br>
> pip install numpy<br>
> pip install keras<br>
> pip install tensorflow<br>
> pip install flask<br>
> pip install spacy<br>

Download do modelo para interpretar a lingua portuguesa:
> python -m spacy download pt_core_news_md<br>


Neste momento temos o ambiente pronto. Apenas uma nota, a versão que eu usei de python é 3.7.9. Também deverá funcionar com versões mais recentes.

### API do webhook

Para criar um webhook para usar no chatbot, recorri ao Heroku (https://www.heroku.com/). Se não conhece, este site permite fazer deploy de web ou a exposição de API de forma gratuita (com limitação até 5 projetos).

Não é o meu propósito explicar os passos necessários para a criação das APIs, uma vez que há muitos videos na web a ensinar. Caso pretenda experimentar, pode usar a minha API criada para este projeto e que se encontra no código fonte.
Se tiver curiosidade pode também ver o código compactado no ficheiro api-py.zip e usar como bem entender. 

### Estrutura do projeto

O projeto está dividido em duas parte, uma de IA para treinar o modelo e outra para executar o chatbot utilizado o modelo pré treinado.

| Ficheiro | Descrição |
| -------- | --------- |
| job_intents.json | O ficheiro com as intents com as perguntas e respostas |
| chatbot.py | Neste ficheiro temos o algoritmo de NLP para treinar e criar o modelo a usar no chatbot |
| words.pkl | ficheiro pickle no qual fica armazenado as palavras do nosso vocabulário |
| classes.pkl | ficheiro pickle com a lista das intents |
| chatbot_model.h5 | temos aqui o resultado do modelo treinado |
| app.py | código do frontend do chatbot em versão browser |
| chatgui.py | código do frontend do chatbot em versão janela de conversão |
| processor.py | ficheiro com toda a funcionalidades tal como a previsão da intent, validação da acurrancy e escolha aleatória da resposta (sempre que há mais do que uma resposta |

### Executar o projeto:

Numa primeira fase é necessário criar o modelo de NLP (h5).
Segue o exemplo do ficheiro json com as intents:

<img width="698" alt="json" src="https://user-images.githubusercontent.com/76813386/156906247-a484bd9d-d493-4787-8078-e306bb99fc4c.PNG">

Na linha de Command Prompt, dentro do environment que tiver criado, (garanta que está na pasta onde descarregou os ficheiros do projeto antes de executar o comando):

> python chatbot.py

<img width="479" alt="criarmodelo" src="https://user-images.githubusercontent.com/76813386/156905708-db8b41e8-8f0c-4c51-9c8c-9ffed8fd1568.PNG">

Se não aparecer nenhum erro durante o treinamento e terminar com "model created" é porque o modelo foi criado com sucesso.

Neste momento estamos em condições de executar o aplicativo do chatbot.
Temos dois frontends diferentes:

> python app.py

O resultado deverá terminar com o link a copiar para o seu browser:

<img width="668" alt="browser" src="https://user-images.githubusercontent.com/76813386/156906048-37b1b3fb-aad9-4769-b6f8-76fa068f75f0.PNG">

Ao copiar o link para um browser, teremos um resultado deste tipo:

<img width="600" alt="chatbot_browser" src="https://user-images.githubusercontent.com/76813386/156905744-5e23119d-8b15-473d-8ab2-3d7e3a23250a.PNG">

Adicionei no final da resposta que o bot nos dá alguns dados que podem ser interessante na fase de treino

<img width="329" alt="output" src="https://user-images.githubusercontent.com/76813386/156905980-780ac09d-b156-4e64-9005-1af42887bea0.PNG">

Caso pretenda remover, basta alterar no file "processor.py".

> python chatgui.py

<img width="206" alt="chatbot_gui" src="https://user-images.githubusercontent.com/76813386/156906136-ff156fcf-74e8-4ef9-974c-63c98a625d15.PNG">

Neste caso, é aberto uma janela de chat e o resultado mostrado é semelhante ao exemplo anterior, até porque ambos partilham das mesmas funções do file "processor.py".

## Estrutura do JSON

O JSON tem informação das intents e das entidades, em forma de array. Essa informação é necessária para definir a lógica do de atuação do bot. Desta forma, é muito importante ficar explicado como está estruturado e o significado de cada parte.

### Intents

<img width="544" alt="json" src="https://user-images.githubusercontent.com/76813386/160299716-37d5a70b-20a8-4b22-9736-77b170200e6a.PNG">

A estrutura da **Intent** pode ter:
| Nome | significado | Mandatório | Exemplos |
| ---- | ----------- | ---------- | -------- |
| tag  | Nome da intent | sim | 'Obter_nome_melhor_aluno' |
| patterns | Formas diferentes de dizer o mesmo e que têm o mesmo sentido da Intent. Vão servir para a criação do modelo de IA | sim | ['Olá', 'Bom dia', ...] |
| responses | Respostas possíveis a dar no caso da Intent ser escolhida como provável. É um array de respostas para permitir escolher uma de forma aleatória e assim parecer mais uma conversa humana | sim | ['olá', 'Viva, como posso ajudar?'] |
| api_action | Corresponde ao url do webhook para fazer uma chamada ao exterior. Caso a resposta não necessite de fazer nenhuma chamada, deverá deixar com string vazia | sim | "https://xpto.com/demo?action=obter_nome_aluno" |
| api_param_type | informa, quando diferente de string vazia, o tipo de informação a extrair da frase para entregar na chamada da API. Este pode ser nome próprio (proper noun), verbo (verb), pronome (pronoun), advérbios (adverb), adjetivo (adjective), entre outros permitidos pela biblioteca spacy do python. Também pode ter o valor "entity" quando se trata de uma entidade. | Apenas obrigatório quando tem api_action <> "" | 'proper noun' |  
| api_param_name | Representa o nome do parâmetro que a api está desenhada para receber. Quando o campo api_param_type for igual a "entity", este campo deve também corresponder ao name da entidade correspondente | Apenas obrigatório quando tem api_action <> "" | 'aluno' |
| api_responses_missing_param | Sempre que não for encontrado a informação que mapea com o parâmetro de entrada para a API, pode colocar aqui a questão para obter a informação em falta. Este campo é um array de questões para que seja escolhida uma aleatoriamente e assim parecer uma conversa mais naturar com o cliente | Apenas se api_action <> "" e tiver parâmetro de entrada (api_param_type <> "") | ['Qual o nome da criança?', 'Como se chama a criança'] |

### Entity

<img width="637" alt="Entidade_config" src="https://user-images.githubusercontent.com/76813386/162626303-64f4d804-6865-4a7e-9724-ea60baf4fa57.PNG">

A estrutura da **Entity** pode ter:
| Nome | significado | Mandatório | Exemplos |
| ---- | ----------- | ---------- | -------- |
| name | Nome da entidade. Deverá corresponder ao valor dado ao parâmetro api_param_name da Intent que o vai usar | sim | periodo |
| values | corresponde ao dicionário dos possíveis valores e os respectivos sinónimos. Recomenda-se que a key do dicionário esteja também na lista de valores, para que seja tido em conta na procura. | sim | "values": {"parcial" : ["parcial", "meio periodo"], "integral" : ["integral", "dia completo"]} |


Este ficheiro é o coração do bot, onde toda a configuração vai implicar o comportamento do mesmo.


## Modelo de NLP

O modelo de IA criado é de 3 camadas. 
1. Primeira camada 128 neurônios
2. Segunda camada 64 neurônios
3. Terceira camada de saída contém o número de neurônios igual ao número de intenções para prever a intenção de saída com softmax

<img width="320" alt="modelo" src="https://user-images.githubusercontent.com/76813386/156906542-c8b128ff-fee2-4903-8172-78dee6bd2df0.PNG">

Não cheguei a experimentar variar os parâmetros como o número de camadas, o número de neorónios ou até mesmo as funções de ativação entre outros. A ideia aqui não era arranjar o melhor modelo possível, mas um que respondesse de forma razoavel para o desafio. (esta informação pode encontrar no file "chatbot.py")

Como ainda não é usado nenhum processo de contexto ou desambiguação, optei por usar dois tipos de threshold para aceitação da intent com maior probabilidade. Assim se o comprimento da frase do user for curto (len(sentença) < 10) uso um threshold de 80%, caso contrário este passa para 25%. Com isto, caso a maior probabilidade esteja abaixo do threshold a resposta será "Não entendi. Pode reformular a pergunta?" . (esta infomração encontra-se no file "processor.py")

## Bibliografia

Boa parte do código foram retirados de: <br>
https://data-flair.training/blogs/python-chatbot-project/ <br>
https://docs.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-create-bot?view=azure-bot-service-4.0&tabs=python%2Ccli <br>

Criação de environment: <br>
https://docs.python.org/3/tutorial/venv.html

Bibliotecas usadas:
https://www.nltk.org/
https://realpython.com/natural-language-processing-spacy-python/

