// Header.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faUsers, faBullseye, faLightbulb, faShoppingCart, faSearch, faEarth } from '@fortawesome/free-solid-svg-icons';
import './header.css';

const Header = () => {
  const headerOptions = [
    { icon: faUser, title: 'Profile' },
    { icon: faBullseye, title: 'Goals' },
    { icon: faLightbulb, title: 'Feedback' },
  ];

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-logo">
          <img src="./logo.png">
          </img>
        </div>
        <div className="header-options">
          {headerOptions.map((option, index) => (
            <div key={index} className="header-option">
              <FontAwesomeIcon icon={option.icon} />
              <span>{option.title}</span>
            </div>
          ))}
        </div>
      </div>
    </header>
  );
};

export default Header;
