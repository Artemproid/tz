import styles from './styles.module.css'
import { NavLink } from 'react-router-dom'

const NavMenu = () => {
  const menuItems = [
    { title: 'Главная', path: '/' },
    { title: 'Категории', path: '/categories' },
    { title: 'Подкатегории', path: '/subcategories' },
    { title: 'Типы', path: '/types' },
    { title: 'Статусы', path: '/statuses' }
  ]

  return (
    <nav className={styles.nav}>
      <ul className={styles.menuList}>
        {menuItems.map(item => (
          <li key={item.path} className={styles.menuItem}>
            <NavLink
              exact
              to={item.path}
              className={styles.menuLink}
              activeClassName={styles.menuLink_active}
            >
              {item.title}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}

export default NavMenu