<template>
  <v-app>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="6">
          <v-textarea
            outlined
            v-model="resultText"
            name="input-7-4"
            label="Исходный текст"
          ></v-textarea>

          <v-textarea
            outlined
            v-model="codeText"
            name="input-7-4"
            label="Зашифрованный текст"
          ></v-textarea>

          <v-file-input
            v-model="file"
            accept=".txt"
            placeholder="Исходный текст (прикрепить файл)"
            label="Исходный текст (прикрепить файл)"
            @change="onChangeFile('encode')"
          ></v-file-input>
          <v-file-input
            v-model="codeFile"
            accept=".txt"
            placeholder="Зашифрованный текст (прикрепить файл)"
            label="Зашифрованный текст (прикрепить файл)"
            @change="onChangeFile('code')"
          ></v-file-input>

          <v-btn class="ma-2" outlined :href="fileLink" download>
            Download PDF
          </v-btn>

          <v-btn elevation="3" v-on:click="onSubmit('code')">Зашифровать</v-btn>
          <v-btn elevation="3" v-on:click="onSubmit('decode')">Расшифровать</v-btn>
        </v-col>
        <v-col cols="8" md="4">
          <v-text-field v-model="dValue" outlined label="Значение d" placeholder="Значение d" />
          <v-text-field v-model="nValue" outlined label="Значение n" placeholder="Значение n" />
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
      items: [
        { title: 'RSA', icon: 'mdi-view-dashboard', visible: 'gcd' },
        { title: 'RSA1', icon: 'mdi-forum', visible: 'modul' },
        { title: 'RSA2', icon: 'mdi-forum', visible: 'inv' },
      ],

      ex11: true,
      switch1: true,
      switch1Label: 'Зашифровать',
      msg: [],
      dValue: '',
      nValue: '',
      numberValue3: '',
      visible: '',
      file: '',
      codeFile: '',
      resultText: '',
      codeText: '',
      fileLink: '',
    };
  },
  methods: {
    getMessage(flag) {
      const path = `http://localhost:5000/rsa/${flag}`;
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;

          if (flag === 'code') {
            this.codeText = res.data.codeText.toString();
            this.dValue = res.data.dValue;
            this.nValue = res.data.nValue;
          } else this.resultText = res.data.codeText.toString();
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
    rsaCode(payload) {
      const path = 'http://localhost:5000/rsa/code';
      axios
        .post(path, payload)
        .then(() => {
          this.getMessage('code');
        })
        .catch((error) => {
          // eslint-disable next string
          console.log(error);
        });
    },
    rsaEncode(payload) {
      const path = 'http://localhost:5000/rsa/encode';
      axios
        .post(path, payload)
        .then(() => {
          this.getMessage('encode');
        })
        .catch((error) => {
          // eslint-disable next string
          console.log(error);
        });
    },

    onChange() {
      if (this.switch1) this.switch1Label = 'Зашифровать';
      else this.switch1Label = 'Расшифровать';
    },
    onChangeNumber(textField) {
      if (Number.isInteger(+textField)) {
        console.log('Все ок');
      } else {
        console.log('Что-то не ок');
      }
    },
    onChangeFile(flag) {
      const fr = new FileReader();
      if (flag === 'code') {
        fr.readAsText(this.codeFile);
        fr.addEventListener('load', () => {
          this.codeText = fr.result;
        });
      } else {
        fr.readAsText(this.file);

        fr.addEventListener('load', () => {
          this.resultText = fr.result;
        });
      }
    },

    onSubmit(flag) {
      if (flag === 'code') {
        const payload = {
          text: this.resultText,
        };
        this.rsaCode(payload);
      } else {
        const payload = { text: this.codeText, dValue: this.dValue, nValue: this.nValue };
        this.rsaEncode(payload);
      }
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
    codeText() {
      console.log(this.codeText);
      const newArrUBuf = new Uint8Array(this.codeText);
      console.log(newArrUBuf);
      const blob = new Blob([this.codeText]);
      this.fileLink = URL.createObjectURL(blob);
    },
  },
  created() {},
};
</script>
