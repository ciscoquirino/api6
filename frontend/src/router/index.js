import { createRouter, createWebHistory } from 'vue-router'
import ChatInterface from '../components/ChatInterface.vue'
import ComparacaoRespostas from '../components/ComparacaoRespostas.vue'

const routes = [
  {
    path: '/',
    name: 'avaliacao',
    component: ChatInterface,
  },
  {
    path: '/comparacao',
    name: 'comparacao',
    component: ComparacaoRespostas,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
