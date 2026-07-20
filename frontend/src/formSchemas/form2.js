export const FORM2_ITEMS = [
  { id: "q41", type: "ladder", label: "Onde moram os dados da empresa e quão acessíveis eles são para a IA?", opts: [
    "Dispersos em silos e planilhas sem integração.", "Parcialmente consolidados, acesso manual.",
    "Centralizados, mas não utilizáveis pela IA.", "Centralizados e acessíveis à IA por interfaces/APIs governadas.",
  ]},
  { id: "q42", type: "likert", label: "Conseguimos avaliar, caso a caso, se a IA tem acurácia suficiente para a tarefa." },
  { id: "q43", type: "likert", label: "Avaliamos criticamente o output da IA e só usamos resultados que compreendemos e sabemos defender." },
  { id: "q44", type: "likert", label: "Cada processo automatizado tem um responsável humano definido, que responde pelos resultados." },
  { id: "q45", type: "likert", label: "Conhecemos as exigências de privacidade do nosso setor (incl. LGPD) e as ferramentas as respeitam." },
  { id: "q46", type: "ladder", label: "Qual é a orientação estratégica predominante da adoção de IA?", opts: [
    "Só corte de custos.", "Sobretudo custos.", "Equilíbrio entre eficiência e crescimento.", "Orientada a crescimento e inovação.",
  ]},
  { id: "q47", type: "likert", label: "Medimos o custo e a acurácia atuais dos processos manuais (linha de base)." },
  { id: "q48", type: "likert", rev: true, label: "Adotamos ferramentas de IA principalmente pelo preço da assinatura, sem avaliar complexidade, privacidade e integração." },
];

export const FORM2_REQUIRED_IDS = FORM2_ITEMS.map((i) => i.id);
