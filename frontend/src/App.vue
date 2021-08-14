<script lang="ts">
import { onBeforeMount } from "vue";
import { ref } from "vue";
import firebase from "firebase";
import axios from 'redaxios';

export default{
  setup(){
    const is_authenticated = ref(false)
    const email = ref("")
    const password = ref("")
    const access_token = ref("")

    onBeforeMount(() => {
      firebase.auth().onAuthStateChanged((user) =>{
        if (user){
          is_authenticated.value = true
          firebase.auth().currentUser?.getIdToken().then(async (token) => {
            try{
              access_token.value = token
              const response = await axios.post("http://127.0.0.1:8000/api/users/firebase/auth/", {"token": token})
              alert(JSON.stringify(response.data))
            }
            catch(e){
              console.log(e)
            }
          })
        }
        else {
          is_authenticated.value = false
        }
      })
    })

    const login = () => {
      firebase.auth().createUserWithEmailAndPassword(email.value, password.value)
      .catch((error) => {
        firebase.auth().signInWithEmailAndPassword(email.value, password.value)
      })
    }


    const logout = () => {
      firebase.auth().signOut()
    }

    const get_public = async () => {
      try{
        const response = await axios.get("http://127.0.0.1:8000/api/users/public/")
          alert(JSON.stringify(response.data))
      }
      catch(e){
        console.log(e)
      }

    }


    const get_protected = async () => {
      try{
        const config = {
          headers: { Authorization: `Bearer ${access_token.value}` }
        };
        console.log(config)
        const response = await axios.get("http://127.0.0.1:8000/api/users/protected/", config)
          alert(JSON.stringify(response.data))
      }
      catch(e){
        console.log(e)
      }

    }


   return {is_authenticated, email, password, login, logout, get_public, get_protected}
  }
}

</script>

<template>

  <div v-if="!is_authenticated">
    <label>Email</label>
    <input type="email" v-model="email" placeholder="Email" />

    <label>Password</label>
    <input type="password" v-model="password" placeholder="Password" />
    <button @click="login">Login</button>

    <button @click="get_public">Public API</button>
  </div>

  <div v-else>
    <h1>Hello</h1>
    <button @click="get_protected">Protected API</button>
    <button @click="logout">logout</button>

  </div>

</template>
