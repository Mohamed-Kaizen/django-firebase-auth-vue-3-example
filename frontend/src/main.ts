import { createApp } from 'vue'
import App from './App.vue'
import firebase from "firebase";

const firebaseConfig = {
    apiKey: "AIzaSyAo_R3eROHoFFiSpILnMFhG9XcxKJ0p8zk",
    authDomain: "django-firebaseauth-vue3.firebaseapp.com",
    projectId: "django-firebaseauth-vue3",
    storageBucket: "django-firebaseauth-vue3.appspot.com",
    messagingSenderId: "938030432919",
    appId: "1:938030432919:web:a6b2d545e11ff553cd9fd2"
  };

firebase.initializeApp(firebaseConfig)

createApp(App).mount('#app')
