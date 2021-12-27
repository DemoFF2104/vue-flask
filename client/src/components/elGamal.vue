<template>
  <v-app>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="6">
          <v-textarea outlined v-model="text" name="input-7-4" label="Исходный текст"></v-textarea>

          <v-textarea
            outlined
            v-model="codeText"
            name="input-7-4"
            label="Зашифрованный текст"
          ></v-textarea>
          <v-textarea
            outlined
            v-model="decodeText"
            name="input-7-4"
            label="Сообщение получателя"
          ></v-textarea>

          <v-btn elevation="3" v-on:click="onSubmit('send')" :disabled="text == ''"
            >Зашифровать и отправить</v-btn
          >
          <v-btn elevation="3" v-on:click="onSubmit('decode')" :disabled="codeText == ''"
            >Расшифровать</v-btn
          >
        </v-col>
        <v-col cols="8" md="4">
          <v-text-field
            v-model="secKeyA"
            outlined
            label="Секретный ключ A"
            placeholder="Секретный ключ A"
          />
          <v-text-field
            v-model="secKeyB"
            outlined
            label="Секретный ключ B"
            placeholder="Секретный ключ B"
          />
          <v-text-field
            v-model="openKeyA"
            outlined
            label="Открытый ключ A"
            placeholder="Открытый ключ A"
          />
          <v-text-field
            v-model="openKeyB"
            outlined
            label="Открытый ключ B"
            placeholder="Открытый ключ B"
          />
          <v-text-field
            v-model="pValue"
            outlined
            label="Простое число p"
            placeholder="Простое число p"
          />
          <v-text-field
            v-model="gValue"
            outlined
            label="Выбранное число g"
            placeholder="Выбранное число g"
          />
          <v-btn elevation="3" v-on:click="onSubmit('keygen')">Сгенерировать ключи</v-btn>
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
      text: '',
      pValue: '',
      qValue: '',
      gValue: '',
      secKeyA: '',
      secKeyB: '',
      openKeyA: '',
      openKeyB: '',
      codeText: '',
      decodeText: '',
      rNumbers: [],
    };
  },
  methods: {
    getMessage(flag) {
      const path = `http://localhost:5000/elgamal/${flag}`;
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;
          if (flag === 'keygen') {
            this.pValue = res.data.pValue;
            this.qValue = res.data.qValue;
            this.gValue = res.data.gValue;
            this.secKeyA = res.data.secKeyA;
            this.secKeyB = res.data.secKeyB;
            this.openKeyA = res.data.openKeyA;
            this.openKeyB = res.data.openKeyB;
          } else if (flag === 'send') {
            this.codeText = res.data.codeText;

            this.rNumbers = res.data.rNumbers;
          } else if (flag === 'decode') {
            this.decodeText = res.data.decodeText;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },

    onSubmit(flag) {
      if (flag === 'keygen') {
        this.getMessage('keygen');
      } else if (flag === 'send') {
        const payload = {
          inputTxt: this.text,
          pValue: this.pValue,
          gValue: this.gValue,
          openKeyB: this.openKeyB,
        };
        this.elSend(payload);
      } else if (flag === 'decode') {
        const payload = {
          inputTxt: this.codeText,
          rNumbers: this.rNumbers,
          pValue: this.pValue,
          secKeyB: this.secKeyB,
        };
        this.elDecode(payload);
      }
    },
    elSend(payload) {
      const path = 'http://localhost:5000/elgamal/send';
      axios
        .post(path, payload)
        .then(() => {
          this.getMessage('send');
        })
        .catch((error) => {
          // eslint-disable next string console.log(error);
          console.log(error);
        });
    },
    elDecode(payload) {
      const path = 'http://localhost:5000/elgamal/decode';
      axios
        .post(path, payload)
        .then(() => {
          this.getMessage('decode');
        })
        .catch((error) => {
          // eslint-disable next string console.log(error);
          console.log(error);
        });
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
