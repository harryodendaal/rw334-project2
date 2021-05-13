import React, { useEffect, useState } from 'react'
import axios from 'axios';
import * as d3 from 'd3'
import {drawGraph} from './drawGraph'

export const Graph = (props) => {

  useEffect(() => {
    
  }, );

  const zoomStyles = {
    overflow: 'hidden'
  }

  return (
    <div>
      <div style={zoomStyles}>
      <div className="viz"><svg width="1100" height="700"></svg></div>
      </div>
    </div>
  )
}