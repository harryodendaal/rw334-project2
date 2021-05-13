import React, { useEffect } from 'react'
import {ReactComponent as Spinner} from './loader.svg';

export const Loader = (props) => {

  useEffect(() => {
    
  }, );

  const zoomStyles = {
    overflow: 'hidden'
  }

  return props.isLoading ? ( <Spinner /> ) : null
}