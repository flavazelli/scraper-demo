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
  const selectedFile = ref([])

  const submit = async () => {
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

  const onUpload = async($event) => {
    try {
        console.log($event.files[0].name)
        isLoading.value = true
        const formData = new FormData();
        formData.append("file", $event.files[0])
        const response = await fetch('http://localhost:8000/file', {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        markdown.value = data.response
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
    <FileUpload :disabled=isLoading mode="basic" auto accept="image/*" :maxFileSize="100000000" @select="onUpload($event)" chooseLabel="Browse" />
    <ProgressSpinner v-if=isLoading />
    <VueMarkdown class= "vue-markdown " :source="markdown" />
  </div>
</template>
<style>
</style>
