import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import './App.css';

// ROUTES
import Home from './components/Home';
import Search from './components/Search';


const App = () => {
  return <>
    <Router>
      <Switch>

        <Route exact path='/'
          render={() => <Home />}
        />

        <Route exact path='/search'
          render={() => <Search />}
        />

      </Switch>
    </Router>

    </>
}

export default App;