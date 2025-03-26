
<template>
  <VaFormField v-model="formFieldValue" @keyup.enter="submit" >
    <template #default="{ value }">
      <input placeholder="Write here..." class="border-2 border-sold border-grey-300 px-2">
    </template>

    <template #message="{ messages }">
      {{ messages }}
    </template>
  </VaFormField>
  <vue-markdown :source="src" />
</template>
<script setup lang="ts">
import VueMarkdown from 'vue-markdown-render'

const formFieldValue = defineModel('formFieldValue')
const markdown = defineModel('markdown')

  const submit = async (event) => {
    try {
        const response = await fetch('http://localhost:8000/question', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: formFieldValue.value }),
        });
        const data = await response.json();
        markdown = data
      } catch (error) {
        console.error('Error:', error);
      }
  };
</script>

<style>

</style>
