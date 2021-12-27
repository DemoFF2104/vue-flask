<template>
  <v-app>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="6" v-show="visible == 'gcd'">
          <v-text-field
            v-model="numberValue1"
            hide-details
            single-line
            type="number"
            label="Первое число"
          />
          <v-text-field
            v-model="numberValue2"
            hide-details
            single-line
            type="number"
            label="Второе число"
          />
          <v-text-field
            v-model="numberResult"
            hide-details
            single-line
            type="number"
            label="Наибольший общий делитель"
          />
          <v-btn elevation="3" v-on:click="onSubmit" class="mt-10">Отправить</v-btn>
        </v-col>
        <v-col cols="12" md="6" v-show="visible == 'modul'">
          <v-text-field v-model="numberValue1" hide-details single-line type="number" label="A" />
          <v-text-field v-model="numberValue2" hide-details single-line type="number" label="X" />
          <v-text-field v-model="numberValue3" hide-details single-line type="number" label="P" />
          <v-text-field
            v-model="numberResult"
            hide-details
            single-line
            type="number"
            label="A^x mod p"
          />

          <v-btn elevation="3" v-on:click="onSubmit" class="mt-10">Отправить</v-btn>
        </v-col>
        <v-col cols="12" md="6" v-show="visible == 'inv'">
          <v-text-field v-model="numberValue1" hide-details single-line type="number" label="X" />
          <v-text-field v-model="numberValue2" hide-details single-line type="number" label="P" />
          <v-text-field
            v-model="numberResult"
            hide-details
            single-line
            type="number"
            label="x^-1 mod p"
          />

          <v-btn elevation="3" v-on:click="onSubmit" class="mt-10">Отправить</v-btn>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="pa-12" color="indigo darken-2" flat>
            <v-card elevation="12" width="300">
              <v-navigation-drawer floating permanent>
                <v-list dense rounded>
                  <v-list-item
                    v-for="item in items"
                    :key="item.title"
                    link
                    v-on:click="changeComponent(item)"
                  >
                    <v-list-item-icon>
                      <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>

                    <v-list-item-content>
                      <v-list-item-title>{{ item.title }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-navigation-drawer>
            </v-card>
          </v-card>
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
        { title: 'NOD', icon: 'mdi-view-dashboard', visible: 'gcd' },
        { title: 'Возведение по модулю', icon: 'mdi-forum', visible: 'modul' },
        { title: 'Инверсия', icon: 'mdi-forum', visible: 'inv' },
      ],

      ex11: true,
      switch1: true,
      switch1Label: 'Зашифровать',
      msg: [],
      numberValue1: null,
      numberValue2: null,
      numberValue3: null,
      numberResult: null,
      visible: '',
    };
  },
  methods: {
    getMessage(visible) {
      const path = `http://localhost:5000/number/${visible}`;
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;
          console.log(res.data.numbers);
          this.numberResult = res.data.numbers;
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
    numberReq(payload) {
      const path = `http://localhost:5000/number/${this.visible}`;
      axios
        .post(path, payload)
        .then(() => {
          this.getMessage(this.visible);
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
    onSubmit() {
      if (this.visible !== 'modul') {
        const payload = {
          number1: this.numberValue1,
          number2: this.numberValue2,
        };
        this.numberReq(payload);
      } else {
        const payload = {
          number1: this.numberValue1,
          number2: this.numberValue2,
          number3: this.numberValue3,
        };
        this.numberReq(payload);
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
  },

  created() {},
};
</script>
