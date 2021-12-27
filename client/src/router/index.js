import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Rsa from '@/components/Rsa';
import keyGen from '@/components/keyGen';
import Shamir from '@/components/Shamir';
import elGamal from '@/components/elGamal';
import md5 from '@/components/md5';
import sha1 from '@/components/sha1';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/RSA',
      name: 'RSA',
      component: Rsa,
    },
    {
      path: '/keygen',
      name: 'keygen',
      component: keyGen,
    },
    {
      path: '/shamir',
      name: 'shamir',
      component: Shamir,
    },
    {
      path: '/elgamal',
      name: 'elgamal',
      component: elGamal,
    },
    {
      path: '/md5',
      name: 'md5',
      component: md5,
    },
    {
      path: '/sha1',
      name: 'sha1',
      component: sha1,
    },
  ],
});
