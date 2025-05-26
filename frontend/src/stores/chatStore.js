import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    question: '',
    resposta1: '',
    resposta2: '',
    evaluations: [],
  }),
  actions: {
    setQuestion(q) {
      this.question = q
    },
    setRespostas(r1, r2) {
      this.resposta1 = r1
      this.resposta2 = r2
    },
    setEvaluations(evals) {
      this.evaluations = evals
    },
  },
})
