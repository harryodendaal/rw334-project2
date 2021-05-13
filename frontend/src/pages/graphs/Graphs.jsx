import React, { useState, useEffect } from 'react'
import {Loader} from './Loader'

import styled from './Graph.module.css'
import axios from 'axios';
import * as d3 from 'd3'
import {drawGraph} from './drawGraph'

export const Graphs = () => {
  const [visType, setVisType] = useState('social-network');
  const [isLoading, setLoading] = useState(true)

  useEffect(() => {
    axios
    .get('http://127.0.0.1:5000/graphs/', {timeout: 28000})
    .then((res) => {
      // Loader equal to false... 
      setLoading(false);
      drawGraph(res.data, 'social-network');
    })
    .catch((e) => {
      console.log(e);
      alert(e);
    });
  }, []);
  
  function initGraph(graphType) {
    if (graphType === 'social-network') {
      d3.selectAll("svg > *").remove();
    } else if (graphType === 'label-propagation') {
      d3.selectAll("svg > *").remove();
    } else if (graphType === 'shortest-path') {
      d3.selectAll("svg > *").remove();
    } else if (graphType === 'centrality') {
      d3.selectAll("svg > *").remove();
    } else { return }

    let apiLink = "http://127.0.0.1:5000/graphs/";

    if (graphType !== 'social-network') {
      apiLink = apiLink + graphType;
    }

    setVisType(graphType);
    setLoading(true);

    axios
    .get(apiLink, {timeout: 28000})
    .then((res) => {
      // Loader equal to false... 
      setLoading(false);
      drawGraph(res.data, graphType);
    })
    .catch((e) => {
      console.log(e);
      alert(e);
    });

    
  }

  const zoomStyles = {
    overflow: 'hidden'
  }

  return (
    <div className={styled.btn}>
      <button onClick={() => initGraph('social-network')}>Social Network</button>
      <button onClick={() => initGraph('label-propagation')}>Label propagation</button>
      <button onClick={() => initGraph('shortest-path')}>Shortest path</button>
      <button onClick={() => initGraph('centrality')}>Centrality</button>
      <h1>{visType}</h1>
      < Loader isLoading={isLoading}/>
      <div style={zoomStyles}>
      <div className="viz"><svg width="1100" height="700"></svg></div>
      </div>
      
      

    </div>
  )
}