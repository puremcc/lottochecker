import firebase from "firebase/app";
import "firebase/firestore";
import firebaseConfig from "../firebase.config";

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

export class Ticket {

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