import torch
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

original_text: list[str] = [
    "O CS50 é um curso introdutório de Ciência da Computação da Universidade de Harvard. Ele é dividido em semanas, começando pela semana 0 com o Scratch, e vai até a semana 10, que aborda conceitos de Inteligência Artificial.",
    "O curso é ministrado por David J. Malan, professor formado e doutor em Ciência da Computação pela própria Harvard. Embora o conteúdo seja atualizado anualmente, o objetivo principal do CS50 não é apresentar as tecnologias mais populares do momento, mas sim ensinar os fundamentos essenciais para quem deseja trabalhar com desenvolvimento de software.",
    "Ao longo do curso, passamos por:",
    "Embora exista debate sobre o C ser uma linguagem de alto ou baixo nível, essa discussão foge tanto da minha competência quanto do foco do curso. O que realmente importa é que aprender C nos obriga a lidar com aspectos fundamentais da computação, o que proporciona uma compreensão mais profunda da programação, pois estamos lidando diretamente com a memória da máquina. A forma como declaramos as variáveis também importa, se não o código nem compila.",
    "Ao iniciarmos a aula da semana 1, somos introduzidos a alguns conceitos importantes da linguagem C, vamos listar eles aqui.",
    'Por isso é necessário adicionar um compilador a sua máquina quando se programa em C, C++. Atualmente eu tenho preferência pelo GCC, entretando existem outros disponíveis para experimentar. O compilador também serve como uma maneira de comunicar falhas no seu código, indicando linhas em que estão estes erros, podendo ser de sintaxe, léxico, etc(provavelmente um ";").',
    "Ao final de cada aula, são disponibilizados exercícios para praticar os conceitos apresentados. Acredito que para alguém com mais experiência na área e uma lógica forte, não terá dificuldades em resolver as questões(existem algumas cabreiras, mas ainda não chegamos lá). É preciso lembrar também que são questões feitas para ",
    'Pessoalmente, eu sempre opto por resolver o exercício mais simples, e manter o mais dificil como uma revisão que utilizarei eventualmente. Dito isso, vamos ao exercício: é proposto que desenhemos com "#" as pirâmides do jogo Super Mario Bros., aquele amontoado de quadrados, sabe? Minha solução ficou dessa forma:',
    "Por padrão ao curso, eu opto por manter meus comentários em inglês.",
    "A proposta é simples: dado um valor em centavos, calcular quantas moedas de 25¢, 10¢, 5¢ e 1¢ são necessárias para dar o troco com o menor número de moedas possível. Sinceramente o que mais aprendi aqui foi sobre o nomeclatura das moedas que eles usam (CS50 também é cultura). A lógica por trás é de um algoritmo ganancioso: Sempre usamos a maior moeda possível em cada etapa.",
    "Vamos ao código.",
    "Sei que não é a maneira mais otimizada de solucionar este problema. Eu poderia ter usado divisão inteira e %, no entanto decidi priorizar a lógica e a estrutura do código, quase uma descrição lógica do passo a passo.",
    "Gosto da didática do David, e como os exercícios são feitos para utilizar tudo aquilo que lhe foi ensinado durante a aula. Sei que poderia ter usado a biblioteca <math.h>, no entanto optei por resolver tudo na unha para me acostumar ao estilo do curso. Volto semana que vem com minhas considerações sobre a Week 2 - Arrays.",
    "Na minha postagem anterior, eu mencionei estudar o SICP também. Ainda o farei, no entanto a vida acontece e a vida pessoal tem exigido muito da minha atenção, então estarei optando para acompanhar este material após terminar o CS50.",
    "Agradeço a atenção de cada um que parou para ler um pouco do que escrevi, entendo que minha didática não possa estar tão clara, e alguns conceitos podem ter sido explicados de forma incorreta, para isso estou aberto a críticas e direções. Até semana que vem.",
]

messages = [
    {
        "role": "system",
        "content": "Voce e um assistente especialista em redação de textos, com foco em resumos de textos longos. Seu objetivo e receber um texto longo e resumir em um texto mais curto, mantendo o maior numero possivel de detalhes e informacoes. Regras: 1. O resumo deve ser escrito em portugues brasileiro. 2. O resumo deve ser escrito de forma clara e objetiva, com um tom neutro e objetivo. 3. O resumo deve ser escrito de forma a ser facilmente compreendido por pessoas que nao sao especialistas na area do texto original. 4. O resumo deve ser escrito de forma a ser facilmente compreendido por pessoas que nao sao especialistas na area do texto original. 5. O resumo nao deve ultrapassar 4 paragrafos e nao deve conter mais de 2000 caracteres.",
    },
    {"role": "user", "content": "\n".join(original_text)},
]

prompt = pipe.tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)

outputs = pipe(
    prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95
)

print("result:", outputs[0]["generated_text"])
