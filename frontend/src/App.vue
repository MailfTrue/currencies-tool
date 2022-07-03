<template>
  <toast/>
  <Card>
    <template #title>
      Currencies quotes
    </template>
    <template #content>
      <form @submit.prevent="loadQuotes">
        <div class="field grid">
          <div class="col-12">
            <MultiSelect id="currencies" v-model="selected" :options="currenciesOptions"
                         placeholder="Select currencies.." :loading="currenciesLoading"
                         option-label="name" option-value="value" class="mr-4 w-full"/>
          </div>
        </div>
        <div class="grid">
          <div class="col-12 md:col-6">
            <Button label="Get quotes" type="submit" class="w-full"/>
          </div>
          <div class="col-12 md:col-6 flex justify-content-around">
            <Button icon="pi pi-external-link" label="Excel" @click="exportQuotes('xlsx')"/>
            <Button icon="pi pi-external-link" label="PDF" @click="exportQuotes('pdf')"/>
            <Button icon="pi pi-external-link" label="HTML" @click="exportQuotes('html')"/>
            <Button icon="pi pi-external-link" label="CSV" @click="exportQuotes('csv')"/>
          </div>
        </div>
      </form>
      <DataTable :value="currenciesTable" :loading="quotesLoading">
        <Column field="char_code" header="Currency code"></Column>
        <Column field="name" header="Name"></Column>
        <Column field="denomination" header="Denomination"></Column>
        <Column field="value" header="Price"></Column>
        <Column field="date" header="Updated"></Column>
        <template #empty>
          No currencies.
        </template>
        <!--    <Column field="date" header="Дата котировки"></Column>-->
      </DataTable>
    </template>
  </Card>
</template>

<script>
import FileDownload from 'js-file-download';
import Toast from 'primevue/toast';
import MultiSelect from 'primevue/multiselect';
import Card from 'primevue/card';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import API from './api';

const currencyNames = new Intl.DisplayNames(['en'], {type: 'currency'});

export default {
  name: 'App',
  components: {
    MultiSelect,
    Card,
    DataTable,
    Column,
    Button,
    Toast,
  },
  data: () => ({
    quotes: null,
    quotesLoading: false,
    currencies: null,
    currenciesLoading: false,
    selected: [],
  }),
  computed: {
    currenciesOptions() {
      if (!this.currencies) return [];
      return this.currencies.map(currency => ({
        name: currencyNames.of(currency.char_code),
        value: currency.char_code,
      }))
    },
    currenciesTable() {
      if (!this.quotes) return [];
      return this.quotes.currencies.map(currency => ({
        ...currency,
        name: currencyNames.of(currency.char_code),
        date: new Date(this.quotes.date).toLocaleString(),
        value: `₽${currency.value}`,
      }));
    }
  },
  created() {
    this.api = new API();
  },
  mounted() {
    this.loadCurrencies()
  },
  methods: {
    loadQuotes() {
      this.quotesLoading = true;
      this.api.getQuotes({data: this.selected}).then((response) => {
        this.quotesLoading = false;
        this.quotes = response.data;
      }).catch(err => {
        this.quotesLoading = false;
        this.$toast.add({severity: 'error', summary: 'Error', detail: 'Failed to fetch quotes', life: 3000});
        console.error(err);
      });
    },
    loadCurrencies() {
      this.currenciesLoading = true;
      this.api.getCurrencies().then((response) => {
        this.currenciesLoading = false;
        this.currencies = response.data;
      }).catch(err => {
        this.currenciesLoading = false;
        this.$toast.add({severity: 'error', summary: 'Error', detail: 'Failed to fetch currencies list', life: 3000});
        console.error(err);
      });
    },
    exportQuotes(format) {
      this.api.getQuotes({
        data: this.selected,
        config: {params: {export_to: format}, responseType: "blob"},
      }).then((response) => {
        const todayStr = new Date().toLocaleString().replace(" ", "_");
        FileDownload(response.data, `export_${todayStr}.${format}`, response.headers['content-type']);
      }).catch(err => {
        this.$toast.add({severity: 'error', summary: 'Error', detail: 'Failed to export quotes', life: 3000});
        console.error(err);
      });
    }
  }
};
</script>

<style>
@import "primevue/resources/primevue.min.css";
@import "primevue/resources/themes/saga-blue/theme.css";
@import "primeicons/primeicons.css";
@import "primeflex/primeflex.css";
</style>
