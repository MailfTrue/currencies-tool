import axios from 'axios';

export default class API {
  constructor() {
    this.client = axios.create({
      baseURL: '/api',
    });
  }

  async getCurrencies() {
    return (await this.client.get('/currencies'));
  }

  async getQuotes({data, config}) {
    return (await this.client.post('/quotes', data, config));
  }
}
