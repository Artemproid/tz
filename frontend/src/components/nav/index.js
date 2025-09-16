import styles from './style.module.css'
import { useState, useEffect } from 'react'
import { AccountMenu, NavMenu, AccountMenuMobile } from '../index.js'
import cn from 'classnames'
import { useLocation } from 'react-router-dom'

const Nav = ({ loggedIn, onSignOut }) => {
  const [menuToggled, setMenuToggled] = useState(false)
  const location = useLocation()
  
  useEffect(() => {
    const cb = () => {
      setMenuToggled(false)
    }
    window.addEventListener('resize', cb)
    return () => window.removeEventListener('resize', cb)
  }, [])

  useEffect(() => {
    setMenuToggled(false)
  }, [location.pathname])

  return <div className={styles.nav}>
    <div className={styles.nav__container}>
      <NavMenu loggedIn={loggedIn} />
      <AccountMenu onSignOut={onSignOut} />
    </div>

    <div className={cn(styles['nav__container-mobile'], {
      [styles['nav__container-mobile_visible']]: menuToggled
    })}>
      <NavMenu loggedIn={loggedIn} />
      <AccountMenuMobile onSignOut={onSignOut} />
    </div>
  </div>
}

export default Nav
