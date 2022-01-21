import axios from "axios";

export default {
  async getWinningNumbers(accessToken) {
    console.log("API_URL:", process.env.VUE_APP_API_URL);
    const url = `${process.env.VUE_APP_API_URL}/winningNumbers`;
    const config = {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    };
    let winningNumbers = (await axios.get(url, config)).data;
    return winningNumbers;
  },
};
