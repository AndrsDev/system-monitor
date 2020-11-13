import firebase from "firebase/app";
import 'firebase/database';

var config = {
  apiKey: "AIzaSyATj1ov6n6bfJ4QGvv8WrDWeox5aqimH2I",
  authDomain: "system-monitor-531ab.firebaseapp.com",
  databaseURL: "https://system-monitor-531ab.firebaseio.com",
  projectId: "system-monitor-531ab",
  storageBucket: "system-monitor-531ab.appspot.com",
  messagingSenderId: "154390991734",
  appId: "1:154390991734:web:79dc0f4d9d800ed695e057",
};

export default !firebase.apps.length ? firebase.initializeApp(config) : firebase.app();