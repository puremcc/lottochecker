const firebase = require("firebase/app");
require("firebase/firestore");
// const firebaseConfig = require("firebase.config");
const firebaseConfig = {
    apiKey: "AIzaSyBC8mQDTgIshNny7_dfBVajPml5_ne6P-Q",
    authDomain: "lotto-checker-9490e.firebaseapp.com",
    projectId: "lotto-checker-9490e",
    storageBucket: "lotto-checker-9490e.appspot.com",
    messagingSenderId: "721404318244",
    appId: "1:721404318244:web:42da875931e22c30757eb1"
  };

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

class Ticket {

    async createTicket(ticket) {
        ticket.picks.forEach(pick => {
            pick.numbers.forEach(number => number = +number);
        });
        let docRef = await db.collection("tickets").add(ticket);
        console.log("Document written with ID: ", docRef.id);
    }

    async listTickets() {
        let tickets = [];
        const querySnapshot = await db.collection("tickets").get();
        querySnapshot.forEach(doc => tickets.push(doc.data()));
        // return querySnapshot.map(doc => doc.data());
        return tickets;
    }
}
// import { Ticket } from "./models/firebase";
// const { Ticket } = require("./models/firebase");

const ticketModel = new Ticket();

ticketModel.listTickets().then(tickets => {
    // console.log(JSON.stringify(tickets))
    var fs = require('fs');
    fs.writeFile("firebase_export.json", tickets, function(err) {
        if (err) {
            console.log(err);
        }
    });
});

