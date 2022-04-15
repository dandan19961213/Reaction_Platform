import React from 'react';
import Home from './Home';
import Query from './Query';

import {
    BrowserRouter as Router,
    Route,
    Routes,
    Link
  } from "react-router-dom";

  export default function Routers() {
    return (
      <Router>
          <Routes>
            <Route exact path="/" element={<Home/>}>
            </Route>
            <Route path="/query" element={<Query/>}>
            </Route>
          </Routes>
      </Router>
    );
  }
  