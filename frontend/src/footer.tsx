import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faInstagram, faFacebook, faGithub, faLinkedin } from '@fortawesome/free-brands-svg-icons';
import { faCopyright, faEnvelope } from '@fortawesome/free-solid-svg-icons';
import './footer.css';

const Footer = () => {
  return (
    <footer>
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <h4>FileBot : LLM ChatBot</h4>
            <p>
              Jaypee Institute Of Information Technology, Noida, India<br />
              <strong>Phone :</strong> +91 86904 09766<br />
              <strong>Email :</strong> adityaryk123@gmail.com
            </p>
          </div>
          <div className="footer-section">
            <h4>Useful Links</h4>
            <ul>
              <li><FontAwesomeIcon icon={faEnvelope} /><a href="mailto:adityaryk123@gmail.com" target="_blank">&nbsp; &nbsp; &nbsp;Email</a></li>
              <li><FontAwesomeIcon icon={faInstagram} /><a href="https://www.instagram.com/shrivastava_aditya_/" target="_blank">&nbsp; &nbsp; &nbsp;Instagram</a></li>
              <li><FontAwesomeIcon icon={faFacebook} /><a href="https://www.facebook.com/profile.php?id=100009027675998" target="_blank">&nbsp; &nbsp; &nbsp;Facebook</a></li>
              <li><FontAwesomeIcon icon={faGithub} /><a href="https://github.com/shrivastavaditya" target="_blank">&nbsp; &nbsp; &nbsp;GitHub</a></li>
              <li><FontAwesomeIcon icon={faLinkedin} /><a href="https://www.linkedin.com/in/aditya-kumar-14b6a6222/" target="_blank">&nbsp; &nbsp; &nbsp;LinkedIn</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <div className="max-w-7xl flex flex-col sm:flex-row py-4 mx-auto justify-around items-center">
          <div className="text-center">
            <div>
              <i>
                <FontAwesomeIcon icon={faCopyright}></FontAwesomeIcon>
              </i> 2023 Copyright <strong><span>FileBot</span></strong>. All Rights Reserved.
            </div>
            <div>
            &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;Designed by <a href="https://www.linkedin.com/in/aditya-shrivastava-14b6a6222/" className="text-purple-500">Aditya Kumar</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
