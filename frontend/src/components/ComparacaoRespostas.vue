<template>
  <div class="max-w-5xl mx-auto bg-white p-6 rounded shadow space-y-6">
    <h2 class="text-2xl font-bold">Comparação entre Respostas</h2>

    <div class="grid md:grid-cols-2 gap-6">
      <div class="p-4 border rounded bg-gray-50">
        <h3 class="font-semibold mb-2">Resposta 1</h3>
        <p class="whitespace-pre-line">{{ resposta1 }}</p>
      </div>
      <div class="p-4 border rounded bg-gray-50">
        <h3 class="font-semibold mb-2">Resposta 2</h3>
        <p class="whitespace-pre-line">{{ resposta2 }}</p>
      </div>
    </div>

    <div class="mt-6">
      <label class="block mb-2 font-medium">Comparação:</label>
      <select v-model="score" class="w-full border rounded px-2 py-1">
        <option disabled value="">Selecione</option>
        <option value="1">1 - Resposta 1 é muito melhor</option>
        <option value="2">2 - Resposta 1 é melhor</option>
        <option value="3">3 - Ambas são iguais</option>
        <option value="4">4 - Resposta 2 é melhor</option>
        <option value="5">5 - Resposta 2 é muito melhor</option>
      </select>

      <textarea
        v-model="comment"
        class="w-full border rounded px-2 py-1 mt-4"
        rows="4"
        placeholder="Justifique sua escolha"
      ></textarea>
    </div>

    <div class="text-right mt-6">
      <button
        class="bg-green-600 text-white px-4 py-2 rounded"
        @click="enviarComparacao"
      >
        Enviar Comparação
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

import { useChatStore } from '../stores/chatStore'

const chatStore = useChatStore()
const resposta1 = chatStore.resposta1
const resposta2 = chatStore.resposta2


const score = ref('')
const comment = ref('')

const enviarComparacao = async () => {
  const res = await fetch('http://localhost:5000/api/compare', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resposta1: chatStore.resposta1,
      resposta2: chatStore.resposta2,
      score: score.value,
      comment: comment.value,
    }),
  })

  const data = await res.json()
  alert(data.message)
}
</script>
