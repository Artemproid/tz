import React, { useState } from 'react'
import { Link, useHistory } from 'react-router-dom'
import styles from './style.module.css'
import { Container } from '../index.js'
import cn from 'classnames'

const Header = ({ loggedIn }) => {
  const history = useHistory()
  const [isMenuOpen, setMenuOpen] = useState(false)
  const [isReferencesOpen, setReferencesOpen] = useState(false)
  const referencesTimeoutRef = React.useRef(null)

  const handleSignOut = () => {
    localStorage.removeItem('token')
    history.push('/signin')
    window.location.reload()
  }

  const handleReferencesMouseEnter = () => {
    if (referencesTimeoutRef.current) {
      clearTimeout(referencesTimeoutRef.current)
    }
    setReferencesOpen(true)
  }

  const handleReferencesMouseLeave = () => {
    referencesTimeoutRef.current = setTimeout(() => {
      setReferencesOpen(false)
    }, 300)
  }

  return <header className={styles.header}>
    <Container>
      <div className={styles.header__container}>
        <nav className={styles.header__nav}>
          <div className={styles.header__nav__container}>
            <Link to='/' className={styles.header__link}>
              <span>Главная</span>
            </Link>
            {loggedIn && (
              <>
                <button 
                  className={styles.createButton}
                  onClick={() => history.push('/money-flow-create')}
                >
                  Создать запись
                </button>
                <div 
                  className={styles.dropdown}
                  onMouseEnter={handleReferencesMouseEnter}
                  onMouseLeave={handleReferencesMouseLeave}
                >
                  <button className={styles.referencesButton}>
                    Справочники ▼
                  </button>
                  <div className={cn(styles.dropdownContent, {
                    [styles.show]: isReferencesOpen
                  })}>
                    <Link to='/statuses' className={styles.dropdownLink}>
                      Статусы
                    </Link>
                    <Link to='/types' className={styles.dropdownLink}>
                      Типы операций
                    </Link>
                    <Link to='/categories' className={styles.dropdownLink}>
                      Категории
                    </Link>
                    <Link to='/subcategories' className={styles.dropdownLink}>
                      Подкатегории
                    </Link>
                  </div>
                </div>
              </>
            )}
          </div>
          <div className={styles.right}>
            {loggedIn ? (
              <div className={styles.dropdown}>
                <button 
                  className={styles.dropbtn}
                  onClick={() => setMenuOpen(!isMenuOpen)}
                >
                  Профиль
                </button>
                <div className={cn(styles.dropdownContent, {
                  [styles.show]: isMenuOpen
                })}>
                  <Link to='/change-password' className={styles.dropdownLink}>
                    Изменить пароль
                  </Link>
                  <button 
                    className={styles.dropdownButton}
                    onClick={handleSignOut}
                  >
                    Выйти
                  </button>
                </div>
              </div>
            ) : (
              <div className={styles.header__nav__container}>
                <Link to='/signin' className={styles.header__link}>
                  Войти
                </Link>
                <Link to='/signup' className={styles.header__link}>
                  Регистрация
                </Link>
              </div>
            )}
          </div>
        </nav>
      </div>
    </Container>
  </header>
}

export default Header
