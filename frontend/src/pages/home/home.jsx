import React from 'react';
import image from './logo1.jpg';
import styled from './home.module.css';

import rutger from './Rutger.jpeg'
import harry from './Harry.jpeg'
import bernard from './Bernard.jpeg'
import anna from './Anna.jpg'
import jacq from './jacq.jpeg'
import kaylan from './kaylan.jpeg'


export const home = () => {
  return (
    <div class={styled.border}> 
      <h1>Home</h1>
      <ul className="Group">
        <div class = {styled.group}>
          <h1 className="heading">Meet the Team</h1>
          <section>
          <div class="column"> 
            <div class={styled.column}>
                  <img src={harry} alt="member"/>
                  <h4>Harry Odendaal</h4>
                  <h4>22794484</h4>
                </div>
            </div>
          </section>
          <section>
            <div class="column">
            <div class={styled.column}>
              <img src={bernard} alt="member"/>
              <h4>Bernard Oosthuizen</h4>
              <h4>21570124</h4>
              </div>
            </div>            
          </section>
          <section>
            <div class="column">
            <div class={styled.column}>
              <img src={jacq} alt="member"/>
              <h4>Jacques Le Roux</h4>
              <h4>23068574</h4>
              </div>
            </div>            
          </section>
        </div>
        <div class = "row">
          <section>
          <div class="column"> 
            <div class={styled.column}>
                  <img src={anna} alt="member"/>
                  <h4>Anna Davies</h4>
                  <h4>21161097</h4>
                </div>
            </div>
          </section>
          <section>
          <div class="column"> 
            <div class={styled.column}>
                  <img src={kaylan} alt="member"/>
                  <h4>Kaylan Naidu</h4>
                  <h4>22778063</h4>
                </div>
            </div>
          </section>
          <section>
          <div class="column"> 
            <div class={styled.column}>
                  <img src={rutger} alt="member" height="400"/>
                  <h4>Rutger van Huyssteen</h4>
                  <h4>23052228</h4>
                </div>
            </div>
          </section>

        </div>
      </ul>

    </div>
  )
}




