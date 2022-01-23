import { DateTime } from "luxon";

export default {
  expandTicket(sStartDate, sEndDate, numbers) {
    console.log('[expandTicket]:', sStartDate, sEndDate, numbers)
    const picks = [];
    let drawingDate = DateTime.fromISO(sStartDate, { zone: "America/Chicago" });
    const endDate = DateTime.fromISO(sEndDate, { zone: "America/Chicago" });
    while (drawingDate <= endDate) {
      if (this.isValidDrawingDate(drawingDate)) {
        picks.push({
          drawingDate: drawingDate.toISODate(),
          numbers: numbers.map((x) => +x),
        });
      }
      drawingDate = drawingDate.plus({ days: 1 });
    }
    return picks;
  },

  getResults(ticket, winningNumbers) {
    const prizes = [0, 0, 0, 3, 56, 2000, 10e6];
    const playerPicks = this.expandTicket(
      ticket.startDate,
      ticket.endDate,
      ticket.picks[0].numbers
    );
    const ticketResults = new Array(playerPicks.length);
    playerPicks.forEach((playerPick) => {
      let thisResult = {
        drawingDate: playerPick.drawingDate,
        numbers: playerPick.numbers,
        winningNumbers: null,
        matches: null,
        prize: null,
      };
      thisResult.winningNumbers = winningNumbers.find(
        (drawing) => drawing.drawingDate === playerPick.drawingDate
      );
      if (thisResult.winningNumbers) {
        thisResult.matches = this.findMatches(
          playerPick,
          thisResult.winningNumbers
        );
        thisResult.prize = prizes[thisResult.matches.length];
      }
      ticketResults.push(thisResult);
    });
    return ticketResults;
  },

  findMatches(playerPick, winingPick) {
    return playerPick.numbers.filter(
      (playerNum) =>
        !!winingPick.numbers.find((winningNum) => winningNum === playerNum)
    );
  },

  isValidDrawingDate(drawingDate) {
    var validDays = [1, 3, 6]; // Drawings are on Mon, Wed, Sat.
    if (drawingDate < new Date("2021-08-23"))
      // Prior to 2021-08-23 drawings were only Wed, Sat.
      validDays = [3, 6];
    return validDays.includes(drawingDate.weekday);
  },

  isoStringToLocaleString(isoDateString) {
    const split = isoDateString.split("-");
    return `${+split[1]}/${+split[2]}/${+split[0]}`;
  },
};
