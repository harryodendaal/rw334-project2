import React, { useEffect, useState } from "react";
import {Route, BrowserRouter as Router} from 'react-router-dom'
import {home,Login,Register,Graphs, Employees } from './pages/index';
import {Navbar} from './components/index'

import "./App.css"

function App() {
  const [token, setToken] = useState(false);

  const changeTokenState =() => {
    setToken(state => state = !state)
  }
  useEffect(() => {
    if (localStorage.getItem("token") !== null) {
      setToken(true);
    } else {
      setToken(false);
    }
  }, [token]);
  return (
    <Router>
      <Navbar token={token} changeToken={changeTokenState}/>
      <Route exact path='/' component= {home}/>
      <Route exact path='/graphs' component= {Graphs}/>
      <Route exact path='/login'>
        <Login changeToken={changeTokenState}/>
      </Route>
      <Route exact path='/register'>
        <Register changeToken={changeTokenState}/>
      </Route>
      <Route exact path ='/employees'>
        <Employees/>
      </Route>
    </Router>
  );
}

export default App;
