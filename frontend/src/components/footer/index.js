import React from 'react';
import styles from './style.module.css'
import Container from '../container'

const Footer = () => {
  return <footer className={styles.footer}>
    <Container>
      <div className={styles.footer__container}>
        <p className={styles.footer__text}>© 2024 Foodgram</p>
      </div>
    </Container>
  </footer>
}

export default Footer
