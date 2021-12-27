<template>
  <v-app>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="pValue"
            outlined
            label="Простое число"
            placeholder="Простое число"
          />
          <v-textarea
            outlined
            v-model="inputTxt"
            name="input-7-4"
            label="Исходное сообщение"
          ></v-textarea>
          <v-textarea outlined v-model="stepTxt1" name="input-7-4" label="Шаг 1"></v-textarea>
          <v-textarea outlined v-model="stepTxt2" name="input-7-4" label="Шаг 2"></v-textarea>
          <v-textarea outlined v-model="stepTxt3" name="input-7-4" label="Шаг 3"></v-textarea>
          <v-textarea outlined v-model="stepTxt4" name="input-7-4" label="Шаг 4"></v-textarea>
        </v-col>
        <v-col cols="4" md="1">
          <v-btn elevation="40" v-on:click="onSubmit('step1')">Шаг 1</v-btn>
          <v-btn elevation="40" v-on:click="onSubmit('step2')" class="mt-10">Шаг 2</v-btn>
          <v-btn elevation="40" v-on:click="onSubmit('step3')" class="mt-16">Шаг 3</v-btn>
          <v-btn elevation="40" v-on:click="onSubmit('step4')" class="mt-16">Шаг 4</v-btn>
        </v-col>

        <v-col cols="4" md="2">
          <v-textarea v-model="secKeys1" outlined label="Секретные ключи абонента 1"></v-textarea>
        </v-col>
        <v-col cols="4" md="2">
          <v-textarea v-model="secKeys2" outlined label="Секретные ключи абонента 2"></v-textarea>
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
      inputTxt: '',
      stepTxt1: '',
      stepTxt2: '',
      stepTxt3: '',
      stepTxt4: '',
      secKeys1: '',
      secKeys2: '',
    };
  },
  methods: {
    getMessage(step) {
      const path = `http://localhost:5000/shamir/${step}`;
      axios
        .get(path)
        .then((res) => {
          if (step === 'step1') {
            this.stepTxt1 = res.data.stepTxt1;
            this.pValue = res.data.pValue;
            this.secKeys1 = res.data.secKeys1;
          } else if (step === 'step2') {
            this.stepTxt2 = res.data.stepTxt2;

            this.secKeys2 = res.data.secKeys2;
          } else if (step === 'step3') {
            this.stepTxt3 = res.data.stepTxt3;
          } else if (step === 'step4') {
            this.stepTxt4 = res.data.stepTxt4;
          }
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
    doStep(step, payload) {
      const path = `http://localhost:5000/shamir/${step}`;
      axios
        .post(path, payload)
        .then(() => {
          this.getMessage(step);
        })
        .catch((error) => {
          // eslint-disable next string
          console.log(error);
        });
    },

    onSubmit(step) {
      if (step === 'step1') {
        const payload = { inputTxt: this.inputTxt, pValue: this.pValue };
        this.doStep(step, payload);
      } else if (step === 'step2') {
        const payload = { inputTxt: this.stepTxt1, pValue: this.pValue, nValue: this.nValue };
        this.doStep(step, payload);
      } else if (step === 'step3') {
        const payload = { inputTxt: this.stepTxt2, pValue: this.pValue, secKeys1: this.secKeys1 };
        this.doStep(step, payload);
      } else if (step === 'step4') {
        const payload = { inputTxt: this.stepTxt3, pValue: this.pValue, secKeys2: this.secKeys2 };
        this.doStep(step, payload);
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
