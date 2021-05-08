import React, { useState } from 'react'
import {Graph} from './Graph'
import styled from './Graph.module.css'

export const Graphs = () => {
  const [visType, setVisType] = useState('social-network');

  return (
    <div class={styled.btn}>
      <button onClick={() => setVisType('social-network')}>Social Network</button>
      <button onClick={() => setVisType('label-propagation')}>Label propagation</button>
      <button onClick={() => setVisType('shortest-path')}>Shortest path</button>
      <button onClick={() => setVisType('centrality')}>Centrality</button>
      {visType !== '' ? <Graph visType={visType} /> : null}

    </div>
  )
}