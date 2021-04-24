import React from 'react'
import {Link} from 'react-router-dom'
import './navbar.css'

export const Navbar = () => {
  return (
    <div className="container">
      <nav>
        <ul>
          <li>
            <Link to="">Home</Link>
          </li>
          <li>
            <Link to="/register">Register</Link>
          </li>
          <li>
            <Link to="/login">Login</Link>
          </li>
        </ul>
      </nav>
    </div>
  )
}
