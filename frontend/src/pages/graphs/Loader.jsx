import React from 'react'
import {ReactComponent as Spinner} from './loader.svg';

export const Loader = (props) => {

  return props.isLoading ? ( <Spinner /> ) : null
}