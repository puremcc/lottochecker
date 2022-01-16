import axios from "axios";

export class Ticket {
  constructor(accessToken) {
    this.service = axios.create({
      baseURL: process.env.VUE_APP_API_URL,
    });
    this.service.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${accessToken}`;
  }

  async createTicket(ticket) {
    ticket.picks.forEach((pick) => {
      pick.numbers.forEach((number) => (number = +number));
    });
    await this.service.put("/tickets", ticket);
  }

  async listTickets() {
    let resp = await this.service.get("/tickets");
    return resp.data;
  }
}
