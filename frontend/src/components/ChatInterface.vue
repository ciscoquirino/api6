<template>
  <div class="max-w-6xl mx-auto bg-white p-6 rounded-lg shadow space-y-6">
    <h1 class="text-2xl font-bold">Sistema RLHF</h1>

    <!-- PERGUNTA -->
    <form @submit.prevent="handleSubmit" class="flex gap-2">
      <input
        v-model="question"
        type="text"
        class="flex-1 border px-4 py-2 rounded"
        placeholder="Digite sua pergunta..."
        required
      />
      <button class="bg-blue-600 text-white px-4 py-2 rounded">Enviar</button>
    </form>

    <!-- RESPOSTAS E AVALIAÇÃO -->
    <div v-if="responses.length" class="grid md:grid-cols-2 gap-6">
      <div
        v-for="(response, index) in responses"
        :key="index"
        class="border rounded p-4 bg-gray-50"
      >
        <h2 class="font-semibold text-lg mb-2">Resposta {{ index + 1 }}</h2>
        <p class="mb-4 whitespace-pre-line">{{ response['resposta'] }}</p>

        <div class="space-y-4">
          <div
            v-for="criterion in criteria"
            :key="criterion"
            class="space-y-1"
          >
            <label class="font-medium block">
              {{ criterion }}:
            </label>

            <select
              v-model="ratings[index][criterion].score"
              class="border px-2 py-1 rounded w-full"
              required
            >
              <option disabled value="">Nota (1 a 5)</option>
              <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
            </select>

            <textarea
              v-model="ratings[index][criterion].comment"
              class="w-full border rounded px-2 py-1"
              rows="2"
              placeholder="Justifique a nota..."
              required
            ></textarea>
          </div>
        </div>
      </div>
    </div>

    <!-- BOTÃO DE ENVIO DAS AVALIAÇÕES -->
    <div v-if="responses.length" class="text-right">
      <button
        @click="submitEvaluation"
        class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        Enviar Avaliações
      </button>
    </div>
    
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'
import { useChatStore } from '../stores/chatStore'

const router = useRouter()
const chatStore = useChatStore()

const question = ref('');
const responses = ref([]);

const criteria = ['Instrução', 'Linguagem', 'Veracidade', 'Ética'];

const ratings = ref([
  {}, // resposta 1
  {}, // resposta 2
]);

// Inicializa o estado de avaliação para cada resposta
function initRatings() {
  ratings.value = responses.value.map(() => {
    const obj = {};
    criteria.forEach((c) => {
      obj[c] = { score: '', comment: '' };
    });
    return obj;
  });
}

const handleSubmit = async () => {
  const res = await fetch("http://localhost:5000/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question.value }),
  });
  const data = await res.json();
  responses.value = data.responses;
  initRatings();
};

const submitEvaluation = async () => {
    await fetch("http://localhost:5000/api/evaluate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question: question.value,
      evaluations: ratings.value,
      responses: responses.value,
    }),
  })

  chatStore.setQuestion(question.value)
  chatStore.setRespostas(responses.value[0].resposta, responses.value[1].resposta)
  chatStore.setEvaluations(ratings.value)

  router.push({
    name: 'comparacao'
  })

};


</script>
