<template>
  <v-app>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="6">
          <v-textarea outlined v-model="fileText" name="input-7-4" label="Текст файла"></v-textarea>

          <v-textarea
            outlined
            v-model="hashText"
            name="input-7-4"
            label="Полученная хэш-функция"
          ></v-textarea>

          <v-file-input
            v-model="codeFile"
            accept=".txt"
            placeholder="Исходный текст (прикрепить файл)"
            label="Исходный текст (прикрепить файл)"
            @change="onChangeFile()"
          ></v-file-input>

          <v-btn elevation="3" v-on:click="onSubmit('hash')">Получить хэш-функцию</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      file: '',
      codeFile: '',
      hashText: '',
      fileText: '',
      fileLink: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/sha1';
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;
          this.hashText = res.data.hashText;
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
    getHash(payload) {
      const path = 'http://localhost:5000/sha1';
      axios
        .post(path, payload)
        .then(() => {
          this.getMessage();
        })
        .catch((error) => {
          // eslint-disable next string
          console.log(error);
        });
    },

    onChangeNumber(textField) {
      if (Number.isInteger(+textField)) {
        console.log('Все ок');
      } else {
        console.log('Что-то не ок');
      }
    },
    onChangeFile() {
      const fr = new FileReader();
      fr.readAsBinaryString(this.codeFile);
      fr.addEventListener('load', () => {
        this.fileText = fr.result;
      });
    },

    onSubmit() {
      const payload = {
        inputTxt: this.fileText,
      };
      this.getHash(payload);
    },

    changeComponent(item) {
      this.visible = item.visible;
      console.log(this.visible);
    },
  },
  watch: {
    switch1() {
      this.onChange();
    },
    numberValue1() {
      this.onChangeNumber(this.numberValue1);
    },
    numberValue2() {
      this.onChangeNumber(this.numberValue2);
    },
  },
  created() {},
};
</script>
