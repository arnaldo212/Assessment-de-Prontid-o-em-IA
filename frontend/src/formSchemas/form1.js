// Estrutura das perguntas do Formulário 1 — portada de Formulario_1_Geral.html.
// Cada item aponta a chave usada no payload enviado para POST /forms/form1.

export const FORM1_SECTIONS = [
  {
    tag: "M1",
    title: "Organização (Estratégia e Direção)",
    items: [
      { id: "m1q1", type: "likert", label: "Existe uma direção declarada da alta liderança sobre o papel da IA no futuro da companhia." },
      { id: "m1q2", type: "likert", label: "A liderança patrocina ativamente as iniciativas de IA, de modo que elas se conectam entre si em vez de ficarem isoladas." },
      { id: "m1q3", type: "likert", label: "A liderança sênior tem clareza de como a IA acelera as top metas estratégicas do ano." },
      { id: "m1q4", type: "likert", rev: true, label: "Na prática, as decisões sobre IA acontecem de forma reativa e dispersa, sem um direcionamento central." },
      { id: "m1q5", type: "ladder", label: "Qual frase melhor descreve o momento da liderança em relação à IA?", opts: [
        "Resiste ou ignora o tema.", "Quer usar, mas não sabe por onde começar.",
        "Cobra o uso, mas não dá direcionamento nem orçamento.", "Alinhada, com estratégia clara de desdobramento.",
      ]},
    ],
  },
  {
    tag: "M2",
    title: "Times (Processos, Rituais e Colaboração)",
    items: [
      { id: "m2q1", type: "likert", label: "Nossos rituais e reuniões abrem espaço intencional para discutir experimentos com IA." },
      { id: "m2q2", type: "likert", label: "Os times usam IA de forma intencional para resolver problemas que impactam o cliente." },
      { id: "m2q3", type: "likert", label: "Conseguimos medir e acompanhar o ganho de produtividade ou o impacto das ferramentas de IA adotadas." },
      { id: "m2q4", type: "likert", rev: true, label: "O uso de IA nos times é pontual e depende de poucos entusiastas." },
      { id: "m2q5", type: "ladder", label: "Como o conhecimento sobre IA circula entre os departamentos?", opts: [
        "Não circula; cada um faz o seu.", "Restrito a poucos entusiastas isolados.",
        "TI centraliza e dita as regras.", "Troca fluida, rituais compartilhados, aprendizado em rede.",
      ]},
    ],
  },
  {
    tag: "M3",
    title: "Pessoas (Crenças, Medos e Hábitos)",
    items: [
      { id: "m3q1", type: "likert", label: "Os colaboradores demonstram curiosidade e iniciativa própria para adotar IA no dia a dia." },
      { id: "m3q2", type: "likert", label: "Há clareza de que a IA veio para potencializar o trabalho humano, não para substituir postos." },
      { id: "m3q3", type: "likert", label: "A empresa oferece um plano estruturado de desenvolvimento para preparar as pessoas." },
      { id: "m3q4", type: "likert", rev: true, label: "Muitas pessoas ainda veem a IA como ameaça ao próprio emprego e evitam usá-la." },
      { id: "m3q5", type: "ladder", label: "Onde a empresa está na preparação de pessoas para a era da IA?", opts: [
        "Sem ação estruturada; esforço individual.", "Ações pontuais, sem trilhas nem novos papéis.",
        "Trilhas em construção e revisão de cargos.", "Desenvolvimento, papéis e atração já adaptados.",
      ]},
    ],
  },
  {
    tag: "A",
    title: "Literacia em IA (sobre você)",
    items: [
      { id: "a1", type: "ladder", label: "Seu contato com ferramentas de IA generativa:", opts: [
        "Nunca ouvi falar", "Já ouvi, nunca usei", "Testei poucas vezes", "Uso de vez em quando", "Uso com frequência no trabalho",
      ]},
      { id: "a2", type: "ladder", label: "Com que frequência usa IA no trabalho hoje?", opts: [
        "Nunca", "Algumas vezes por mês", "Semanalmente", "Diariamente",
      ]},
      { id: "a3", type: "multicheck", label: "Para quê você já usou IA? (marque todas)", opts: [
        "Escrever/revisar textos", "Resumir documentos", "Gerar ideias", "Planilhas/dados",
        "Traduzir", "Apresentações/materiais", "Buscar informação", "Programar",
      ]},
      { id: "a4", type: "likert", label: "Sei descrever bem o que quero para a IA e reformular quando o resultado não vem bom." },
      { id: "a5", type: "likert", label: "Confiro o resultado da IA antes de usar em algo importante." },
      { id: "a6", type: "likert", label: "Sei que a IA pode “inventar” informação com aparência de certeza, e levo isso em conta." },
      { id: "a7", type: "likert", label: "Sei quais informações não devo inserir em ferramentas de IA." },
      { id: "a8", type: "likert", label: "Entendo em que tipos de tarefa a IA ajuda mais e em quais não é confiável." },
      { id: "a9", type: "likert", rev: true, label: "Costumo apresentar resultados da IA sem conferir, mesmo quando não entendo bem como ela chegou neles." },
    ],
  },
  {
    tag: "C",
    title: "Checagem de conhecimento",
    items: [
      { id: "c1", type: "objective", label: "O que significa a IA “alucinar”?", opts: [
        "Ficar mais lenta", "Gerar informação falsa com aparência de verdadeira", "Recusar-se a responder", "Precisar de internet",
      ]},
      { id: "c2", type: "objective", label: "Forma mais confiável de reduzir erros factuais numa resposta de IA:", opts: [
        "Pedir com mais educação", "Repetir a mesma pergunta", "Conferir em fonte confiável e pedir que cite fontes", "Usar letras maiúsculas",
      ]},
      { id: "c3", type: "objective", label: "Qual informação NÃO deve ser inserida numa ferramenta de IA pública?", opts: [
        "Um texto genérico de marketing", "Dados pessoais/sigilosos de clientes", "Uma dúvida de português", "Um resumo público da empresa",
      ]},
      { id: "c4", type: "objective", label: "O que mais melhora a qualidade da resposta da IA?", opts: [
        "Um pedido claro, com contexto e exemplos", "Um pedido bem curto", "Escrever tudo em inglês", "Enviar várias vezes",
      ]},
      { id: "c5", type: "objective", label: "Sobre as respostas da IA generativa, é correto afirmar:", opts: [
        "São sempre verdadeiras e atualizadas", "Podem errar e devem ser verificadas", "Nunca inventam nada", "Substituem qualquer especialista",
      ]},
      { id: "c6", type: "objective", label: "Para uma tarefa repetitiva e de regras fixas, normalmente a melhor escolha é:", opts: [
        "Sempre IA generativa", "Automação/regras quando os passos são fixos; IA quando exige linguagem/julgamento", "Nunca automatizar", "Fazer sempre à mão",
      ]},
    ],
  },
  {
    tag: "B",
    title: "Oportunidade no trabalho",
    items: [
      { id: "b1", type: "likert", label: "Boa parte do meu tempo vai para tarefas repetitivas e previsíveis." },
      { id: "b2", type: "likert", label: "Meu trabalho envolve escrever, revisar ou responder muitos textos e e-mails." },
      { id: "b3", type: "likert", label: "Preciso ler e resumir muitos documentos ou relatórios." },
      { id: "b4", type: "likert", label: "Trabalho bastante com planilhas, dados ou números." },
      { id: "b5", type: "likert", label: "Passo parte do meu tempo procurando ou consultando informações digitais." },
      { id: "b6", type: "likert", label: "Crio apresentações, propostas, materiais ou conteúdo." },
      { id: "b7", type: "likert", label: "Respondo perguntas parecidas de clientes ou colegas com frequência." },
      { id: "b8", type: "likert", label: "Tarefas operacionais consomem meu dia e sobra pouco tempo para o estratégico." },
      { id: "b9b", type: "ladder", label: "Sua tarefa mais repetitiva segue passos previsíveis, que poderiam virar uma receita/checklist?", opts: [
        "Não — cada caso é diferente, exige julgamento.", "Em parte — há padrão, mas com muitas exceções.",
        "Bastante — padrão claro com poucas exceções.", "Totalmente — mesmos passos, sempre iguais.",
      ]},
    ],
  },
];

export const FORM1_REQUIRED_IDS = FORM1_SECTIONS.flatMap((s) => s.items.map((i) => i.id));
