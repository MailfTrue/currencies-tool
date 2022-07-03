import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';
import App from './App.vue';

const app = createApp(App);

app.use(PrimeVue);
app.use(ToastService);

app.mount('#app');
