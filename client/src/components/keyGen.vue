<template>
  <v-app>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="pValue"
            outlined
            label="Простое число p"
            placeholder="Простое число p"
          />
          <v-text-field
            v-model="qValue"
            outlined
            label="Простое число q"
            placeholder="Простое число q"
          />
          <v-text-field
            v-model="gValue"
            outlined
            label="Выбранное число g"
            placeholder="Выбранное число g"
          />

          <v-btn elevation="3" v-on:click="onSubmit('code')">Сгенерировать ключи</v-btn>
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
            v-model="opKeyA"
            outlined
            label="Открытый ключ A"
            placeholder="Открытый ключ A"
          />
          <v-text-field
            v-model="opKeyB"
            outlined
            label="Открытый ключ B"
            placeholder="Открытый ключ B"
          />
          <v-text-field v-model="answ1" outlined label="Ответ 1" placeholder="Ответ 1" />
          <v-text-field v-model="answ2" outlined label="Ответ 2" placeholder="Ответ 2" />
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
      pValue: '',
      qValue: '',
      gValue: '',
      secKeyA: '',
      secKeyB: '',
      opKeyA: '',
      opKeyB: '',
      answ1: '',
      answ2: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/keygen';
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;

          this.pValue = res.data.pValue;
          this.qValue = res.data.qValue;
          this.gValue = res.data.gValue;
          this.secKeyA = res.data.secKeyA;
          this.secKeyB = res.data.secKeyB;
          this.opKeyA = res.data.opKeyA;
          this.opKeyB = res.data.opKeyB;
          this.answ1 = res.data.answ1;
          this.answ2 = res.data.answ2;
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
    onChange() {
      if (this.switch1) this.switch1Label = 'Зашифровать';
      else this.switch1Label = 'Расшифровать';
    },

    onSubmit() {
      this.getMessage();
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
