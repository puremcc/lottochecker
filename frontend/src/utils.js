import { DateTime } from "luxon";

export default {
  getResults(ticket, winningNumbers) {
    const prizes = [0, 0, 0, 3, 56, 2000, 10e6];
    const playerPicks = this.expandTicket(
      ticket.startDate,
      ticket.endDate,
      ticket.picks[0].numbers
    );
    return playerPicks.map((pick) => {
      // Lookup winning numbers for this pick.
      let _winningNumbers = winningNumbers.find(
        (drawing) => drawing.drawingDate === pick.drawingDate
      );
      // Check for matches between player pick numbers and winning numbers.
      let matches = this.findMatches(pick, _winningNumbers);
      return {
        drawingDate: pick.drawingDate,
        numbers: pick.numbers,
        winningNumbers: _winningNumbers,
        matches,
        prize: prizes[matches.length],
      };
    });
  },

  expandTicket(sStartDate, sEndDate, numbers) {
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

  findMatches(playerPick, winningPick) {
    return !winningPick
      ? []
      : playerPick.numbers.filter(
          (playerNum) =>
            !!winningPick.numbers.find((winningNum) => winningNum === playerNum)
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
