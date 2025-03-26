<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

input {
  margin-bottom: 20px;
  width: 50%;
}

.vue-markdown {
  width: 50%;
}
</style>
<script setup lang="ts">
  import VueMarkdown from 'vue-markdown-render'
  import { ProgressSpinner, InputText, FileUpload } from 'primevue';
  import { ref } from 'vue'
  
  const markdown = ref('')
  const formFieldValue = ref('')
  const isLoading = ref(false)

  const submit = async (event) => {
    try {
        isLoading.value = true
        const response = await fetch('http://localhost:8000/question', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: formFieldValue.value }),
        });
        const data = await response.json();
        console.log(data.response)
        markdown.value = data.response
        console.log(markdown)
      } catch (error) {
        console.error('Error:', error);
      } finally {
        isLoading.value = false
      }
  };

  const onUpload = async() => {
    try {
        isLoading.value = true
        const response = await fetch('http://localhost:8000/question', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: formFieldValue.value }),
        });
        const data = await response.json();
        console.log(data.response)
        markdown.value = data.response
        console.log(markdown)
      } catch (error) {
        console.error('Error:', error);
      } finally {
        isLoading.value = false
      }
  };
</script>
<template>
  <div class="container">
    <InputText :disabled=isLoading placeholder="Type grocery list here or click below to upload picture of grocery list..." type="text" v-model="formFieldValue" @keyup.enter="submit"/>
    <FileUpload :disabled=isLoading  mode="basic" name="demo[]" accept="image/*" :maxFileSize="1000000" @upload="onUpload" :auto="true" chooseLabel="Browse" />
    <ProgressSpinner v-if=isLoading />
    <VueMarkdown class= "vue-markdown " :source="markdown" />
  </div>
</template>
<style>
</style>
