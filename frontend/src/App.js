import React from 'react';
import {Route, BrowserRouter as Router} from 'react-router-dom'
import {home,Login,register } from './pages/index';
import {Navbar} from './components/index'

import "./App.css"

function App() {
  return (
    <Router>
      <Navbar />
      <Route exact path='/' component= {home}/>
      <Route exact path='/login' component={Login} />
      <Route exact path='/register' component={register}/>
    </Router>
  );
}

export default App;
